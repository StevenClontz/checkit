from .exercise import Exercise
import os, json, random, hashlib, zipfile, requests, io
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

    def build_path(self):
        p = os.path.join(self.bank.build_path(),self.slug,"generated")
        os.makedirs(p, exist_ok=True)
        return p
    
    def seeds_json_path(self):
        return os.path.join(self.build_path(),"seeds.json")

    def generate_exercises(self,regenerate=False,images=False,amount=1_000):
        if not regenerate:
            try:
                self.load_exercises()
                return
            except RuntimeError:
                pass # generation is necessary
        sage(self,images=images,amount=amount)
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

    def generator_hash(self):
        # Get hash of generator file
        with open(self.generator_path(), 'rb') as f:
            generator_bytes = f.read()
        return hashlib.sha256(generator_bytes).hexdigest()

    def download_cache(self,url):
        # append /assets/{self.slug}/generated/cache.zip to the url
        url = os.path.join(url, "assets", self.slug, "generated", "cache.zip")
        # download cache.zip from url
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Extracting from <{url}>.")
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                zip_ref.extractall(os.path.join(self.bank.build_path(), ".cache"))
        else:
            print(f"Failed to download cache.zip from <{url}>.")
    
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
