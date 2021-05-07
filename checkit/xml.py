
TRANSFORM = {
    filetype: lxml.etree.XSLT(lxml.etree.parse(os.path.join("xsl",f"{filetype}.xsl")))
    for filetype in ["html","latex","qti"]
}
NS = "{https://checkit.clontz.org}"
XSL = "{http://www.w3.org/1999/XSL/Transform}"