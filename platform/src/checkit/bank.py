from lxml import etree
import os, time, json, zipfile, io, csv, shutil
from .outcome import Outcome
from .xml import CHECKIT_NS, xml_boilerplate

class Bank():
    def __init__(self, path="."):
        # read manifest for bank
        xml = etree.parse(os.path.join(path,"bank.xml")).getroot()
        if xml.get("version") != "0.2":
            raise Exception("ERROR: Bank configuration doesn't match CheckIt version 0.2")
        self.title = xml.find(f"{CHECKIT_NS}title").text
        self.url = xml.find(f"{CHECKIT_NS}url").text
        # create each outcome
        self.outcomes = [
            Outcome(
                ele.find(f"{CHECKIT_NS}title").text,
                ele.find(f"{CHECKIT_NS}slug").text,
                ele.find(f"{CHECKIT_NS}path").text,
                ele.find(f"{CHECKIT_NS}description").text,
                self,
            )
            for ele in xml.find(f"{CHECKIT_NS}outcomes").iter(f"{CHECKIT_NS}outcome")
        ]
    
    def generate_exercises(self,public=False,amount=300,regenerate=False):
        # cache build path
        self.build_path(public,regenerate)
        # cache exercises
        for o in self.outcomes:
            o.generate_exercises(public,amount,regenerate)

    def build_path(self,public=False,regenerate=False):
        if not(regenerate):
            try:
                return self.__build_path
            except:
                pass
        if public:
            build_dir = os.path.join("docs")
        else:
            build_dir = os.path.join("builds",time.strftime("%Y-%m-%d_%H%M%S", time.localtime()))
        self.__build_path = os.path.join("banks",self.slug,build_dir)
        os.makedirs(self.__build_path, exist_ok=True)
        os.makedirs(os.path.join(self.__build_path,"pretext"), exist_ok=True)
        return self.__build_path

    def generate_dict(self,public=False,amount=300,regenerate=False):
        if public:
            exs = "public exercises"
        else:
            exs = "private exercises"
        olist = [o.generate_dict(public,amount,regenerate) for o in self.outcomes]
        return {
            "title": self.title,
            "slug": self.slug,
            "url": self.url,
            "outcomes": olist,
        }

    def write_json(self,public=False,amount=300,regenerate=False):
        build_path = os.path.join(self.build_path(public,regenerate),f"bank.json")
        with open(build_path,'w') as f:
            json.dump(self.generate_dict(public,amount,regenerate),f)
        return f"- CheckIt exercise bank JSON written to [{build_path}]({self.build_path(public)})"

    def outcome_csv_list(self):
        outcome_csv = [[
            "vendor_guid",
            "object_type",
            "title",
            "description",
            "display_name",
            "calculation_method",
            "calculation_int",
            "mastery_points",
            "ratings",
        ]]
        oid_suffix = time.time()
        for count,outcome in enumerate(self.outcomes):
            outcome_csv.append(outcome.csv_row(count,oid_suffix))
        return outcome_csv

    def write_canvas_outcome_csv(self,public=False,regenerate=False):
        build_path = os.path.join(self.build_path(public), f"canvas-outcomes.csv")
        with open(build_path,'w') as f:
            csv.writer(f).writerows(self.outcome_csv_list())
        return f"- Canvas outcome CSV written to [{build_path}]({self.build_path(public)})"

    def outcome_from_slug(self,outcome_slug):
        return [x for x in self.outcomes if x.slug==outcome_slug][0]

    def sample_for_outcome(self,outcome_slug):
        return self.outcome_from_slug(outcome_slug).generate_exercises(amount=1,regenerate=True,save=False)[0]

    def write_canvas_zip(self,public=False,amount=300,regenerate=False):
        build_path = os.path.join(self.build_path(public), f"canvas-question-bank.zip")
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for outcome in self.outcomes:
                zip_file.writestr(
                    f"{outcome.slug}.qti",
                    str(etree.tostring(outcome.canvas_tree(public,amount,regenerate),
                                            encoding="UTF-8", xml_declaration=True),"UTF-8")
                )
        with open(build_path,'wb') as f:
            f.write(zip_buffer.getvalue())
        return f"- Canvas question bank ZIP written to [{build_path}]({self.build_path(public)})"

    def brightspace_manifest_tree(self):
        IMSMD = "{http://www.imsglobal.org/xsd/imsmd_rootv1p2p1}"
        tree = xml_boilerplate("brightspace_manifest")
        for elem in tree.iterfind(f".//{IMSMD}langstring"):
            elem.text = self.title
        return tree

    def brightspace_questiondb_tree(self,public=False,amount=300,regenerate=False):
        tree = xml_boilerplate("brightspace_questiondb")
        for o in self.outcomes:
            tree.find("objectbank").append(o.brightspace_tree(public,amount,regenerate).getroot())
        #print(str(etree.tostring(tree,pretty_print=True), 'utf-8'))
        return tree

    def write_brightspace_zip(self,public=False,amount=300,regenerate=False):
        build_path = os.path.join(self.build_path(public), f"brightspace-question-bank.zip")
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            zip_file.writestr(
                f"imsmanifest.xml",
                str(etree.tostring(self.brightspace_manifest_tree(),
                                        encoding="UTF-8", xml_declaration=True),"UTF-8")
            )
            zip_file.writestr(
                f"questiondb.xml",
                str(etree.tostring(self.brightspace_questiondb_tree(public,amount,regenerate),
                                        encoding="UTF-8", xml_declaration=True),"UTF-8")
            )
        with open(build_path,'wb') as f:
            f.write(zip_buffer.getvalue())
        return f"- Brightspace question bank ZIP written to [{build_path}]({self.build_path(public)})"

    def moodle_xmle(self,public=False,amount=300,regenerate=False):
        root = etree.Element("quiz")
        header = etree.SubElement(root,"question")
        header.set("type","category")
        category = etree.SubElement(header,"category")
        category_text = etree.SubElement(category,"text")
        category_text.text = f"$course$/top/checkit/{self.slug}"
        info = etree.SubElement(header,"info")
        info_text = etree.SubElement(info,"text")
        info_text.text = self.title
        root.append(header)
        for o in self.outcomes:
            for q in o.moodle_xmle(public,amount,regenerate).xpath("question"):
                root.append(q)
        return root

    def write_moodle_xml(self,public=False,amount=300,regenerate=False):
        build_path = os.path.join(self.build_path(public), f"moodle-question-bank.xml")
        et = etree.ElementTree(self.moodle_xmle(public,amount,regenerate))
        et.write(build_path)
        return f"- Moodle question bank XML written to [{build_path}]({self.build_path(public)})"

    def write_pretext_files(self,public=False,amount=300,regenerate=False):
        for outcome in self.outcomes:
            for n,exercise in enumerate(outcome.generate_exercises(public=public,amount=amount,regenerate=regenerate)[:10]):
                build_path = os.path.join(self.build_path(public), "pretext", f"{outcome.slug}-{n}.ptx")
                et = etree.ElementTree(exercise.pretext_tree())
                et.write(build_path, pretty_print=True)
        return f"- Pretext files written to [{self.build_path(public)}/pretext]({self.build_path(public)})"

    def write_outcomes_boilerplate(self):
        outcomes_path = os.path.join("banks",self.slug,"outcomes")
        os.makedirs(outcomes_path,exist_ok=True)
        for outcome in self.outcomes:
            if not os.path.isfile(os.path.join(outcomes_path,f"{outcome.slug}.xml")):
                shutil.copyfile(
                    os.path.join("xml","template_boilerplate.xml"),
                    os.path.join(outcomes_path,f"{outcome.slug}.xml"),
                )
            if not os.path.isfile(os.path.join(outcomes_path,f"{outcome.slug}.sage")):
                shutil.copyfile(
                    os.path.join("wrappers","sage_boilerplate.sage"),
                    os.path.join(outcomes_path,f"{outcome.slug}.sage"),
                )

    def copy_viewer(self,public=False):
        copy_from_path = os.path.join("viewer")
        copy_to_path = self.build_path(public)
        shutil.copytree(copy_from_path,copy_to_path,dirs_exist_ok=True)
        return f"- Viewer copied to [{copy_to_path}/index.html]({copy_to_path}/index.html)."

    def build(self,public=False,amount=300,regenerate=False):
        print(self.write_json(public,amount,regenerate))
        print(self.write_canvas_zip(public,regenerate=False))
        print(self.write_canvas_outcome_csv(public,regenerate=False))
        print(self.write_brightspace_zip(public,regenerate=False))
        print(self.write_moodle_xml(public,regenerate=False))
        print(self.write_pretext_files(public,regenerate=False))
        print(self.copy_viewer(public))
