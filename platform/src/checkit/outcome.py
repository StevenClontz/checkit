from .exercise import Exercise
from lxml import etree
from .xml import xml_boilerplate
from .wrapper import sage
import subprocess, os, json
import io
from contextlib import redirect_stdout
from html import escape as escape_html
from tempfile import gettempdir

class Outcome():
    def __init__(self, title=None, slug=None, path=None, description=None, bank=None):
        self.title = title
        self.slug = slug
        self.path = path
        self.description = description
        self.bank = bank

    def template_filepath(self):
        return os.path.join(
            self.path,
            "template.xml"
        )

    def generator_path(self):
        return os.path.join(
            self.path
        )

    # def generate_dict(self,public=False,amount=300,regenerate=False):
    #     exercises = self.generate_exercises(public,amount,regenerate)
    #     return {
    #         "title": self.title,
    #         "slug": self.slug,
    #         "description": self.description,
    #         "exercises": [e.dict() for e in exercises],
    #     }

    def preview_exercise(self):
        temp_dir = gettempdir()
        temp_json = os.path.join(temp_dir,"seeds.json")
        sage(self.generator_path(),temp_json,preview=True)
        with open(temp_json) as f:
            data = json.load(f)[0]
        return Exercise(data["values"],data["seed"],self)

    def HTML_preview(self):
        ex = self.preview_exercise()
        html = "<h2>Preview:</h2>\n"
        # html += ex.html()
        html += "\n"
        html += "<pre>\n"
        # f = io.StringIO()
        # with redirect_stdout(f):
        #     ex.print_preview()
        # html += escape_html(f.getvalue())
        html += escape_html(ex.spatext())
        html += "</pre>\n"
        return html
    
    def seeds_json_path(self):
        return os.path.join(self.path,".seeds.json")

    def generate_exercises(self):
        sage(self.generator_path(),self.seeds_json_path(),preview=False)
        with open(self.seeds_json_path()) as f:
            data_list = json.load(f)
        self._exercises = [Exercise(d["values"],d["seed"],self) for d in data_list]
    
    def exercises(self):
        try:
            return self._exercises
        except:
            self.generate_exercises()
            return self._exercises
        

            


    # def canvas_tree(self,public=False,amount=300,regenerate=False):
    #     tree = etree.fromstring(f"""<?xml version="1.0"?>
    #       <questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2"
    #         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    #         xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd">
    #         <objectbank ident="{self.bank.slug}_{self.slug}">
    #           <qtimetadata>
    #             <qtimetadatafield/>
    #           </qtimetadata>
    #         </objectbank>
    #       </questestinterop>""")
    #     label = etree.SubElement(tree.find("*/*/*"), "fieldlabel")
    #     label.text = "bank_title"
    #     entry = etree.SubElement(tree.find("*/*/*"), "fieldentry")
    #     entry.text = f"{self.bank.title} | {self.slug}: {self.title}"
    #     for exercise in self.generate_exercises(public,amount,regenerate):
    #         tree.find("*").append(exercise.canvas_tree())
    #     return tree

    # def brightspace_tree(self,public=False,amount=300,regenerate=False):
    #     tree = xml_boilerplate("brightspace_questiondb_outcome")
    #     tree.getroot().set("title", f"{self.bank.title} | {self.slug}: {self.title}")
    #     tree.find("presentation_material//mattext").text = self.description
    #     for exercise in self.generate_exercises(public,amount,regenerate):
    #         tree.getroot().append(exercise.brightspace_tree())
    #     return tree

    # def moodle_xmle(self,public=False,amount=300,regenerate=False):
    #     root = etree.Element("quiz")
    #     header = etree.SubElement(root,"question")
    #     header.set("type","category")
    #     category = etree.SubElement(header,"category")
    #     category_text = etree.SubElement(category,"text")
    #     category_text.text = f"$course$/top/checkit/{self.bank.slug}/{self.slug}"
    #     info = etree.SubElement(header,"info")
    #     info_text = etree.SubElement(info,"text")
    #     info_text.text = f"{self.slug} | {self.title}"
    #     root.append(header)
    #     for exercise in self.generate_exercises(public,amount,regenerate):
    #         root.append(exercise.moodle_xmle())
    #     return root

    # def csv_row(self,count,oid_suffix):
    #     return [
    #         f"checkit_{self.bank.slug}_{count:02}_{self.slug}_{oid_suffix:06}",
    #         "outcome",
    #         f"{count:02}-{self.slug}: {self.title}",
    #         "",
    #         self.slug,
    #         "n_mastery",
    #         "2",
    #         "3",
    #         "4",
    #         "Exceeds Mastery",
    #         "3",
    #         "Meets Mastery",
    #         "2",
    #         "Near Mastery",
    #         "1",
    #         "Well Below Mastery",
    #         "0",
    #         "Insufficient Work to Assess",
    #     ]
