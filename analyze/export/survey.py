#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import html
import matplotlib.pyplot as plt
import numpy as np

import tools.connect
import tools.selections
import codes.insee
import codes.survey
import tools.export

    #========= CONSTANTS =================================================#

FOLDER = "../exported/survey/"

    #========= EXPORT FUNCTIONS ==========================================#

def pourcentage(answer, selection, value=1):
    request = ("SELECT 100*COUNT(*)/(SELECT COUNT(*) FROM "+selection["expression"]+")\n"
               "FROM "+selection["expression"]+"\n"
               "WHERE "+answer+" = '"+str(value)+"'")
    result = tools.connect.execute(request)[0][0]
    if result==None:
        raise Exception("empty table: division by zero")
    return result

def figurePourcentages(answer, selections, data=None, sort=True):
    tools.export.inform(selections)
    kind = tools.selections.checkKind(selections)
    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=(9, 6))
    plt.xlim(0, 110)
    fig.subplots_adjust(left=0.41, right=0.99, top=0.95, bottom=0.09)
    plt.grid(True)
    plt.title(codes.survey.COMMON_PARTS[answer])
    name = []
    for key in codes.survey.ANSWERS[answer]:
        name.append(codes.survey.ANSWERS[answer][key])

    if data is None:
        data = [[] for i in range(len(selections))]
        for key in codes.survey.ANSWERS[answer]:
            for i in range(len(selections)):
                data[i].append(pourcentage(key, selections[i]))

    #if sort:
    #    data = sorted(data, key=lambda x: x[0], reverse=True)
    width, pitch = tools.export.barGeometry(selections)
    y = np.arange(len(data[0]))
    for i in range(len(selections)):
        ax.barh(y+i*width, data[i], width, color='#%02x%02x%02x' % selections[i]["color"])
    ax.set_yticks(y+pitch)
    ax.set_yticklabels(name)
    steps = [i*20 for i in range(6)]
    plt.xticks(steps, [str(s)+'%' for s in steps])
    plt.xlabel("Pourcentage d'"+tools.selections.KINDS[kind])
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.legend([tools.selections.selectionSymbole(t["name"]) for t in selections])
    for p in ax.patches:
        percentage = '{:.1f}%'.format(p.get_width())
        X = p.get_x() + p.get_width() + 1
        Y = p.get_y() + p.get_height()/2
        plt.text(X, Y, percentage, verticalalignment='center', fontsize='small', color='grey')

    plt.savefig(FOLDER+"answer"+str(answer)+"/"+"_with_".join([t["name"] for t in selections])+".pdf")

def listTextAnswer(*selections):
    tools.export.inform(selections)
    tools.selections.checkKind(selections)
    for column in ["answer2i", "answer7"]:
        answers = []
        for selection in selections:
            request = "SELECT "+column+" FROM "+selection["expression"]+" WHERE "+column+" NOT LIKE ''"
            answers.append([a[0] for a in tools.connect.execute(request)])
        for i in range(len(selections)):
            f = open(FOLDER+column+"/"+selections[i]["name"]+".tex", "w", encoding='utf-8')
            for j in range(len(answers[i])):
                if answers[i][j][-1]!='.':
                    answers[i][j] = answers[i][j]+'.'
                f.write('''\item "'''+". ".join([s.strip().capitalize() for s in html.unescape(answers[i][j]).split('.')]).strip()+'''"\n''')
            f.close()

def wordcloudAnswer(*selections):
    tools.export.inform(selections)
    tools.selections.checkKind(selections)
    for column in ["answer2i", "answer7"]:
        answers = []
        for selection in selections:
            request = "SELECT "+column+" FROM "+selection["expression"]+" WHERE "+column+" NOT LIKE ''"
            answers.append([a[0] for a in tools.connect.execute(request)])
        for i in range(len(selections)):
            text = " ".join(answers[i])
            f = open(FOLDER+column+"/"+selections[i]["name"]+".txt", "w", encoding='utf-8')
            f.write(" ".join(answers[i]))
            f.close()

