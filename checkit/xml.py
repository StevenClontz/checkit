from lxml import etree
import os

TRANSFORM = {
    filetype: etree.XSLT(etree.parse(os.path.join("xsl",f"{filetype}.xsl")))
    for filetype in ["html","latex","qti"]
}
NS = "{https://checkit.clontz.org}"

def insert_object_into_element(obj,name,element):
    """
    Inserts Python object into xml element
    """
    if obj is False:
        # skip generating element only when exactly False (not falsy)
        # since xsl:if checks if element exists
        return None
    se = etree.SubElement(element, name)
    if isinstance(obj, list):
        for item in obj:
            insert_object_into_element(item,"item",se)
    elif isinstance(obj, dict):
        for key in obj.keys():
            insert_object_into_element(obj[key],key,se)
    else:
        se.text = str(obj)

def dict_to_tree(data_dict,seed):
    """
    Takes a dictionary of data (typically randomized exercise data)
    and represents it as an XML tree
    """
    data = etree.Element("data")
    data.attrib['seed'] = f"{seed:04}"
    for key in data_dict.keys():
        insert_object_into_element(data_dict[key], key, data)
    return data
