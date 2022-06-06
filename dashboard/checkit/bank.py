from lxml import etree
import os, json, datetime, zipfile, shutil, glob
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
    
    def generate_exercises(self,regenerate=False,images=False):
        for o in self.outcomes():
            o.generate_exercises(regenerate=regenerate,images=images)

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

    def build_viewer(self):
        build_path = os.path.join(self.abspath(),"docs")
        if os.path.exists(build_path) and os.path.isdir(build_path):
            shutil.rmtree(build_path)
        os.makedirs(build_path)
        archive = zipfile.ZipFile(static.open_resource("viewer.zip"))
        archive.extractall(build_path)
        # copy assets
        shutil.copytree(self.build_path(),os.path.join("docs","assets"), dirs_exist_ok=True)

    def generated_on(self):
        try:
            with open(os.path.join(self.build_path(),f"bank.json"),'r') as f:
                return json.load(f)["generated_on"]
        except:
            return "(never generated)"
