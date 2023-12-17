#!/usr/bin/python3

# 2023-12 -- rewrite from the totally obsolete perl script

import sys,os

def flatten(tree,outlist):
    for l in tree:
        if isinstance(l,list):
            flatten(l,outlist)
        else:
            outlist.append(l)
    return outlist

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
            par.append("\n%BEGIN()"+filename+")\n")
            par.append(tree)
            par.append("\n%END()"+filename+")\n")

        else:
            sys.exit("unbalanced filename"+l)
        l = l[y+1:]
        x = l.find("\\input{")
    par.append(l)
    return par

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
        x = l.find("%")
        if len(l)==0:    # blank line, new paragraph
            tree.append(" ".join(p))
            tree.append("") # insert blank line to split paragraphs
            p = []
        elif len(l)>1 and l[len(l)-2:]=="\\\\":  # ends with \\ split
            print("line ends with \\\\",l)
            tree.append(" ".join(p))
            tree.append(l)
            p = []
        elif x > 0:
            if l[x-1:x]=="\\":
                #  \% is not a comment
                print("rare \% found")
                p.append(l)
            else: # accumulate into same paragraph
                p.append(l[0:x])
        elif x<0: 
            p.append(l)

        #implicitely, x==0: comments are dropped at the beginning of the file but don't break paragraphs
    tree.append(" ".join(p)) 
    return tree

# Substitutions that make it easier to use the MS Word grammar checker


COMMANDSUB = {
    "~\\cite{" : " [CITE]",
    "~\\ref{" : " [REF]",
     "\\S\\ref{" : " [SECREF]",
     "\\autoref{" : " [AUTOREF]",
     "\\label{" : " [LABEL]",
     "\\emph{" : "SELF",
     "\\texttt{" : "SELF",
     "\\textit{" : "SELF",
     "\\camera{" : "SELF",
     "\\edb{" : "SELF"
}

def ppword(l):
    for c in COMMANDSUB:
        x = l.find(c)
        if x>=0:
            l2 = l[x+len(c):]
            y = l2.find("}")
            if y>0:
                if COMMANDSUB[c]=="SELF":
                    sub = l[0:x]+l2[:y]+l2[y+1:]
                else:
                    sub = l[0:x]+COMMANDSUB[c]+l2[y+1:]
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

F = open(outname,"w")
wasblank = 0
for l in tree:
    if l=="":
        if wasblank == 0:
            F.write("\n")
        wasblank = 1
    else:
        F.write(l+"\n")
        wasblank = 0
