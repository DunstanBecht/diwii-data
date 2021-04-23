#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import tools.connect as connect
import tools.terminals as terminals
import tools.selections as selections
import codes.insee

    #========= EXPORT ====================================================#

print("Tool for maitaining consistency between the script and the report.")

# Colors / froms codes to exported
if True:

    f = open("../exported/report/selections.tex", "w", encoding='utf-8')

    def countEnterprises(enterprises, f):
        size_enterprises = connect.execute("SELECT COUNT(*) FROM "+enterprises["expression"])[0][0]
        f.write("\\newcommand\SelectionEnterprises"+enterprises["name"]+"{"+str(size_enterprises)+"}\n")

    def countEstablishements(establishments, f):
        size_establishments = connect.execute("SELECT COUNT(*) FROM "+establishments["expression"])[0][0]
        f.write("\\newcommand\SelectionEstablishments"+establishments["name"]+"{"+str(size_establishments)+"}\n")

    for selection in selections.MAIN:
        f.write("\\newcommand\Selection"+selection+"{"+selections.selectionSymbole(selection)[1:-1]+"}\n")
        f.write("\definecolor{Selection"+selection+"}{RGB}{"+", ".join([str(j) for j in selections.MAIN[selection]["color"]])+"}\n")
        f.write("\\newcommand\SelectionDescription"+selection+"{"+selections.MAIN[selection]["legend"]+"}\n")

        if selections.MAIN[selection]["kind"]=="enterprises":
            countEnterprises(selections.MAIN[selection], f)
        if selections.MAIN[selection]["kind"]=="establishments":
            countEstablishements(selections.MAIN[selection], f)
            countEnterprises(selections.groupByEnterprise(selections.MAIN[selection]), f)

    f.write("\\newcommand\FilterA{\n")
    for d in selections.FILTER_A:
        f.write("\item "+d+" : "+codes.insee.DEPARTMENTS[d]+"\n")
    f.write("}\n")

    f.write("\\newcommand\FilterD{\n")
    for d in selections.FILTER_D:
        f.write("\item "+d+" : "+codes.insee.descriptionOfActivityCode(d)+"\n")
    f.write("}\n")

    f.write("\\newcommand\FilterE{\n")
    for d in selections.FILTER_E:
        f.write("\item "+d+" : "+codes.insee.WORKFORCES[d]+"\n")
    f.write("}\n")

    f.write("\\newcommand\FilterM{\n")
    for d in selections.FILTER_M:
        f.write("\item "+d+" : "+codes.insee.descriptionOfActivityCode(d)+"\n")
    f.write("}\n")

    f.write("\\newcommand\FilterP{\n")
    for d in selections.FILTER_P:
        f.write("\item "+d+" : "+codes.insee.descriptionOfActivityCode(d)+"\n")
    f.write("}\n")

    f.close()

# I2DF topics / froms codes to exported



terminals.finished()
