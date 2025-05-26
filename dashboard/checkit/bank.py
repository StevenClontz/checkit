from lxml import etree
import os, json, datetime, zipfile, shutil
from pathlib import Path
from . import static
from .outcome import Outcome
from .xml import CHECKIT_NS

class Bank():
    def __init__(self, path="."):
        # read manifest for bank
        self._abspath = os.path.abspath(path)
        xml = etree.parse(os.path.join(self.abspath(),"bank.xml")).getroot()
        if xml.get("version") != "0.2":
            raise Exception("ERROR: Bank configuration doesn't match CheckIt version 0.2")
        self.title = xml.find(f"{CHECKIT_NS}title").text
        self.slug = xml.find(f"{CHECKIT_NS}slug").text
        self.url = xml.find(f"{CHECKIT_NS}url").text
        # create each outcome
        self._outcomes = [
            Outcome(
                ele.find(f"{CHECKIT_NS}title").text,
                ele.find(f"{CHECKIT_NS}slug").text,
                ele.find(f"{CHECKIT_NS}path").text,
                ele.find(f"{CHECKIT_NS}description").text,
                self,
            )
            for ele in xml.find(f"{CHECKIT_NS}outcomes").iter(f"{CHECKIT_NS}outcome")
        ]
        for o in self._outcomes:
            o.load_exercises(strict=False)
    
    def abspath(self):
        return self._abspath
    
    def outcomes(self):
        return self._outcomes
    
    def generate_exercises(self,regenerate=False,images=False,amount=1_000):
        for o in self.outcomes():
            print(f"Generating {amount} exercises for outcome {o.slug}")
            o.generate_exercises(regenerate=regenerate,images=images,amount=amount)

    def build_path(self):
        p = os.path.join(self.abspath(),"assets")
        os.makedirs(p, exist_ok=True)
        return p

    def to_dict(self,regenerate=False):
        olist = [o.to_dict(regenerate=regenerate) for o in self.outcomes()]
        return {
            "title": self.title,
            "slug": self.slug,
            "url": self.url,
            "generated_on": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "outcomes": olist,
        }

    def write_json(self,regenerate=False):
        build_path = os.path.join(self.build_path(),f"bank.json")
        with open(build_path,'w') as f:
            json.dump(self.to_dict(regenerate=regenerate),f)

    def build_viewer(self, with_cache=False):
        docs_path = Path(self.abspath()) / "docs"
        if docs_path.exists() and docs_path.is_dir():
            shutil.rmtree(docs_path)
        docs_path.mkdir()
        archive = zipfile.ZipFile(static.open_resource("viewer.zip"))
        archive.extractall(docs_path)
        if with_cache:
            for o in self.outcomes():
                cache_zip = os.path.join(o.build_path(), "cache.zip")
                with zipfile.ZipFile(cache_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    cache_dir = os.path.join(self.build_path(), ".cache", o.generator_hash())
                    for root, _, files in os.walk(cache_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.join(o.generator_hash(), os.path.relpath(file_path, cache_dir))
                            zipf.write(file_path, arcname)
        # copy assets
        shutil.copytree(self.build_path(), docs_path / "assets", dirs_exist_ok=True)
        # remove cache directory if it exists
        cache_dir = docs_path / "assets" / ".cache"
        if cache_dir.exists() and cache_dir.is_dir():
            shutil.rmtree(cache_dir)



    def generated_on(self):
        try:
            with open(os.path.join(self.build_path(),f"bank.json"),'r') as f:
                return json.load(f)["generated_on"]
        except:
            return "(never generated)"
