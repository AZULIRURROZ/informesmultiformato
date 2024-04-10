import sys 
import re 
import imp
import mimetypes
from datetime import datetime
try:
    imp.find_module('pyperclip')
    import pyperclip
    pasting = True
except ImportError:
    pasting = False

class doc_vidOrHtml:
    def __init__(self, title, subtitle, date, sites, tags, edits, description, age):
        self.title = title
        self.subtitle = subtitle
        self.date = date
        self.sites = sites
        self.tags = tags
        self.edits = edits
        self.description = description
        self.age = age

class doc_desc:
    def __init__(self, subtitle, description):
        self.subtitle = subtitle
        self.description = description

def fun_vid(fn_file):
    pro_edits = []
    pro_tags = []
    pro_subtitle = []

    if ("__" in fn_file):
        pro_date = fn_file.split("__")[0].replace("+"," + ")
        if ("/" in fn_file):
            pro_date = pro_date.rsplit('/', 1)[1]
        pro_rest = fn_file.split("__",1)[1]
        pro_sites = pro_rest.split("+")
        if ( pro_rest.split(",")[0] != pro_rest):
            pro_tags = ["edit"]
            pro_pretags = pro_rest.split(",", 1)[1]
            # if ("k" in pro_pretags):
            #    pro_tags.append("comprimido")
            if ("r" in pro_pretags):
                pro_edits.append("recorte")
            if ("c" in pro_pretags):
                pro_edits.append("censura")
    else:
        pro_date = fn_file.split("+")[0]
        pro_rest = fn_file.split("+",1)[1]
        pro_sites = pro_rest.split("+")
        if ( ("EDITADO" in pro_rest) or ("YE")):
            pro_tags = ["edit"]
            # if ( "YC" in pro_rest ):
            #    pro_tags.append("comprimido")
    
    pro_date = pro_date.replace("_"," ").replace(".",":")
    pro_sites = " + ".join(pro_sites).rsplit('.', 1)[0]
    pro_subtitle = pro_subtitle+[sub.replace('(', '').replace(')', '') for sub in (re.findall(r'\(.+?\)', pro_sites))]
    pro_sites = re.sub(r'\(.+?\)', '', pro_sites).replace('()', '').split(",",1)[0].split(" + ")
    pro_age = -1
    if (len(re.findall(r'era [^,]*?(\d+)', fn_file, re.I)) > 0):
        pro_age = [int(n) for n in re.findall(r'era [^,]*?(\d+)', fn_file, re.I)][0]
    
    return doc_vidOrHtml([], pro_subtitle, [pro_date], pro_sites, pro_tags, pro_edits, [], pro_age)
    
def fun_desc(fn_file):
    pro_description = []
    pro_subtitle = []
    with open(fn_file, "r") as pro_read:
        pro_first = pro_read.readline()
        if (len(pro_first) > 0 ):
            if ("#" in pro_first):
                pro_subtitle = pro_subtitle+[pro_first.replace("# ","").replace("#","").replace("\n","")]
                pro_description = [pro_read.read()]
            else:
                pro_description = [pro_first+pro_read.read()]
    return doc_desc(pro_subtitle, pro_description)


