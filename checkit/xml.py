from lxml import etree
import os

CHECKIT_NS = "{https://checkit.clontz.org}"

def xsl_transform(filetype):
    return etree.XSLT(etree.parse(os.path.join("xsl",f"{filetype}.xsl")))

def xml_boilerplate(filename):
    return etree.parse(os.path.join("xml",f"{filename}.xml"))