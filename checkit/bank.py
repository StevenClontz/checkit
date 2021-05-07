from lxml import etree
import os, time, json, zipfile, io, csv
from .outcome import Outcome
from .xml import NS

class Bank():
    def __init__(self, slug=None):
        # read manifest for bank
        xml = etree.parse(os.path.join("banks",slug,"bank.xml")).getroot()
        self.title = xml.find(f"{NS}title").text
        self.homepage = xml.find(f"{NS}homepage").text
        self.slug = slug
        # create each outcome
        self.outcomes = [
            Outcome(
                ele.find(f"{NS}title").text,
                ele.find(f"{NS}slug").text,
                ele.find(f"{NS}description").text,
                ele.find(f"{NS}alignment").text,
                self,
            )
            for ele in xml.find(f"{NS}outcomes").iter(f"{NS}outcome")
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
            "homepage": self.homepage,
            "outcomes": olist,
        }

    def write_json(self,public=False,amount=300,regenerate=False):
        build_path = os.path.join(self.build_path(public,regenerate),f"{self.slug}-bank.json")
        with open(build_path,'w') as f:
            json.dump(self.generate_dict(public,amount,regenerate),f)
        return f"- Bank JSON written to [{build_path}]({self.build_path(public)})"

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
        return f"- Outcome CSV written to [{build_path}]({self.build_path(public)})"

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
                    str(etree.tostring(outcome.qtibank_tree(public,amount,regenerate),
                                            encoding="UTF-8", xml_declaration=True),"UTF-8")
                )
        with open(build_path,'wb') as f:
            f.write(zip_buffer.getvalue())
        return f"- Canvas QTI bank zip written to [{build_path}]({self.build_path(public)})"

    def build(self,public=False,amount=300,regenerate=False,callback=print):
        callback(self.write_json(public,amount,regenerate))
        callback(self.write_qti_zip(public,amount,regenerate))
        callback(self.write_outcome_csv(public,regenerate))