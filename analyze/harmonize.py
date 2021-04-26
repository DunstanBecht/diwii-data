#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import tools.connect
import tools.terminals
import tools.selections
import codes.insee

    #========= EXPORT ====================================================#

print("Tool for maitaining consistency between the code and the report.")
tools.terminals.stopInfo()

if tools.terminals.do("export selection.tex"):

    f = open("../exported/report/selections.tex", "w", encoding='utf-8')

    def countEnterprises(enterprises, f):
        size_enterprises = tools.connect.execute("SELECT COUNT(*) FROM "+enterprises["expression"])[0][0]
        f.write("\\newcommand\SelectionEnterprises"+enterprises["name"]+"{"+str(size_enterprises)+"}\n")

    def countEstablishements(establishments, f):
        size_establishments = tools.connect.execute("SELECT COUNT(*) FROM "+establishments["expression"])[0][0]
        f.write("\\newcommand\SelectionEstablishments"+establishments["name"]+"{"+str(size_establishments)+"}\n")

    for selection in tools.selections.MAIN:
        f.write("\\newcommand\Selection"+selection+"{"+tools.selections.selectionSymbole(selection)[1:-1]+"}\n")
        f.write("\definecolor{Selection"+selection+"}{RGB}{"+", ".join([str(j) for j in tools.selections.MAIN[selection]["color"]])+"}\n")
        f.write("\\newcommand\SelectionDescription"+selection+"{"+tools.selections.MAIN[selection]["legend"]+"}\n")

        if tools.selections.MAIN[selection]["kind"]=="enterprises":
            countEnterprises(tools.selections.MAIN[selection], f)
        if tools.selections.MAIN[selection]["kind"]=="establishments":
            countEstablishements(tools.selections.MAIN[selection], f)
            countEnterprises(tools.selections.groupByEnterprise(tools.selections.MAIN[selection]), f)

    f.write("\\newcommand\FilterA{\n")
    for d in tools.selections.FILTER_A:
        f.write("\item "+d+" : "+codes.insee.DEPARTMENTS[d]+"\n")
    f.write("}\n")

    f.write("\\newcommand\FilterD{\n")
    for d in tools.selections.FILTER_D:
        f.write("\item "+d+" : "+codes.insee.descriptionOfActivityCode(d)+"\n")
    f.write("}\n")

    f.write("\\newcommand\FilterE{\n")
    for d in tools.selections.FILTER_E:
        f.write("\item "+d+" : "+codes.insee.WORKFORCES[d]+"\n")
    f.write("}\n")

    f.write("\\newcommand\FilterM{\n")
    for d in tools.selections.FILTER_M:
        f.write("\item "+d+" : "+codes.insee.descriptionOfActivityCode(d)+"\n")
    f.write("}\n")

    f.write("\\newcommand\FilterP{\n")
    for d in tools.selections.FILTER_P:
        f.write("\item "+d+" : "+codes.insee.descriptionOfActivityCode(d)+"\n")
    f.write("}\n")

    f.close()

# I2DF topics / froms codes to exported

tools.terminals.finished()
