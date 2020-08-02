from lxml import etree
import lxml.html

def insert_object_into_element(obj,name,element):
    if obj is False:
        return None #skip generating element only when exactly False (not falsy)
    se = etree.SubElement(element, name)
    if isinstance(obj, list):
        for item in obj:
            insert_object_into_element(item,"item",se)
    elif isinstance(obj, dict):
        for key in obj.keys():
            insert_object_into_element(obj[key],key,se)
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



import os

def path_relative_from_script(rel_path):
    try:
        dirname = os.path.dirname(__file__)
    except NameError:
        dirname = ""
    return os.path.join(dirname, rel_path)




def mi_vars(*latex_names, random_order=True):
    """
    Given one or more `latex_names` of strings, returns a tuple
    of Sage variables. `random_order` names them so that they appear
    in expressions in a random order.
    """
    stamp = randrange(100000,999999)
    indices = list(range(len(latex_names)))
    if random_order:
        shuffle(indices)
    return (var(f"mi_var_{stamp}_{indices[i]}", latex_name=name) for i, name in enumerate(latex_names))

def shuffled_equation(*terms):
    """
    Represents the equation sum(terms)==0, but with terms shuffled randomly
    to each side.
    """
    new_equation = 0
    for term in terms:
        if choice([True,False]):
            new_equation += (term==0)
        else:
            new_equation += (0==-term)
    return new_equation*choice([-1,1])


class Exercise:
    def __init__(self, name=None, slug=None, generator=None, template=None, seed=None):
        self.__name = name
        self.__slug = slug
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
        tree = transform(self.data_tree()).getroot()
        tree.xpath("/*")[0].attrib['masterit-seed'] = f"{self.__seed:04}"
        tree.xpath("/*")[0].attrib['masterit-slug'] = str(self.__slug)
        tree.xpath("/*")[0].attrib['masterit-name'] = str(self.__name)
        return tree

    def pretext(self):
        return str(etree.tostring(self.pretext_tree()), encoding="UTF-8")

    def html(self):
        transform = etree.XSLT(etree.parse(path_relative_from_script("html.xsl")))
        return str(transform(self.pretext_tree()))

    def latex(self):
        transform = etree.XSLT(etree.parse(path_relative_from_script("latex.xsl")))
        return str(transform(self.pretext_tree()))

    def qti_tree(self):
        transform = etree.XSLT(etree.parse(path_relative_from_script("qti.xsl")))
        tree = transform(self.pretext_tree()).getroot()
        for mattextxml in tree.xpath("//mattextxml"):
            mattext = etree.Element("mattext")
            mattext.attrib['texttype'] = 'text/html'
            mattext.text = lxml.html.tostring(lxml.html.fromstring(etree.tostring(mattextxml.find("*"))))
            mattextxml.addnext(mattext)
        return tree

    def qti(self):
        return str(etree.tostring(self.qti_tree()), 'UTF-8')

    def preview(self):
        print("Data dictionary")
        print("-----------")
        print(self.data_dict())
        print()
        print("Data XML")
        print("-----------")
        print(str(etree.tostring(self.data_tree()), "UTF-8"))
        print()
        print("HTML source")
        print("-----------")
        print(self.html())
        print()
        print("LaTeX source")
        print("------------")
        print(self.latex())
        print()
        print("QTI source")
        print("------------")
        print(self.qti())
        print()
        print("PreTeXt source")
        print("------------")
        print(self.pretext())

    def build_files(self, amount=50, fixed=True, build_path="build"):
        if not os.path.isdir(build_path): os.mkdir(build_path)
        obj_build_path = os.path.join(build_path, self.__slug)
        if not os.path.isdir(obj_build_path): os.mkdir(obj_build_path)
        bank_build_path = os.path.join(build_path, "qti-bank")
        if not os.path.isdir(bank_build_path): os.mkdir(bank_build_path)
        bank_tree = etree.fromstring("""<?xml version="1.0"?>
<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd">
  <objectbank>
    <qtimetadata>
      <qtimetadatafield/>
    </qtimetadata>
  </objectbank>
</questestinterop>""")
        label = etree.SubElement(bank_tree.find("*/*/*"), "fieldlabel")
        label.text = "bank_title"
        entry = etree.SubElement(bank_tree.find("*/*/*"), "fieldentry")
        entry.text = f"MasterIt Question Bank -- {self.__slug}"
        for count in range(0,amount):
            if fixed:
                self.reset_seed(count)
            else:
                self.reset_seed()
            # build flat files
            with open(f'{obj_build_path}/{count:04}.ptx','w') as outfile:
                print(self.pretext(), file=outfile)
            with open(f'{obj_build_path}/{count:04}.tex','w') as outfile:
                print(self.latex(), file=outfile)
            with open(f'{obj_build_path}/{count:04}.html','w') as outfile:
                print(self.html(), file=outfile)
            with open(f'{obj_build_path}/{count:04}.qti','w') as outfile:
                print(self.qti(), file=outfile)
            # add to bank file
            bank_tree.find("*").append(self.qti_tree())
            bank_tree.find("*").attrib['ident'] = self.__slug
        with open(f'{bank_build_path}/{self.__slug}.qti','w') as outfile:
            print(str(etree.tostring(bank_tree, encoding="UTF-8", xml_declaration=True),"UTF-8"), file=outfile)
        print(f"Files built successfully at {obj_build_path}")



def main(library_path):
    config = etree.parse(os.path.join(library_path, "masterit.xml"))
    for objective in config.xpath("/masterit/objectives/objective"):
        slug = objective.find("slug").text
        load(os.path.join(library_path, f"{slug}.sage")) # imports `generator` function
        with open(os.path.join(library_path, f"{slug}.ptx"),'r') as template_file:
            template = template_file.read()
        Exercise(
            name=objective.find("title").text,
            slug=slug,
            generator=generator,
            template=template
        ).build_files(
            build_path=os.path.join(library_path,"build")
        )

if (__name__ == "__main__") and ("repl/" not in sys.argv[0]): #hax
    main(sys.argv[1])