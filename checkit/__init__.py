import lxml.etree, lxml.html
import os, json, subprocess, time, csv, io, zipfile
from IPython.core.display import display, HTML, Markdown
import urllib

TRANSFORM = {
    filetype: lxml.etree.XSLT(lxml.etree.parse(os.path.join("xsl",f"{filetype}.xsl")))
    for filetype in ["html","latex","qti"]
}



# XSL Helpers
def insert_object_into_element(obj,name,element):
    """
    Inserts Python object into xml element
    """
    if obj is False:
        # skip generating element only when exactly False (not falsy)
        # since xsl:if checks if element exists
        return None
    se = lxml.etree.SubElement(element, name)
    if isinstance(obj, list):
        for item in obj:
            insert_object_into_element(item,"item",se)
    elif isinstance(obj, dict):
        for key in obj.keys():
            insert_object_into_element(obj[key],key,se)
    else:
        se.text = str(obj)

def dict_to_tree(data_dict,seed):
    """
    Takes a dictionary of data (typically randomized exercise data)
    and represents it as an XML tree
    """
    data = lxml.etree.Element("data")
    data.attrib['seed'] = f"{seed:04}"
    for key in data_dict.keys():
        insert_object_into_element(data_dict[key], key, data)
    return data



# Banks contain many Outcomes generate many Exercises

class Bank():
    def __init__(self, slug=None):
        # read manifest for bank
        xml = lxml.etree.parse(os.path.join("banks",slug,"bank.xml")).getroot()
        self.title = xml.find("title").text
        self.slug = xml.find("slug").text
        self.author = xml.find("author").text
        self.url = xml.find("url").text
        # create each outcome
        self.outcomes = [
            Outcome(
                ele.find("title").text,
                ele.find("slug").text,
                ele.find("description").text,
                ele.find("alignment").text,
                self,
            )
            for ele in xml.xpath("outcomes/outcome")
        ]

    def build_path(self,public=False,regenerate=False):
        if not(regenerate):
            try:
                return self.__build_path
            except:
                pass
        if public:
            build_dir = "public"
        else:
            build_dir = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
        self.__build_path = os.path.join("banks",self.slug,"builds",build_dir)
        os.makedirs(self.__build_path, exist_ok=True)
        return self.__build_path

    def generate_dict(self,public=False,amount=300,regenerate=False):
        if public:
            exs = "public exercises"
        else:
            exs = "private exercises"
        print(f"Generating {exs} for {len(self.outcomes)} outcomes...")
        olist = [o.generate_dict(public,amount,regenerate) for o in self.outcomes]
        print("Exercises successfully generated for all outcomes!")
        return {
            "title": self.title,
            "slug": self.slug,
            "outcomes": olist,
        }

    def write_json(self,public=False,amount=300,regenerate=False):
        build_path = os.path.join(self.build_path(public,regenerate),f"{self.slug}-bank.json")
        with open(build_path,'w') as f:
            json.dump(self.generate_dict(public,amount,regenerate),f)
        display(Markdown(f"- Bank JSON written to [{build_path}]({self.build_path(public)})"))

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

    def write_outcome_csv(self,public=False,regenerate=False):
        build_path = os.path.join(self.build_path(public), f"{self.slug}-canvas-outcomes.csv")
        with open(build_path,'w') as f:
            csv.writer(f).writerows(self.outcome_csv_list())
        display(Markdown(f"- Outcome CSV written to [{build_path}]({self.build_path(public)})"))

    def outcome_from_slug(self,outcome_slug):
        return [x for x in self.outcomes if x.slug==outcome_slug][0]

    def sample_for_outcome(self,outcome_slug):
        return self.outcome_from_slug(outcome_slug).generate_exercises(amount=1,regenerate=True,save=False)[0]

    def write_qti_zip(self,public=False,amount=300,regenerate=False):
        build_path = os.path.join(self.build_path(public), f"{self.slug}-canvas-qtibank.zip")
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for outcome in self.outcomes:
                zip_file.writestr(
                    f"{outcome.slug}.qti",
                    str(lxml.etree.tostring(outcome.qtibank_tree(public,amount,regenerate),
                                            encoding="UTF-8", xml_declaration=True),"UTF-8")
                )
        with open(build_path,'wb') as f:
            f.write(zip_buffer.getvalue())
        display(Markdown(f"- Canvas QTI bank zip written to [{build_path}]({self.build_path(public)})"))

    def build(self,public=False,amount=300,regenerate=False):
        self.write_json(public,amount,regenerate)
        self.write_qti_zip(public,amount,regenerate)
        self.write_outcome_csv(public,regenerate)


