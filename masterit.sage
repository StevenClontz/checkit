from lxml import etree

PREFIX = """<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml"/>
    <xsl:template match="/data">
"""
SUFFIX = """
    </xsl:template>
</xsl:stylesheet>
"""

def string_to_transform(template_string):
    return etree.XSLT(etree.XML(PREFIX+template_string+SUFFIX))

def to_pretext(transform,data_dict):
    doc = etree.Element("data")
    for key in data_dict.keys():
        se = etree.SubElement(doc, key)
        se.text = latex(data_dict[key])
    return transform(doc)

def to_string(doc):
    return str(
        etree.tostring(doc),
        encoding="UTF-8",
    )

def to_html(doc):
    transform = etree.XSLT(etree.parse("html.xsl"))
    return str(
        transform(doc)
    )

def to_latex(doc):
    transform = etree.XSLT(etree.parse("latex.xsl"))
    return str(
        transform(doc)
    )
