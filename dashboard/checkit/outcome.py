from .exercise import Exercise
import os, json, random
from html import escape as escape_html
from .wrapper import sage

class Outcome():
    def __init__(self, title=None, slug=None, path=None, description=None, bank=None):
        self.title = title
        self.slug = slug
        self.relpath = path
        self.description = description
        self.bank = bank
    
    def abspath(self):
        return os.path.join(self.bank.abspath(),self.relpath)
    
    def full_title(self,max_length=None):
        ft = f"{self.slug}: {self.title}"
        if (max_length is not None) and (len(ft)>max_length):
            return ft[:max_length]+"…"
        else:
            return ft

    def template_filepath(self):
        return os.path.join(
            self.abspath(),
            "template.xml"
        )
    
    def template(self):
        with open(self.template_filepath()) as f:
            return f.read()

    def generator_path(self):
        return os.path.join(
            self.abspath(),
            "generator.sage"
        )

    def to_dict(self,regenerate=False):
        self.generate_exercises(regenerate)
        exs = self.exercises()
        return {
            "title": self.title,
            "slug": self.slug,
            "description": self.description,
            "template": self.template(),
            "exercises": [e.to_dict() for e in exs],
        }

    def preview_exercises(self):
        preview_json = os.path.join(self.build_path(),"preview.json")
        sage(self,preview_json,preview=True,images=True)
        with open(os.path.join(preview_json)) as f:
            data = json.load(f)['seeds']
        return [Exercise(d["data"],d["seed"],self) for d in data]

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
            html += "<h3>PreTeXt</h3>"
            html += "<pre>\n"
            html += escape_html(ex.pretext())
            html += "</pre>\n"
        return html

    def build_path(self):
        p = os.path.join(self.bank.build_path(),self.slug,"generated")
        os.makedirs(p, exist_ok=True)
        return p
    
    def seeds_json_path(self):
        return os.path.join(self.build_path(),"seeds.json")

    def generate_exercises(self,regenerate=False,images=False):
        if not regenerate:
            try:
                self.load_exercises()
                return
            except RuntimeError:
                pass # generation is necessary
        sage(self,self.seeds_json_path(),preview=False,images=images)
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
            self._exercises = [Exercise(d["data"],d["seed"],self) for d in seed_list]
            self._generated_on = data['generated_on']
        except FileNotFoundError as e:
            if strict:
                raise RuntimeError("Exercises must be generated before being loaded in strict mode.") from e
    
    def generated_on(self):
        try:
            return self._generated_on
        except AttributeError as e:
            return "(never generated)"
    
    def exercises(self,all=True,amount=300,randomized=False):
        try:
            exs = self._exercises
            if all:
                return exs
            if randomized:
                indices = sorted(random.sample(range(len(exs)),amount))
            else:
                indices = range(amount)
            return [exs[i] for i in indices]
        except AttributeError as e:
            raise RuntimeError("Exercises must be generated/loaded before being requested.") from e