class Outcome():
    def __init__(self, title=None, slug=None, description=None, alignment=None, bank=None):
        self.title = title
        self.slug = slug
        self.description = description
        self.alignment = alignment
        self.bank = bank

    def template_filepath(self):
        return os.path.join(
            "banks",
            self.bank.slug,
            "outcomes",
            f"{self.slug}.ptx"
        )

    def template(self):
        with open(self.template_filepath()) as template_file:
            template_file_text = template_file.read()
        complete_template = f"""<?xml version="1.0"?>
          <xsl:stylesheet version="1.0"
                          xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
              <xsl:output method="xml"/>
              <xsl:template match="/data">
                  {template_file_text}
              </xsl:template>
          </xsl:stylesheet>
        """
        return lxml.etree.XSLT(lxml.etree.XML(complete_template))

    def generator_directory_path(self):
        return os.path.join(
            "banks",
            self.bank.slug,
            "outcomes"
        )

    def generator_filename(self):
        return f"{self.slug}.sage"

    def generate_exercises(self,public=False,amount=300,regenerate=False,save=True):
        if not(regenerate):
            try:
                return self.__exercises
            except:
                pass
        # get sage script to run generator
        script_path = os.path.join("wrappers","sage_wrapper.sage")
        # run script to return JSON output with [amount] seeds
        command = ["sage",script_path,self.generator_directory_path(),self.generator_filename(),str(amount)]
        if public:
            command.append("PUBLIC")
        else:
            command.append("PRIVATE")
        if public:
            exs = "public exercises"
        else:
            exs = "private exercises"
        print(f"Generating {amount} {exs} for {self.slug}...",end=" ")
        # returns json list of exercise objects
        result = subprocess.run(command,capture_output=True)
        if result.stderr:
            print("ERROR, no exercises generated:")
            print(result.stdout.decode())
            print(result.stderr.decode())
            return []
        data_json_list = result.stdout
        print("Done!")
        data_list = json.loads(data_json_list)
        exercises = [
            Exercise(data["values"],data["seed"],self) \
            for data in data_list
        ]
        if save:
            self.__exercises = exercises
        return exercises

    def generate_dict(self,public=False,amount=300,regenerate=False):
        exercises = self.generate_exercises(public,amount,regenerate)
        return {
            "title": self.title,
            "slug": self.slug,
            "description": self.description,
            "alignment": self.alignment,
            "exercises": [e.dict() for e in exercises],
        }

    def qtibank_tree(self,public=False,amount=300,regenerate=False):
        qtibank_tree = lxml.etree.fromstring(f"""<?xml version="1.0"?>
          <questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd">
            <objectbank ident="{self.bank.slug}_{self.slug}">
              <qtimetadata>
                <qtimetadatafield/>
              </qtimetadata>
            </objectbank>
          </questestinterop>""")
        label = lxml.etree.SubElement(qtibank_tree.find("*/*/*"), "fieldlabel")
        label.text = "bank_title"
        entry = lxml.etree.SubElement(qtibank_tree.find("*/*/*"), "fieldentry")
        entry.text = f"{self.bank.title} -- {self.slug}"
        for exercise in self.generate_exercises(public,amount,regenerate):
            qtibank_tree.find("*").append(exercise.qti_tree())
        return qtibank_tree

    def csv_row(self,count,oid_suffix):
        return [
            f"checkit_{self.bank.slug}_{count:02}_{self.slug}_{oid_suffix:06}",
            "outcome",
            f"{count:02}-{self.slug}: {self.title}",
            "",
            self.slug,
            "n_mastery",
            "2",
            "3",
            "4",
            "Exceeds Mastery",
            "3",
            "Meets Mastery",
            "2",
            "Near Mastery",
            "1",
            "Well Below Mastery",
            "0",
            "Insufficient Work to Assess",
        ]

    def print_preview(self):
        ex = self.generate_exercises(amount=1,regenerate=True,save=False)[0]
        display(HTML("<h2>Preview:</h2> "+ex.html()))
        ex.print_preview()


class Exercise:
    def __init__(self, data=None, seed=None, outcome=None):
        self.data = data
        self.seed = seed
        self.outcome = outcome

    def data_tree(self):
        return dict_to_tree(self.data,self.seed)

    def pretext_tree(self):
        transform = self.outcome.template()
        tree = transform(self.data_tree()).getroot()
        tree.xpath("/*")[0].attrib['checkit-seed'] = f"{self.seed:04}"
        tree.xpath("/*")[0].attrib['checkit-slug'] = str(self.outcome.slug)
        tree.xpath("/*")[0].attrib['checkit-title'] = str(self.outcome.title)
        return tree

    def pretext(self):
        return str(lxml.etree.tostring(self.pretext_tree(), pretty_print=True), encoding="UTF-8")

    def html_tree(self):
        transform = TRANSFORM["html"]
        tree = transform(self.pretext_tree()).getroot()
        return tree

    def html(self):
        return str(lxml.etree.tostring(self.html_tree(),pretty_print=True), 'UTF-8')

    def latex(self):
        transform = TRANSFORM["latex"]
        return str(transform(self.pretext_tree()))

    def qti_tree(self):
        transform = TRANSFORM["qti"]
        tree = transform(self.pretext_tree()).getroot()
        for mattextxml in tree.xpath("//mattextxml"):
            for img in mattextxml.xpath("//img"):
                tex = img.get("data-equation-content")
                src = "https://pi998nv7pc.execute-api.us-east-1.amazonaws.com/production/svg?tex="+urllib.parse.quote(tex)
                img.set("src",src)
            mattext = lxml.etree.Element("mattext")
            mattext.attrib['texttype'] = 'text/html'
            mattext.text = lxml.html.tostring(lxml.html.fromstring(lxml.etree.tostring(mattextxml.find("*"),pretty_print=True)),pretty_print=True)
            mattextxml.addnext(mattext)
        return tree

    def qti(self):
        return str(lxml.etree.tostring(self.qti_tree(),pretty_print=True), 'UTF-8')

    def dict(self):
        return {
            "seed": self.seed,
            #"qti": self.qti(),
            "pretext": self.pretext(),
            "html": self.html(),
            "tex": self.latex(),
        }

    def print_preview(self):
        print("Data XML")
        print("-----------")
        print(str(lxml.etree.tostring(self.data_tree(), pretty_print=True), "UTF-8"))
        print()
        print("HTML source")
        print("-----------")
        print(self.html())
        print()
        print("LaTeX source")
        print("------------")
        print(self.latex())
        print()
        print("QTI source")
        print("------------")
        print(self.qti())
        print()
        print("PreTeXt source")
        print("------------")
        print(self.pretext())

