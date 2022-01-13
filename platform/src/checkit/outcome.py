from .exercise import Exercise
from lxml import etree
from .xml import xml_boilerplate
from .wrapper import sage
import subprocess, os, json, io, random,datetime
from contextlib import redirect_stdout
from html import escape as escape_html
from tempfile import gettempdir
from .static import read_resource

class Outcome():
    def __init__(self, title=None, slug=None, path=None, description=None, bank=None):
        self.title = title
        self.slug = slug
        self.path = path
        self.description = description
        self.bank = bank
    
    def full_title(self,max_length=None):
        ft = f"{self.slug}: {self.title}"
        if (max_length is not None) and (len(ft)>max_length):
            return ft[:max_length]+"…"
        else:
            return ft

    def template_filepath(self):
        return os.path.join(
            self.path,
            "template.xml"
        )
    
    def template(self):
        with open(self.template_filepath()) as f:
            return f.read()

    def generator_path(self):
        return os.path.join(
            self.path
        )

    def to_dict(self,public=False,amount=300,regenerate=False,randomized=False):
        self.generate_exercises(regenerate)
        exs = self.exercises(public=public,amount=amount,randomized=randomized)
        return {
            "title": self.title,
            "slug": self.slug,
            "description": self.description,
            "template": self.template(),
            "exercises": [e.to_dict() for e in exs],
        }

    def preview_exercises(self):
        temp_dir = gettempdir()
        temp_json = os.path.join(temp_dir,"seeds.json")
        sage(self.generator_path(),temp_json,preview=True)
        with open(temp_json) as f:
            data = json.load(f)['seeds']
        return [Exercise(d["values"],d["seed"],self) for d in data]

    def html_preview(self,pregenerated=False):
        if pregenerated:
            exs = random.sample(self.exercises(),1)
        else:
            exs = self.preview_exercises()
        html = "<h2>Preview:</h2>\n"
        for ex in exs:
            html += ex.html()
            html += "\n"
            html += "<h3>Data</h3>"
            html += "<pre>\n"
            html += escape_html(json.dumps(ex.to_dict(),indent=4))
            html += "</pre>\n"
            html += "\n"
            html += "<h3>SpaTeXt</h3>"
            html += "<pre>\n"
            html += escape_html(ex.spatext())
            html += "</pre>\n"
            html += "\n"
            html += "<h3>HTML</h3>"
            html += "<pre>\n"
            html += escape_html(ex.html())
            html += "</pre>\n"
            html += "<h3>LaTeX</h3>"
            html += "<pre>\n"
            html += escape_html(ex.latex())
            html += "</pre>\n"
        return html
    
    def seeds_json_path(self):
        return os.path.join(self.path,".seeds.json")

    def generate_exercises(self,regenerate=False):
        if not regenerate:
            try:
                self.load_exercises()
                return
            except RuntimeError:
                pass # generation is necessary
        sage(self.generator_path(),self.seeds_json_path(),preview=False)
        self.load_exercises(reload=True)


    def load_exercises(self,reload=False,strict=True):
        if not reload:
            try:
                self._exercises
            except AttributeError:
                pass # load is necessary
        try:
            with open(self.seeds_json_path()) as f:
                data = json.load(f)
            seed_list = data['seeds']
            self._exercises = [Exercise(d["values"],d["seed"],self) for d in seed_list]
            self._generated_on = data['generated_on']
        except FileNotFoundError as e:
            if strict:
                raise RuntimeError("Exercises must be generated before being loaded in strict mode.") from e
    
    def generated_on(self):
        try:
            return self._generated_on
        except AttributeError as e:
            return "(never generated)"
    
    def exercises(self,public=False,amount=300,randomized=False,all=False):
        try:
            if all:
                return self._exercises
            if public:
                exs = self._exercises[:1000]
            else:
                exs = self._exercises[1000:]
            if randomized:
                indices = sorted(random.sample(range(len(exs)),amount))
            else:
                indices = range(amount)
            return [exs[i] for i in indices]
        except AttributeError as e:
            raise RuntimeError("Exercises must be generated/loaded before being requested.") from e

    def canvas_ele(self,public=False,amount=300,regenerate=False,randomized=False,outcomes=None):
        self.generate_exercises(regenerate)
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        ele = etree.fromstring(read_resource("canvas-outcome.xml"))
        CNS = "{"+ele.nsmap[None]+"}"
        obj_bank = ele.find(f"{CNS}objectbank")
        obj_bank.set("ident",f"{self.bank.slug}_{self.slug}")
        label = etree.SubElement(ele.find(f"*/*/{CNS}qtimetadatafield"), "fieldlabel")
        label.text = "bank_title"
        entry = etree.SubElement(ele.find(f"*/*/{CNS}qtimetadatafield"), "fieldentry")
        entry.text = f"CheckIt | {self.bank.title} | {self.slug}: {self.title} (Build {timestamp})"
        for exercise in self.exercises(public=public,amount=amount,randomized=randomized):
            ele.find(f"{CNS}objectbank").append(exercise.canvas_ele())
        return ele
            


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
