from lxml import etree

def insert_object_into_element(obj,name,element):
    if obj is False:
        return None #skip generating element only when exactly False (not falsy)
    se = etree.SubElement(element, name)
    if isinstance(obj, list):
        for item in obj:
            insert_object_into_element(item,"item",se)
    else:
        if isinstance(obj,str):
            se.text = obj
        else:
            se.text = f" {latex(obj)} "

def dict_to_tree(data_dict):
    tree = etree.Element("data")
    for key in data_dict.keys():
        insert_object_into_element(data_dict[key], key, tree)
    return tree

class Exercise:
    def __init__(self,name=None,short_name=None,generator=None,template=None,seed=None):
        self.__name = name
        self.__short_name = short_name
        self.__generator = generator
        self.__template = template
        self.reset_seed(seed=seed)

    def reset_seed(self, seed=None):
        if seed is None:
            set_random_seed()
            seed = randrange(0,10000)
        self.__seed = seed

    def data_dict(self):
        set_random_seed(self.__seed)
        return self.__generator()

    def data_tree(self):
        return dict_to_tree(self.data_dict())

    def template(self):
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
        return etree.XSLT(etree.XML(PREFIX+self.__template+SUFFIX))

    def pretext_tree(self):
        transform = self.template()
        return transform(self.data_tree())

    def pretext(self):
        return str(
            etree.tostring(self.pretext_tree()),
            encoding="UTF-8",
        )

    def html(self):
        transform = etree.XSLT(etree.parse("html.xsl"))
        return str(transform(self.pretext_tree()))

    def latex(self):
        transform = etree.XSLT(etree.parse("latex.xsl"))
        return str(transform(self.pretext_tree()))

    def preview(self):
        print("HTML source")
        print("-----------")
        print(self.html())
        print()
        print("LaTeX source")
        print("------------")
        print(self.latex())
        print()
        print("PreTeXt source")
        print("------------")
        print(self.pretext())

    def build_files(self, amount=50, fixed=True):
        import os
        if not os.path.isdir('build'): os.mkdir('build')
        build_path = f"build/{self.__short_name}"
        if not os.path.isdir(build_path): os.mkdir(build_path)
        for count in range(0,amount):
            if fixed:
                self.reset_seed(count)
            else:
                self.reset_seed()
            with open(f'{build_path}/{count:04}.ptx','w') as outfile:
                print(self.pretext(), file=outfile)
            with open(f'{build_path}/{count:04}.tex','w') as outfile:
                print(self.latex(), file=outfile)
            with open(f'{build_path}/{count:04}.html','w') as outfile:
                print(self.html(), file=outfile)
        print(f"Files built successfully at {build_path}")

