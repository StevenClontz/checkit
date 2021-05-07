from .exercise import Exercise
from lxml import etree
from IPython.display import display, HTML
import subprocess, os, json

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
            f"{self.slug}.xml"
        )

    def template(self):
        xml = etree.parse(self.template_filepath()).getroot()
        for e in xml.getiterator():
            if etree.QName(e).localname=="v":
                e.tag=f"{XSL}value-of"
                e.set("select",e.get("of"))
                del e.attrib["of"]
            elif etree.QName(e).localname=="for-each":
                e.tag=f"{XSL}for-each"
                e.set("select",e.get("of")+"/*")
                del e.attrib["of"]
            elif etree.QName(e).localname=="cases":
                e.tag=f"{XSL}choose"
                check = e.get("of")
                del e.attrib["of"]
                for case in e.iterfind("{*}case"):
                    case.tag=f"{XSL}when"
                    value = case.get("when")
                    del case.attrib["when"]
                    case.set("test", f"{check} = '{value}'")
                for case_true in e.iterfind("{*}case-true"):
                    case_true.tag=f"{XSL}when"
                    case_true.set("test", check)
                for otherwise in e.iterfind("{*}otherwise"):
                    otherwise.tag = f"{XSL}otherwise"
            elif etree.QName(e).localname=="exercise":
                e.tag=etree.QName(e).localname
                del e.attrib["version"]
            else:
                if etree.QName(e).namespace!=XSL[1:-1]:
                    e.tag=etree.QName(e).localname
        etree.cleanup_namespaces(xml)
        xsl = etree.Element(f"{XSL}stylesheet")
        xsl.set('version', "1.0")
        output = etree.SubElement(xsl,f"{XSL}output")
        output.set('method', "xml")
        template = etree.SubElement(xsl,f"{XSL}template")
        template.set('match', "/data")
        template.append(xml)
        #print(etree.tostring(xsl).decode("UTF-8"))
        return etree.XSLT(xsl)

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
        qtibank_tree = etree.fromstring(f"""<?xml version="1.0"?>
          <questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd">
            <objectbank ident="{self.bank.slug}_{self.slug}">
              <qtimetadata>
                <qtimetadatafield/>
              </qtimetadata>
            </objectbank>
          </questestinterop>""")
        label = etree.SubElement(qtibank_tree.find("*/*/*"), "fieldlabel")
        label.text = "bank_title"
        entry = etree.SubElement(qtibank_tree.find("*/*/*"), "fieldentry")
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
