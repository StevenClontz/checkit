import lxml.etree, lxml.html
import os, json, subprocess, time

TRANSFORM = {
    filetype: lxml.etree.XSLT(lxml.etree.parse(os.path.join("xsl",f"{filetype}.xsl")))
    for filetype in ["html","latex","qti"]
}



# XSL Helpers
def insert_object_into_element(obj,name,element):
    """
    Inserts Python object into tree
    """
    if obj is False:
        return None #skip generating element only when exactly False (not falsy)
    se = lxml.etree.SubElement(element, name)
    if isinstance(obj, list):
        for item in obj:
            insert_object_into_element(item,"item",se)
    elif isinstance(obj, dict):
        for key in obj.keys():
            insert_object_into_element(obj[key],key,se)
    else:
        se.text = str(obj)

def dict_to_tree(data_dict):
    """
    Takes a dictionary of data (typically randomized exercise data)
    and represents it as an XML tree
    """
    tree = lxml.etree.Element("data")
    for key in data_dict.keys():
        insert_object_into_element(data_dict[key], key, tree)
    return tree



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

    def build_path(self,public=False):
        if public:
            build_dir = "public"
        else:
            build_dir = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
        return os.path.join("banks",self.slug,"builds",build_dir)

    def generate_dict(self,public=False,amount=300):
        print(f"Generating exercises for {len(self.outcomes)} outcomes...")
        olist = [o.generate_dict(public,amount) for o in self.outcomes]
        print("Exercises successfully generated for all outcomes!")
        return {
            "title": self.title,
            "slug": self.slug,
            "outcomes": olist,
        }

    def build_json(self,public=False,amount=300):
        path = self.build_path(public)
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, f"{self.slug}-bank.json"),'w') as f:
            json.dump(self.generate_dict(public,amount),f)


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

    def generator_filepath(self):
        return os.path.join(
            "banks",
            self.bank.slug,
            "outcomes",
            f"{self.slug}.sage"
        )

    def generate_exercises(self,public=False,amount=300):
        # get sage script to run generator
        script_path = os.path.join("scripts","generator.sage")
        # run script to return JSON output with [amount] seeds
        command = ["sage",script_path,self.generator_filepath(),str(amount)]
        if public:
            command.append("PUBLIC")
            amount = 1000
        else:
            command.append("PRIVATE")
        print(f"Generating {amount} exercises for {self.slug}...")
        # returns json list of exercise objects
        data_json_list = subprocess.run(command,capture_output=True).stdout
        print("Done!")
        data_list = json.loads(data_json_list)
        return [
            Exercise(data["values"],data["seed"],self) \
            for data in data_list
        ]

    def generate_dict(self,public=False,amount=300):
        exercises = self.generate_exercises(public,amount)
        return {
            "title": self.title,
            "slug": self.slug,
            "description": self.description,
            "alignment": self.alignment,
            "exercises": [e.dict() for e in exercises],
        }

    def qtibank_tree(self):
        qtibank_tree = lxml.etree.fromstring("""<?xml version="1.0"?>
<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd">
  <objectbank>
    <qtimetadata>
      <qtimetadatafield/>
    </qtimetadata>
  </objectbank>
</questestinterop>""")
        label = lxml.etree.SubElement(qtibank_tree.find("*/*/*"), "fieldlabel")
        label.text = "bank_title"
        entry = lxml.etree.SubElement(qtibank_tree.find("*/*/*"), "fieldentry")
        entry.text = f"{self.bank.title} -- {self.slug}"
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


class Exercise:
    def __init__(self, data=None, seed=None, outcome=None):
        self.data = data
        self.seed = seed
        self.outcome = outcome

    def data_tree(self):
        return dict_to_tree(self.data)

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
            "qti": self.qti(),
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


#    def build_files(
#        self,
#        build_path="__build__",
#        bank_title="CheckIt Question Bank"
#    ):
#        # provision filesystem
#        if not os.path.isdir(build_path): os.mkdir(build_path)
#        outcome_build_path = os.path.join(build_path, self.__slug)
#        if not os.path.isdir(outcome_build_path): os.mkdir(outcome_build_path)
#        qtibank_build_path = os.path.join(build_path, "qti-bank")
#        if not os.path.isdir(qtibank_build_path): os.mkdir(qtibank_build_path)
#        print(f"Building {outcome_build_path}...")

#        qtibank_tree = self.qtibank_generic_tree(bank_title)

#        for count,seed in enumerate(self.__seeds):
#            exercise = self.list()[count]
#            # build flat files
#            with open(f'{outcome_build_path}/{count:04}.ptx','w') as outfile:
#                print(exercise.pretext(), file=outfile)
#            with open(f'{outcome_build_path}/{count:04}.tex','w') as outfile:
#                print(exercise.latex(), file=outfile)
#            with open(f'{outcome_build_path}/{count:04}.html','w') as outfile:
#                print(exercise.html(), file=outfile)
#            with open(f'{outcome_build_path}/{count:04}.qti','w') as outfile:
#                print(exercise.qti(), file=outfile)
#            # add to qtibank file
#            qtibank_tree.find("*").append(exercise.qti_tree())
#            qtibank_tree.find("*").attrib['ident'] = self.__slug
#        with open(f'{qtibank_build_path}/{self.__slug}.qti','w') as outfile:
#            print(str(lxml.etree.tostring(qtibank_tree, encoding="UTF-8", xml_declaration=True,pretty_print=True),"UTF-8"), file=outfile)
#        print(f"- Files built successfully!")



# Bank building
def build_bank(bank_path, amount=50, fixed=False, public=False):
    config = lxml.etree.parse(os.path.join(bank_path, "__bank__.xml"))
    bank_title = config.find("title").text
    bank_slug = config.find("slug").text
    # build Canvas outcome CSV
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
    # build JSON blob for bank
    bank_json = {
        "title": bank_title,
        "slug": bank_slug,
        "outcomes": [],
    }
    # Canvas chokes on repeated IDs from mult instructors in same institution
    import time; oid_suffix = time.time()
    for n,objective in enumerate(config.xpath("objectives/objective")):
        slug = objective.find("slug").text
        title = objective.find("title").text
        description = objective.find("description").text
        alignment = objective.find("alignment").text
        oldwd=os.getcwd();os.chdir(bank_path)
        load(f"{slug}.sage") # imports `generator` function
        os.chdir(oldwd)
        with open(os.path.join(bank_path, f"{slug}.ptx"),'r') as template_file:
            template = template_file.read()
        outcome = Outcome(
            title=title,
            slug=slug,
            description=description,
            alignment=alignment,
            generator=generator,
            template=template,
            amount=amount,
            fixed=fixed,
            public=public,
        )
        outcome.build_files(
            build_path=os.path.join(bank_path,"__build__"),
            bank_title=bank_title,
        )
        bank_json["outcomes"].append(outcome.dict())
        outcome_csv.append(outcome.outcome_csv_row(n,bank_slug,oid_suffix))
    import csv
    with open(os.path.join(bank_path, "__build__", f"{bank_slug}-canvas-outcomes.csv"),'w') as f:
        csv.writer(f).writerows(outcome_csv)
    print("Canvas outcomes built.")
    import json
    with open(os.path.join(bank_path, "__build__", f"{bank_slug}-bank.json"),'w') as f:
        json.dump(bank_json,f)
    print("JSON blob built.")
    print("Bank build complete!")