def figureEstablishmentsByDivision(*selections):
    tools.export.inform(selections)
    assert tools.selections.checkKind(selections)=="establishments"
    answers = []
    for selection in selections:
        request = ("SELECT SUBSTRING(activitePrincipaleEtablissement, 1, 2), COUNT(*)\n"
                   "FROM (\n"
                   "SELECT * FROM "+selection["expression"]+" GROUP BY siren) AS t\n"
                   "GROUP BY SUBSTRING(activitePrincipaleEtablissement, 1, 2)\n"
                   "ORDER BY SUBSTRING(activitePrincipaleEtablissement, 1, 2) ASC")
        answers.append(tools.connect.execute(request))
    name, data = tools.export.homogenize(answers, 0, tools.selections.FILTER_D)
    fig, x = tools.export.templateFigure(selections, data, (9, 10))
    fig.subplots_adjust(left=0.1, right=0.99, top=0.99, bottom=0.05)
    plt.xlabel("Division APE")
    plt.ylabel("Nombre d'établissements")
    plt.xticks(x, name)
    #plt.yticks([2*i for i in range(max(data[0])//2+1)])
    plt.savefig(FOLDER+"representativeness/establishments_by_division.pdf")

def figureEstablishmentsByWorkforce(*selections):
    tools.export.inform(selections)
    assert tools.selections.checkKind(selections)=="establishments"
    answers = []
    for selection in selections:
        request = ("SELECT trancheEffectifsEtablissement, COUNT(*)\n"
                   "FROM "+selection['expression']+"\n"
                   "GROUP BY trancheEffectifsEtablissement\n"
                   "ORDER BY trancheEffectifsEtablissement ASC")
        answers.append(tools.connect.execute(request))
    name, data = tools.export.homogenize(answers, 0, tools.selections.FILTER_E)
    fig, x = tools.export.templateFigure(selections, data)
    fig.subplots_adjust(left=0.09, right=0.99, top=0.99, bottom=0.12)
    plt.xlabel("Tranche d'effectif de l'établissement")
    plt.ylabel("Nombre d'établissements")
    plt.xticks(x, [codes.insee.WORKFORCES[n] for n in name], rotation = 90)
    plt.savefig(FOLDER+"representativeness/establishments_by_workforce.pdf")

def figureEstablishmentsByDepartment(*selections):
    tools.export.inform(selections)
    assert tools.selections.checkKind(selections)=="establishments"
    answers = []
    for selection in selections:
        request = ("SELECT SUBSTRING(codePostalEtablissement, 1, 2), COUNT(*)\n"
                   "FROM "+selection['expression']+"\n"
                   "GROUP BY SUBSTRING(codePostalEtablissement, 1, 2)\n"
                   "ORDER BY SUBSTRING(codePostalEtablissement, 1, 2) ASC")
        answers.append(tools.connect.execute(request))
    name, data = tools.export.homogenize(answers, 0, tools.selections.FILTER_A)
    fig, x = tools.export.templateFigure(selections, data)
    fig.subplots_adjust(left=0.09, right=0.99, top=0.99, bottom=0.05)
    plt.xlabel("Département")
    plt.ylabel("Nombre d'établissements")
    plt.xticks(x, name, rotation = 0)
    plt.savefig(FOLDER+"representativeness/establishments_by_department.pdf")

def spreadsheetResults():
    def processAnswer(v):
        if v=="1":
            return "Oui"
        elif v=="0":
            return "Non"
        elif v is None:
            return ""
        return codes.survey.ANSWERS[5][v]

    view_company = [
            ["siren",
             "Siren (entreprise)"],

            ["name",
             "Nom"],

            ["need",
             "Souhaiteriez-vous être recontacté par un spécialiste de DIWII ?",
             processAnswer],

            ["answer7",
             "En 1 mot, dites ce que l'industrie du futur est pour vous."],

            ["answer2i",
             "Pour votre entreprise, une nouvelle technologie aurait vocation à :"],
    ]

    for answer in [1, 2, 3, 4, 6]:
        for key in codes.survey.ANSWERS[answer]:
            view_company.append([key, codes.survey.COMMON_PARTS[answer]+"\n"+codes.survey.ANSWERS[answer][key].replace("\n", ""), processAnswer])
    view_company.append(['answer5', codes.survey.COMMON_PARTS[5], processAnswer])
    views = {}

    view_columns = view_company
    sql = ("SELECT "+", ".join([c[0] for c in view_columns])+"\n"
           "FROM "+tools.selections.groupByEnterprise(tools.selections.MAIN["R"])["expression"]+"\n"
           "WHERE answerDate IS NOT NULL\n")
    views["Entreprises"] = [sql, view_columns]

    separator = ','
    for name in views:

        answer = tools.connect.execute(views[name][0])
        data = [[c[1] for c in views[name][1]]]+[[views[name][1][k][2](answer[j][k]) if len(views[name][1][k])==3 else answer[j][k] for k in range(len(views[name][1]))] for j in range(len(answer))]

        f = open(FOLDER+"results.csv", "w", encoding='utf-8')
        f.write(u"\n".join([separator.join(['"'+str(v)+'"'
                                        for v in line])
                            for line in data]))
        f.close()
