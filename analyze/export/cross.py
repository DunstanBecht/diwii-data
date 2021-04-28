#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import matplotlib.pyplot as plt

import tools.connect
import codes.i2df
import tools.export
import export.survey
import tools.selections

    #========= CONSTANTS =================================================#

FOLDER = "../exported/cross/"

    #========= EXPORT FUNCTIONS ==========================================#

def figureMaturityByLeverByDepartment(lever):
    s1 = tools.selections.groupByEnterprise(tools.selections.MAIN["R"])
    s2 = tools.selections.MAIN["I"]
    tools.export.inform([s1,  s2])
    assert tools.selections.checkKind([s1,  s2])=="enterprises"
    name = tools.selections.FILTER_A
    #insee
    data_1 = [export.survey.pourcentage("answer4"+lever.lower(), tools.selections.DEPARTMENTS_1[tools.selections.FILTER_A[i]]) for i in range(len(tools.selections.FILTER_A))]
    # aif
    data_2 = []
    for i in range(len(tools.selections.FILTER_A)):
        request = ("SELECT "+", ".join(["AVG("+lever+str(topic)+")" for topic in codes.i2df.TOPICS_BY_LEVERS[lever]])+"\n"
                   "FROM "+tools.selections.DEPARTMENTS_2[tools.selections.FILTER_A[i]]["expression"]+"\n")
        answer = tools.connect.execute(request)[0]
        data_2.append(10*sum(filter(None, answer))/len(answer))
    data = [data_1, data_2]
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = int(data[i][j]*10)/10
    fig, x = tools.export.templateFigure([s1, s2], data, (9,3.5))
    plt.ylim(0, 119)
    plt.title("Maturité : "+codes.i2df.LEVERS[lever.upper()])
    fig.subplots_adjust(left=0.09, right=0.99, top=0.9, bottom=0.12)
    plt.xlabel("Département")
    plt.ylabel("Maturité dans le levier "+lever.upper())
    plt.xticks(x, name, rotation = 0)
    plt.savefig(FOLDER+"by_department/lever"+lever.upper()+"/"+s1["name"]+"_with_"+s2["name"]+".pdf")

def figureMaturityByLeverByWorforce(lever):
    s1 = tools.selections.MAIN["R"]
    s2 = tools.selections.MAIN["I"]
    tools.export.inform([s1,  s2])

    name = ["+ de 50 employés", "- de 50 employés"]
    #insee
    data_1 = [export.survey.pourcentage("answer4"+lever.lower(), tools.selections.MAIN["X"]),
              export.survey.pourcentage("answer4"+lever.lower(), tools.selections.MAIN["Y"]),]
    # aif
    data_2 = []

    for s in [tools.selections.MAIN["W"], tools.selections.MAIN["G"]]:
        request = ("SELECT "+", ".join(["AVG("+lever+str(topic)+")" for topic in codes.i2df.TOPICS_BY_LEVERS[lever]])+"\n"
                   "FROM "+s["expression"]+"\n")
        answer = tools.connect.execute(request)[0]
        data_2.append(10*sum(filter(None, answer))/len(answer))
    data = [data_1, data_2]
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = int(data[i][j]*10)/10
    fig, x = tools.export.templateFigure([s1, s2], data, (4,3.5))
    plt.ylim(0, 119)
    plt.title("Maturité : levier "+lever.upper())
    fig.subplots_adjust(left=0.09, right=0.99, top=0.9, bottom=0.12)
    plt.xlabel("Tranche d'effectif")
    plt.ylabel("Maturité dans le levier "+lever.upper())
    plt.xticks(x, name, rotation = 0)
    plt.savefig(FOLDER+"by_workforce/lever"+lever.upper()+"/"+s1["name"]+"_with_"+s2["name"]+".pdf")
