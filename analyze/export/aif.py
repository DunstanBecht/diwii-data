#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import matplotlib.pyplot as plt

import tools.connect
import codes.i2df
import tools.export

    #========= CONSTANTS =================================================#

FOLDER = "../exported/aif/"

    #========= EXPORT FUNCTIONS ==========================================#

def figureEnterprisesByWorkforce(*selections):
    tools.export.inform(selections)
    assert tools.selections.checkKind(selections)=="enterprises"
    answers = []
    for selection in selections:
        request = ("SELECT Effectif, COUNT(*)\n"
                   "FROM "+selection['expression']+"\n"
                   "GROUP BY Effectif\n"
                   "ORDER BY Effectif ASC")
        answers.append(tools.connect.execute(request))
    name, data = tools.export.homogenize(answers)
    for i in range(len(name)):
        if name[i]=="":
            name[i]="?"
    fig, x = tools.export.templateFigure(selections, data, (9,5))
    fig.subplots_adjust(left=0.09, right=0.99, top=0.99, bottom=0.12)
    plt.xlabel("Tranche d'effectif de l'entreprise")
    plt.ylabel("Nombre d'entreprises")
    plt.xticks(x, name, rotation = 0)
    plt.savefig(FOLDER+"representativeness/enterprises_by_workforce.pdf")

def figureEnterprisesByDepartment(*selections):
    tools.export.inform(selections)
    assert tools.selections.checkKind(selections)=="enterprises"
    answers = []
    for selection in selections:
        request = ("SELECT Departement, COUNT(*)\n"
                   "FROM "+selection['expression']+"\n"
                   "GROUP BY Departement\n"
                   "ORDER BY Departement ASC")
        answers.append(tools.connect.execute(request))
    name, data = tools.export.homogenize(answers, 0, tools.selections.FILTER_A)
    fig, x = tools.export.templateFigure(selections, data, (9,5))
    fig.subplots_adjust(left=0.09, right=0.99, top=0.99, bottom=0.12)
    plt.xlabel("Département")
    plt.ylabel("Nombre d'entreprises")
    plt.xticks(x, name, rotation = 0)
    plt.savefig(FOLDER+"representativeness/enterprises_by_department.pdf")

def figureTopics(*selections):
    answers = []
    for selection in selections:
        request = ("SELECT "+", ".join(["AVG("+topic+")" for topic in codes.i2df.TOPICS])+"\n"
                   "FROM "+selection["expression"]+"\n")
        answer = tools.connect.execute(request)[0]
        answers.append([[codes.i2df.TOPICS_CODES[i], int(100*answer[i])/100] for i in range(len(codes.i2df.TOPICS))])
    name, data = tools.export.homogenize(answers)
    fig, x = tools.export.templateFigure(selections, data)
    fig.subplots_adjust(left=0.09, right=0.99, top=0.99, bottom=0.1)
    plt.xlabel("Thématique")
    plt.ylabel("Indice")
    plt.ylim(0, 10)
    plt.xticks(x, name, rotation = 90)
    plt.savefig(FOLDER+"topics/"+"_with_".join([t["name"] for t in selections])+".pdf")

def figureLevers(*selections):
    answers = []
    for selection in selections:
        request = ("SELECT "+", ".join(["AVG("+topic+")" for topic in codes.i2df.TOPICS])+"\n"
                   "FROM "+selection["expression"]+"\n")
        answer = tools.connect.execute(request)[0]
        answer = [[codes.i2df.TOPICS_CODES[i], answer[i]] for i in range(len(codes.i2df.TOPICS))]
        avg = [[] for i in range(len(codes.i2df.LEVERS))]
        for a in answer:
            avg[codes.i2df.LEVERS_CODES.index(a[0][0])].append(a[1])
        for i in range(len(avg)):
            avg[i] = [codes.i2df.LEVERS_CODES[i], int(100*sum(filter(None, avg[i]))/len(avg[i]))/100]
        answers.append(avg)
    name, data = tools.export.homogenize(answers)
    fig, x = tools.export.templateFigure(selections, data)
    fig.subplots_adjust(left=0.09, right=0.99, top=0.99, bottom=0.15)
    plt.xlabel("Leviers")
    plt.ylabel("Indice")
    plt.ylim(0, 10)
    plt.xticks(x, name, rotation = 90)
    plt.savefig(FOLDER+"levers/"+"_with_".join([t["name"] for t in selections])+".pdf")
