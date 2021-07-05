from lxml import etree
from lxml import html as lxml_html
from .xml import xsl_transform, xml_boilerplate
from latex2mathml.converter import convert
import pystache
import urllib
import json

def tex_to_mathml(tex):
    return etree.fromstring(convert(tex))

class Exercise:
    def __init__(self, data=None, seed=None, outcome=None):
        self.data = data
        self.seed = seed
        self.outcome = outcome

    def pretext_tree(self):
        renderer = pystache.Renderer()
        xml_string = renderer.render_path(self.outcome.template_filepath(),self.data)
        tree = etree.fromstring(bytes(xml_string, encoding='utf-8'))
        tree.find(".").attrib.pop("version")
        tree.find(".").set('checkit-seed', f"{self.seed:04}")
        tree.find(".").set('checkit-slug', str(self.outcome.slug))
        tree.find(".").set('checkit-title', str(self.outcome.title))

        #remove namespace
        for elem in tree.getiterator():
            if not(type(elem) == etree._Comment):
                elem.tag = etree.QName(elem).localname
        etree.cleanup_namespaces(tree)

        return tree

    def pretext(self):
        return str(etree.tostring(self.pretext_tree(), pretty_print=True), encoding="UTF-8")

    def html_tree(self):
        transform = xsl_transform("html")
        tree = transform(self.pretext_tree()).getroot()
        return tree

    def html(self):
        return str(etree.tostring(self.html_tree(),pretty_print=True), 'utf-8')

    def latex(self):
        transform = xsl_transform("latex")
        return str(transform(self.pretext_tree()))

    def canvas_tree(self):
        transform = xsl_transform("canvas")
        tree = transform(self.pretext_tree()).getroot()
        for mattextxml in tree.xpath("//mattextxml"):
            for img in mattextxml.xpath("//img"):
                tex = img.get("data-equation-content")
                src = "https://canvas.instructure.com/equation_images/"+ \
                    urllib.parse.quote(urllib.parse.quote(tex))
                img.set("src",src)
            mattext = etree.Element("mattext")
            mattext.attrib['texttype'] = 'text/html'
            mattext.text = lxml_html.tostring(lxml_html.fromstring(etree.tostring(mattextxml.find("*"),pretty_print=True)),pretty_print=True)
            mattextxml.addnext(mattext)
        return tree

    def brightspace_tree(self):
        item = xml_boilerplate("brightspace_questiondb_exercise").getroot()
        transform = xsl_transform("brightspace")
        statement_tree = transform(self.pretext_tree().find("statement")).getroot()
        answer_tree = transform(self.pretext_tree().find("answer")).getroot()
        for tree in [statement_tree,answer_tree]:
            for elem in tree.iterfind(".//mathml"):
                tex = elem.get("latex")
                mathml = tex_to_mathml(tex)
                elem.addnext(mathml)
#                parent = elem.getparent()
#                index = parent.index(elem)+1
#                parent.insert(index,mathml)
                del elem
        statement_encoded = lxml_html.tostring(lxml_html.fromstring(etree.tostring(statement_tree,pretty_print=True)),pretty_print=True)
        item.find("presentation/flow/material/mattext").text = statement_encoded
        answer_encoded = lxml_html.tostring(lxml_html.fromstring(etree.tostring(answer_tree,pretty_print=True)),pretty_print=True)
        item.find("answer_key//mattext").text = answer_encoded
        return item

    def moodle_xmle(self):
        transform = xsl_transform("html")
        root = etree.Element("question")
        root.set("type","essay")
        name = etree.SubElement(root,"name")
        name_text = etree.SubElement(name,"text")
        name_text.text = f"{self.outcome.slug} | {self.outcome.title} | ver. {self.seed}"
        statement = etree.SubElement(root,"questiontext")
        statement.set("format","html")
        statement_text = etree.SubElement(statement,"text")
        statement_text.text = etree.tostring(transform(self.pretext_tree().find("statement")))
        answer = etree.SubElement(root,"generalfeedback")
        answer_text = etree.SubElement(answer,"text")
        answer_text.text = etree.tostring(transform(self.pretext_tree().find("answer")))
        attachments = etree.SubElement(root,"attachments")
        attachments.text = "1"
        return root

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
        print(json.dumps(self.data, indent=2))
        print()
        print("PreTeXt source")
        print("------------")
        print(self.pretext())
        print()
        print("HTML source")
        print("-----------")
        print(self.html())
        print()
        print("LaTeX source")
        print("------------")
        print(self.latex())
