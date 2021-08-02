from .exercise import Exercise
from lxml import etree
from .xml import xml_boilerplate
import subprocess, os, json

class Outcome():
    def __init__(self, title=None, slug=None, description=None, bank=None):
        self.title = title
        self.slug = slug
        self.description = description
        self.bank = bank

    def template_filepath(self):
        return os.path.join(
            "banks",
            self.bank.slug,
            "outcomes",
            f"{self.slug}.xml"
        )

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
            "exercises": [e.dict() for e in exercises],
        }

    def canvas_tree(self,public=False,amount=300,regenerate=False):
        tree = etree.fromstring(f"""<?xml version="1.0"?>
          <questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd">
            <objectbank ident="{self.bank.slug}_{self.slug}">
              <qtimetadata>
                <qtimetadatafield/>
              </qtimetadata>
            </objectbank>
          </questestinterop>""")
        label = etree.SubElement(tree.find("*/*/*"), "fieldlabel")
        label.text = "bank_title"
        entry = etree.SubElement(tree.find("*/*/*"), "fieldentry")
        entry.text = f"{self.bank.title} | {self.slug}: {self.title}"
        for exercise in self.generate_exercises(public,amount,regenerate):
            tree.find("*").append(exercise.canvas_tree())
        return tree

    def brightspace_tree(self,public=False,amount=300,regenerate=False):
        tree = xml_boilerplate("brightspace_questiondb_outcome")
        tree.getroot().set("title", f"{self.bank.title} | {self.slug}: {self.title}")
        tree.find("presentation_material//mattext").text = self.description
        for exercise in self.generate_exercises(public,amount,regenerate):
            tree.getroot().append(exercise.brightspace_tree())
        return tree

    def moodle_xmle(self,public=False,amount=300,regenerate=False):
        root = etree.Element("quiz")
        header = etree.SubElement(root,"question")
        header.set("type","category")
        category = etree.SubElement(header,"category")
        category_text = etree.SubElement(category,"text")
        category_text.text = f"$course$/top/checkit/{self.bank.slug}/{self.slug}"
        info = etree.SubElement(header,"info")
        info_text = etree.SubElement(info,"text")
        info_text.text = f"{self.slug} | {self.title}"
        root.append(header)
        for exercise in self.generate_exercises(public,amount,regenerate):
            root.append(exercise.moodle_xmle())
        return root

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

    def print_preview(self,callback=print):
        ex = self.generate_exercises(amount=1,regenerate=True,save=False)[0]
        callback("<h2>Preview:</h2>")
        callback(ex.html())
        ex.print_preview()
