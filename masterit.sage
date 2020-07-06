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

def insert_object_into_element(obj,name,element):
    if obj is False:
        return None #skip generating element only when exactly False
    se = etree.SubElement(element, name)
    if isinstance(obj, list):
        for item in obj:
            insert_object_into_element(item,"item",se)
    else:
        if isinstance(obj,str):
            se.text = obj
        else:
            se.text = f" {latex(obj)} "

def to_xml(data_dict):
    doc = etree.Element("data")
    for key in data_dict.keys():
        insert_object_into_element(data_dict[key], key, doc)
    return doc

def to_pretext(transform,data_dict):
    doc = to_xml(data_dict)
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
