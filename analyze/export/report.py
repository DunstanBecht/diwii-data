#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import tools.connect
import tools.terminals
import tools.selections

    #========= CONSTANTS =================================================#

FOLDER = "../exported/report/"

    #========= EXPORT FUNCTIONS ==========================================#

def count(selection):
    return tools.connect.execute("SELECT COUNT(*) FROM "+selection["expression"])[0][0]

def selections():
    import codes.insee

    f = open(FOLDER+"selections.tex", "w", encoding='utf-8')

    def writeCount(selection, f):
        size = count(selection)
        f.write("\\newcommand\Selection"+selection["kind"].capitalize()+selection["name"]+"{"+str(size)+"}\n")

    for selection in tools.selections.MAIN:
        f.write("\\newcommand\Selection"+selection+"{"+tools.selections.selectionSymbole(selection)[1:-1]+"}\n")
        f.write("\definecolor{Selection"+selection+"}{RGB}{"+", ".join([str(j) for j in tools.selections.MAIN[selection]["color"]])+"}\n")
        f.write("\\newcommand\SelectionDescription"+selection+"{"+tools.selections.MAIN[selection]["legend"]+"}\n")

        if tools.selections.MAIN[selection]["kind"]=="enterprises":
            writeCount(tools.selections.MAIN[selection], f)
        if tools.selections.MAIN[selection]["kind"]=="establishments":
            writeCount(tools.selections.MAIN[selection], f)
            writeCount(tools.selections.groupByEnterprise(tools.selections.MAIN[selection]), f)

    f.write("\\newcommand\FilterA{\n")
    for d in tools.selections.FILTER_A:
        f.write("\item \\textbf{"+d+"} : "+codes.insee.DEPARTMENTS[d]+"\n")
    f.write("}\n")

    f.write("\\newcommand\FilterD{\n")
    for d in tools.selections.FILTER_D:
        f.write("\item \\textbf{"+d+"} : "+codes.insee.descriptionOfActivityCode(d)+"\n")
    f.write("}\n")

    f.write("\\newcommand\FilterE{\n")
    for d in tools.selections.FILTER_E:
        f.write("\item \\textbf{"+d+"} : "+codes.insee.WORKFORCES[d]+" employés\n")
    f.write("}\n")

    f.write("\\newcommand\FilterM{\n")
    for d in tools.selections.FILTER_M:
        f.write("\item \\textbf{"+d+"} : "+codes.insee.descriptionOfActivityCode(d)+"\n")
    f.write("}\n")

    f.write("\\newcommand\FilterP{\n")
    for d in tools.selections.FILTER_P:
        f.write("\item \\textbf{"+d+"} : "+codes.insee.descriptionOfActivityCode(d)+"\n")
    f.write("}\n")

    f.close()

def i2df():
    import codes.i2df

    f = open(FOLDER+"i2df.tex", "w", encoding='utf-8')
    levers = []
    for lever in codes.i2df.LEVERS:
        label_l = "\\textbf{"+lever+"} : "+codes.i2df.LEVERS[lever]
        topics = []
        for topic in codes.i2df.TOPICS_BY_LEVERS[lever]:
            topics.append("& \\textbf{"+lever+str(topic)+"} : "+codes.i2df.TOPICS[lever+str(topic)])

        tex = "\multirow{"+str(len(codes.i2df.TOPICS_BY_LEVERS[lever]))+"}{\linewidth}{"+label_l+"}\n"
        tex += " \\\ \cline{2-2} \n".join(topics)
        levers.append(tex)

    f.write(" \\\ \hline \n".join(levers)+" \\\ ")
    f.close()

def stats():
    A = 0.02
    p = 0.03
    n_E = count(tools.selections.MAIN["E"])
    Z_theo = 1.96
    n_R_theo = int( Z_theo**2*n_E*p*(1-p)/((A*A*n_E)+(Z_theo**2*p*(1-p))) )+1
    n_R_real = count(tools.selections.MAIN["R"])
    Z_real = A/(p*(1-p)*(1/n_R_real-1/n_E))**(1/2)
    import scipy.integrate as integrate
    import math
    def f(x):
        return math.exp(-(1/2)*x**2)/(2*math.pi)**(1/2)
    P = integrate.quad(f, -Z_real, Z_real)[0]
    f = open(FOLDER+"stats.tex", "w", encoding='utf-8')
    f.write("\\newcommand\\nRtheo{"+str(n_R_theo)+"} \n")
    f.write("\\newcommand\Zreal{"+str(int(100*Z_real)/100)+"} \n")
    f.write("\\newcommand\Preal{"+str(int(10000*P)/10000)+"} \n")
    f.write("\\newcommand\Reliability{"+str(int(10000*P)/100)+"} \n")
    f.close()