def fun_tex(fn_file):
    pro_url = []
    pro_date = []
    pro_title = []
    pro_tags = []
    pro_description = []
    with open(fn_file) as pro_file:
        for i, line in enumerate(pro_file):
            if ("url: " in line): 
                pro_url = [line.split("url: ")[1].split(" ")[0]]
            if ("saved date: " in line and "GMT" in line):
                pro_date = datetime.strptime(line.split("saved date: ", 1)[1].split(" GMT")[0], '%a %b %d %Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            if i == 5:
                break
        pro_html = pro_file.read()
        pro_title = re.findall('<title>(.*)</title>\n', pro_html)
        pro_tags.insert(0, "la página")
        pro_subtitle = ""
        pro_presubtitle = [
            [re.findall(r'<\/div> <h1 class=svelte-.*>(.+?)<\/h1>', pro_html), re.findall(r'margin-top:2%>(.+?)<\/div><\/div><\/div>', pro_html, re.MULTILINE|re.DOTALL), "el topic"],
            [re.findall(r'name id=voxTitle>(.+?)<\/h1>', pro_html),re.findall(r'<div class=voxDescription itemprop=articleBody id=voxContent>(.+?)<\/div><\/header><\/article>', pro_html), "el vox"]
            ]
        for i in range(len(pro_presubtitle)):
            if (len(pro_presubtitle[i][0]) > 0):
                pro_tags.insert(0, pro_presubtitle[i][2])
                pro_subtitle = pro_presubtitle[i][0]
                pro_description = pro_presubtitle[i][1]
                if (i==0 and (("CPCU" in pro_html) or ("combinadorufftopico" in pro_html))):
                    pro_tags.insert(1, "cpcu")
                break
    
    return doc_vidOrHtml(pro_title, pro_subtitle, [pro_date], pro_url, pro_tags, [], pro_description, -1)
        

def fun_get(pro_arguments):
    fn_attrb = doc_vidOrHtml([], [], [], [], [], [], [], -1)
    for i in range(len(pro_arguments)):
        if (".html" in pro_arguments[i]):
            fn_attrb = fun_tex(pro_arguments[i])
            fn_mode = True
        else:
            fn_mode = False
            fn_subattrb = fun_vid(pro_arguments[i])
            fn_attrb.subtitle = fn_attrb.subtitle + fn_subattrb.subtitle
            fn_attrb.date = fn_attrb.date + fn_subattrb.date
            fn_attrb.sites = fn_attrb.sites + fn_subattrb.sites
            fn_attrb.tags = fn_attrb.tags + fn_subattrb.tags
            fn_attrb.edits = fn_attrb.edits + fn_subattrb.edits
            fn_attrb.description = fn_attrb.description + fn_subattrb.description
            fn_attrb.age = fn_subattrb.age
            if mimetypes.guess_type(pro_arguments[i])[0] == 'text/plain':
                fn_subattrbDesc = fun_desc(pro_arguments[i])
                fn_attrb.description = fn_attrb.description+fn_subattrbDesc.description
                fn_attrb.subtitle = fn_attrb.subtitle+fn_subattrbDesc.subtitle
            fn_subattrb = fn_subattrb
    fn_attrb.edits = list( dict.fromkeys(fn_attrb.edits) )
    fn_attrb.sites = " + ".join( list( dict.fromkeys(fn_attrb.sites) ) )
    fn_attrb.date = " + ".join( list( dict.fromkeys(fn_attrb.date) ) )
    fn_attrb.title = " + ".join( list( dict.fromkeys(fn_attrb.title) ) )
    fn_attrb.subtitle = " + ".join( list( dict.fromkeys(fn_attrb.subtitle) ) )
    fn_attrb.description = "".join( list( dict.fromkeys(fn_attrb.description) ) )

    fn_simple = "🔗 " + fn_attrb.sites
    fn_short = fn_attrb.sites
    fn_simple += "\n📅 " + "".join(fn_attrb.date)
    fn_short += " | " + "".join(fn_attrb.date)
    if (len(fn_attrb.title) > 0):
        fn_simple += "\n🧾 "+fn_attrb.title
        fn_short = fn_attrb.title+" | " + fn_short
    if (fn_attrb.age != -1):
        fn_simple += " #AnomItmetishtuMulticoloresInvertidosEra"+str(fn_attrb.age)
        fn_short += " | #AnomItmetishtuMulticoloresInvertidosEra"+str(fn_attrb.age)
        if (fn_attrb.age == 11):
            fn_simple += " #ArchivoClonicoSoñadorIII"
            fn_short += " #ArchivoClonicoSoñadorIII"
    if ("edit" in fn_attrb.tags):
        if (len(fn_attrb.edits) > 0):
            pro_tags = "Editado: "+(", ".join(fn_attrb.edits))
        else:
            pro_tags = "Editado "
        fn_simple += "\n✏️ " + pro_tags
        fn_short += " | " + pro_tags
    if (len(fn_attrb.subtitle) > 0 or len(fn_attrb.description) > 0):
        fn_simple += "\n\n📜 "
    if (len(fn_attrb.subtitle) > 0):
        fn_simple += fn_attrb.subtitle+"\n"
        fn_short = fn_attrb.subtitle + " | " + fn_short
    if (len(fn_attrb.description) > 0):
        fn_simple += fn_attrb.description
        fn_short += "\n\n" + fn_attrb.description
    
    fn_return = fn_simple
    if (fn_mode == False):
        fn_return += "\n\n" + fn_short
    else:
        fn_return += "\n\n📄 Copia de "+fn_attrb.tags[0]+" guardada en .html"
        if ("cpcu" in fn_attrb.tags):
            fn_return += "\n📑 Páginas de comentarios combinadas en una"
    return (fn_return)
    

pro_arguments = sys.argv 
if ("app.py" in pro_arguments[0]): 
    pro_arguments.pop(0) 
pro_typeVideo = ""
pro_typeHtml = ""
pro_typeErrors = []
if (len(pro_arguments)>0):
    if len(pro_arguments) == 1:
        print("\nHola! Si todo sale bien recibirás la descripción de ",len(pro_arguments)," archivo.\n")
    else:
        print("\nHola! Si todo sale bien recibirás la descripción de ",len(pro_arguments)," archivos.\n")
else:
    print("\nHola! No ingresaste ningún archivo. La dejamos acá, ok?\n")
    exit(1)
for i in range(len(pro_arguments)):
    try:
        if (".html" in pro_arguments[i]):
            pro_typeHtml = pro_typeHtml+fun_get([pro_arguments[i]])+"\n"
        else:
            pro_typeVideo = pro_typeVideo+fun_get(pro_arguments)+"\n"
            break
    except Exception as error:
        pro_typeErrors.append(pro_arguments[i]+": "+repr(error))
if (len(pro_typeVideo) > 0):
    print(pro_typeVideo+pro_typeHtml)
    if (pasting):
        pyperclip.copy(pro_typeVideo+pro_typeHtml)
        pyperclip.paste()
    print("\nChau! Ahí está el texto de descripción que se pudo encontrar.\n")
elif (len(pro_typeErrors) > 0):
    print(pro_typeErrors)
    print("\nChau! Hubo un error y posiblemente se deba a nombres incorrectos.\n")

exit(0)
