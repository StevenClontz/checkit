from lxml import etree

def string_to_transform(template_string):
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

def build_latex(name,generator,template_string,amount=50,fixed=True):
    import os
    if not os.path.isdir('build'): os.mkdir('build')
    build_path = f"build/{name}"
    if not os.path.isdir(build_path): os.mkdir(build_path)
    seed = -1
    for count in range(0,amount):
        if fixed:
            seed += 1
        else:
            seed = randrange(0,10000)
        set_random_seed(seed)
        with open(f'{build_path}/{count:03}.tex','w') as outfile:
            for item in [f"Seed {seed}","",to_latex(to_pretext(string_to_transform(template_string),generator())),""]:
                print(item)
                print(item, file=outfile)

