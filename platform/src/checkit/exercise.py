from lxml import etree
from lxml import html as lxml_html
from .xml import xsl_transform, xml_boilerplate
from .static import read_resource
from latex2mathml.converter import convert
import pystache
import urllib
import json,datetime
from itertools import chain

def tex_to_mathml(tex):
    return etree.fromstring(convert(tex))

class Exercise:
    def __init__(self, data=None, seed=None, outcome=None):
        self.data = data
        self.seed = seed
        self.outcome = outcome

    def spatext_ele(self):
        renderer = pystache.Renderer()
        xml_string = renderer.render_path(self.outcome.template_filepath(),self.data)
        try:
            ele = etree.fromstring(bytes(xml_string, encoding='utf-8'))
        except etree.XMLSyntaxError as e:
            lined_xml = "\n".join([f"{i+1:04d}: {l}" for i,l in enumerate(xml_string.split("\n"))])
            e_text = str(e)+"\n"+lined_xml
            raise Exception(e_text) from e
        # remove comments
        etree.strip_tags(ele,etree.Comment)
        # add checkit metadata
        ele.find(".").set('checkit-seed', f"{self.seed:04}")
        ele.find(".").set('checkit-slug', str(self.outcome.slug))
        ele.find(".").set('checkit-title', str(self.outcome.title))
        return ele
        # #remove namespace
        # for elem in tree.getiterator():
        #     if not(type(elem) == etree._Comment):
        #         elem.tag = etree.QName(elem).localname
        # etree.cleanup_namespaces(tree)

    def spatext(self):
        return str(
            etree.tostring(self.spatext_ele(), pretty_print=True), 
            encoding="UTF-8"
        )

    def html_ele(self,subset='all',consumer='basic'):
        transform = etree.XSLT(etree.fromstring(read_resource("html.xsl")))
        ele = transform(
            self.spatext_ele(),
            subset=f"'{subset}'",
            consumer=f"'{consumer}'",
            ).getroot()
        return ele

    def html(self,subset='all',consumer='basic'):
        return str(etree.tostring(self.html_ele(
            subset=subset,
            consumer=consumer
            ),pretty_print=True), 'utf-8')

    def pretext_ele(self,subset='all',consumer='basic'):
        transform = etree.XSLT(etree.fromstring(read_resource("pretext.xsl")))
        ele = transform(
            self.spatext_ele(),
            subset=f"'{subset}'",
            consumer=f"'{consumer}'",
            ).getroot()
        return ele

    def pretext(self,subset='all',consumer='basic'):
        return str(etree.tostring(self.pretext_ele(
            subset=subset,
            consumer=consumer
            ),pretty_print=True), 'utf-8')

    def latex(self):
        transform = etree.XSLT(etree.fromstring(read_resource("latex.xsl")))
        return str(transform(self.spatext_ele()))

    def to_dict(self):
        return {
            "seed": self.seed,
            "data": self.data,
        }

#     def canvas_ele(self):
#         statement_ele = self.html_ele(subset="statement",consumer="canvas")
#         answer_ele = self.html_ele(subset="answer",consumer="canvas")
#         canvas_ele = etree.fromstring(read_resource("canvas-exercise.xml"))
#         CNS = "{"+canvas_ele.nsmap[None]+"}"
#         timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
#         # set metadata
#         ident = f"{self.outcome.slug}-{self.seed}"
#         canvas_ele.set("ident",ident)
#         title = f"{self.outcome.slug} | {self.outcome.title} | ver. {self.seed} (Build {timestamp})"
#         canvas_ele.set("title",title)
#         # fix equation images
#         img_iter = chain(
#             statement_ele.xpath("//img[@data-latex]"),
#             answer_ele.xpath("//img[@data-latex]"),
#         )
#         for img in img_iter:
#             tex = img.get("data-latex")
#             src = "https://canvas.instructure.com/equation_images/"+ \
#                 urllib.parse.quote(urllib.parse.quote(tex))
#             img.set("src",src)
#         # add timestamp to statement
#         tsp = etree.SubElement(statement_ele,"p")
#         tspsm = etree.SubElement(tsp,"small")
#         tspsm.text = f"(Build ID {timestamp})"
#         tsp.set("style","color:gray;")
#         # insert statement/answer
#         s = canvas_ele.find(f"{CNS}presentation/{CNS}material/{CNS}mattext")
#         s.text = lxml_html.tostring(statement_ele,pretty_print=True)
#         a = canvas_ele.find(f"{CNS}itemfeedback/{CNS}flow_mat/{CNS}material/{CNS}mattext")
#         a.text = lxml_html.tostring(answer_ele,pretty_print=True)
#         return canvas_ele
    
#     def canvas(self):
#         return str(etree.tostring(self.canvas_ele()), 'utf-8')

#     def brightspace_tree(self):
#         item = xml_boilerplate("brightspace_questiondb_exercise").getroot()
#         transform = xsl_transform("brightspace")
#         statement_tree = transform(self.pretext_tree().find("statement")).getroot()
#         answer_tree = transform(self.pretext_tree().find("answer")).getroot()
#         for tree in [statement_tree,answer_tree]:
#             for elem in tree.iterfind(".//mathml"):
#                 tex = elem.get("latex")
#                 mathml = tex_to_mathml(tex)
#                 elem.addnext(mathml)
# #                parent = elem.getparent()
# #                index = parent.index(elem)+1
# #                parent.insert(index,mathml)
#                 del elem
#         statement_encoded = lxml_html.tostring(lxml_html.fromstring(etree.tostring(statement_tree,pretty_print=True)),pretty_print=True)
#         item.find("presentation/flow/material/mattext").text = statement_encoded
#         answer_encoded = lxml_html.tostring(lxml_html.fromstring(etree.tostring(answer_tree,pretty_print=True)),pretty_print=True)
#         item.find("answer_key//mattext").text = answer_encoded
#         return item

#     def moodle_xmle(self):
#         transform = xsl_transform("html")
#         root = etree.Element("question")
#         root.set("type","essay")
#         name = etree.SubElement(root,"name")
#         name_text = etree.SubElement(name,"text")
#         name_text.text = f"{self.outcome.slug} | {self.outcome.title} | ver. {self.seed}"
#         statement = etree.SubElement(root,"questiontext")
#         statement.set("format","html")
#         statement_text = etree.SubElement(statement,"text")
#         statement_text.text = etree.tostring(transform(self.pretext_tree().find("statement")))
#         answer = etree.SubElement(root,"generalfeedback")
#         answer_text = etree.SubElement(answer,"text")
#         answer_text.text = etree.tostring(transform(self.pretext_tree().find("answer")))
#         attachments = etree.SubElement(root,"attachments")
#         attachments.text = "1"
#         return root
