#!/usr/bin/python3

###################################
# Linearlize all latex files into a single file. 
#  - strips lines that start with %
#  - paragraph on a single line (necessary for including in word)
#
# Usage 
#   ./scripts/lin.py  <top-file.tex> [OPTION]
#  
# Base mode - when there are no option
#  - generate a file arxiv.tex suitable for upload into arxiv, TOCS, etc
#  - note: does not inline the bibliography
#  - note: does not renumber the figures
#  - normally called by the target "make arxiv"

# Mode #2:  OPTION = word  
#  - applies the logic of base mode
#  - further remove Citations, labels and refs
#  - output file is called latexforword.txt
#  - normally called by the target "make spell"

# Revision history
#  - 2023-12 -- rewrite from the totally obsolete perl script

import sys,os

# global
inbody = 0

# flattens tree of strings into a list of strings
def flatten(tree,outlist):
    for l in tree:
        if isinstance(l,list):
            flatten(l,outlist)
        else:
            outlist.append(l)
    return outlist

# called to expand \\input{filename} (if present) during parsing
def expandlineinput(l):
    par = []
    x = l.find("\\input{")
    while x>=0:
        if x>0:
            par.append(l[0:x])
        l = l[x+len("\\input{"):]
        y = l.find("}")
        if y>0:
            filename = l[0:y]
            print("Expanding input",filename)
            tree = readfile(filename)
            tree = [expandlineinput(l) for l in tree]
            par.append("%BEGIN("+filename+")")
            par.append(tree)
            par.append("%END("+filename+")")

        else:
            sys.exit("unbalanced filename"+l)
        l = l[y+1:]
        x = l.find("\\input{")
    par.append(l)
    return par

# 
def removecomments(l):
    x = l.find("%")
    if x<0:
        return l
    if l[x-1:x]=="\\":
        #  \% is not a comment
        return l[0:x+1] + removecomments(l[x+1:])
    return l[0:x]


# Read and parse latex input file, applying the following logic
#  - remove all comments
#  - strip leading and trailing blanks
#  - merge consective non-blank lines (before removal of comments) into a single line that corresponds to the paragraph
#  - split paragraphs if lines ends with  \\

def readfile(filename):
    if os.path.isfile(filename):
       print ("READING FILENAME: ",filename)
    elif os.path.isfile(filename+".tex"):
        print ("READING FILENAME: ",filename,"(.tex)")
        filename = filename+".tex"
    else:
        sys.exit("could not find file ",filaname)

    lines = [line.strip().lstrip() for line in open(filename)]
    p = []
    tree = []
    for l in lines:
        if len(l)==0:    # blank line, new paragraph
            tree.append(" ".join(p))
            tree.append("") # insert blank line to split paragraphs
            p = []
        else:
            l = removecomments(l)
            if len(l)>1 and l[len(l)-2:]=="\\\\":  # ends with \\ split
                print("line ends with \\\\",l)
                tree.append(" ".join(p))
                tree.append(l)
                p = []
            else: 
                p.append(l)

    tree.append(" ".join(p)) 
    return tree






# Substitutions that make it easier to use the MS Word grammar checker
COMMANDSUB = {
    "~\\cite{" : " [CITE]",
    "~\\ref{" : " [REF]",
     "\\S\\ref{" : " [SECREF]",
     "\\autoref{" : "[AUTOREF]",
     "\\label{" : " [LABEL]",
     "\\includegraphics{" : " [GRAPHICS]",

     "\\emph{" : "SELF",
     "\\texttt{" : "SELF",
     "\\textit{" : "SELF",
     "\\textbf{" : "SELF",
     "\\camera{" : "SELF",
     "\\caption{" : "SELF",
     "\\textsf{" : "CAPS",
     "\\section{" : "CAPS",
     "\\edb{" : "SELF",
     "\\myparagraph{" : "["+"SELF"+":]",
     "\\new{" : "SELF",
     "\\system{": "SYSTEM",
     #paper-specific
     "\\td{" : "TD",
     "\\framework{" : "FRAMEWORK",
     "\\sharedmem{" : "regular memory"

}

KEYWORDSUB = {
    "\\eg" : "e.g.,",
    "\\ie" : "i.e.,",
    "\\etc" : "etc.",
    "\\&" : "&",
    # paper-specific
    "\\overcommitname" : "informed overcommitment",
    "\\Overcommitname" : "Informed overcommitment",
    "\\system" : "SYSTEM"
    # Arm architecture
}


## custom macros

CUSTOMMACROS = {}
## one day, will figure out regex in python
def findcustommacros(l):
    global CUSTOMMACROS
    x = l.find("\\newcommand{")
    if x>=0:
        l2 = l[x+len("\\newcommand{"):]
        x2 = l2.find("}{")
        if x2>0:
            key = l2[0:x2]
            l3 = l2[x2+2:]
            for c in ['\\textsc{','\\textsf{']:
                x3 = l3.find(c)
                if x3==0:
                    x4 = l3.find("}")
                    if x4>0:
                        value = l3[len(c):x4]
                        x5 = value.find("\\xspace")
                        if x5>0:
                            value = value[0:x4]
                        if key in KEYWORDSUB:
                            print("HARD MACRO |"+key+"|"+value+"|")
                        else:
                            print("CUSTOM MACROS |"+key+"|"+value+"|"+value.upper())
                            CUSTOMMACROS[key+"{}"] = value.upper()
        return findcustommacros(l[x+len("\\newcommand{"):])
    else: 
        return l




def ppword(l):
    global inbody
    global CUSTOMMACROS
    if inbody == 0:
        l = findcustommacros(l)
        for c in ["\\title","\\begin{document}"]:
            x = l.find(c)
            if x>=0:
                inbody = 1
                return ppword(l)
        return ""

    for cc in CUSTOMMACROS:
        x = l.find(cc)
        if x>=0:
            sub = l[0:x]+CUSTOMMACROS[cc]+l[x+len(cc):]
            return ppword(sub)
   
    for c in COMMANDSUB:
        x = l.find(c)
        if x>=0:
            l2 = l[x+len(c):]
            y = l2.find("}")
            if y>=0:
                pos = COMMANDSUB[c].find("SELF")
                if COMMANDSUB[c]=="CAPS":
                    sub = l[0:x]+ l2[:y]+l2[y+1:]
                elif pos>=0:
                    prefix = COMMANDSUB[c][:pos]
                    postfix = COMMANDSUB[c][pos+4:]
                    sub = l[0:x]+prefix + l2[:y]+ postfix +l2[y+1:]
                else:
                    sub = l[0:x]+COMMANDSUB[c]+l2[y+1:]
                return ppword(sub)

    for cc in KEYWORDSUB: 
        c2 = cc+"{}"
        for c in [c2,cc]: 
            x = l.find(c)
            if x>=0:
                sub = l[0:x]+KEYWORDSUB[cc]+l[x+len(c):]
                return ppword(sub)
    return l


main = sys.argv[1]
tree = readfile(main)
tree = [expandlineinput(l) for l in tree]
tree = flatten(tree,[])


if len(sys.argv)>2 and sys.argv[2]=="word":
    tree = [ppword(l) for l in tree]
    outname = "latexforword.txt"
else: 
    outname = "arxiv.tex"

print("Generating "+outname)
F = open(outname,"w")

wasblank = 0
for l in tree:
    while len(l)>=1 and l[0:1]==" ":
        l = l[1:]

    if l=="":
        if wasblank == 0:
            F.write("\n")
        wasblank = 1
    else:
        F.write(l+"\n")
        wasblank = 0
