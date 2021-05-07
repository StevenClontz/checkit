from lxml import etree
from lxml import html as lxml_html
from .xml import dict_to_tree, TRANSFORM
import pystache
import urllib
import json

class Exercise:
    def __init__(self, data=None, seed=None, outcome=None):
        self.data = data
        self.seed = seed
        self.outcome = outcome

    def data_tree(self):
        return dict_to_tree(self.data,self.seed)

    def pretext_tree(self):
        renderer = pystache.Renderer()
        xml_string = renderer.render_path(self.outcome.template_filepath(),self.data)
        tree = etree.fromstring(bytes(xml_string, encoding='utf-8'))
        tree.find(".").set('checkit-seed', f"{self.seed:04}")
        tree.find(".").set('checkit-slug', str(self.outcome.slug))
        tree.find(".").set('checkit-title', str(self.outcome.title))

        #remove namespace
        for elem in tree.getiterator():
            elem.tag = etree.QName(elem).localname
        etree.cleanup_namespaces(tree)

        return tree

    def pretext(self):
        return str(etree.tostring(self.pretext_tree(), pretty_print=True), encoding="UTF-8")

    def html_tree(self):
        transform = TRANSFORM["html"]
        tree = transform(self.pretext_tree()).getroot()
        return tree

    def html(self):
        return str(etree.tostring(self.html_tree(),pretty_print=True), 'UTF-8')

    def latex(self):
        transform = TRANSFORM["latex"]
        return str(transform(self.pretext_tree()))

    def qti_tree(self):
        transform = TRANSFORM["qti"]
        tree = transform(self.pretext_tree()).getroot()
        for mattextxml in tree.xpath("//mattextxml"):
            for img in mattextxml.xpath("//img"):
                tex = img.get("data-equation-content")
                src = "https://pi998nv7pc.execute-api.us-east-1.amazonaws.com/production/svg?tex="+urllib.parse.quote(tex)
                img.set("src",src)
            mattext = etree.Element("mattext")
            mattext.attrib['texttype'] = 'text/html'
            mattext.text = lxml_html.tostring(lxml_html.fromstring(etree.tostring(mattextxml.find("*"),pretty_print=True)),pretty_print=True)
            mattextxml.addnext(mattext)
        return tree

    def qti(self):
        return str(etree.tostring(self.qti_tree(),pretty_print=True), 'UTF-8')

    def dict(self):
        return {
            "seed": self.seed,
            "pretext": self.pretext(),
            "html": self.html(),
            "tex": self.latex(),
        }

    def print_preview(self):
        print("Data JSON")
        print("-----------")
        print(json.dumps(self.data))
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
