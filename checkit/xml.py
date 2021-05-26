from lxml import etree
import os

TRANSFORM = {
    filetype: etree.XSLT(etree.parse(os.path.join("xsl",f"{filetype}.xsl")))
    for filetype in ["html","latex","canvas"]
}
NS = "{https://checkit.clontz.org}"

