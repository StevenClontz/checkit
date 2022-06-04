from lxml import etree
from latex2mathml.converter import convert
import pystache
from .static import read_resource

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
        return ele

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
