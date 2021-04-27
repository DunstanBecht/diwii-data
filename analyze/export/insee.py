#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import matplotlib.pyplot as plt
import folium
import json

import tools.connect
import tools.export
import codes.insee

    #========= CONSTANTS =================================================#

FOLDER = "../exported/insee/"

    #========= EXPORT FUNCTIONS ==========================================#

def map(selection):
    assert tools.selections.checkKind([selection])=="establishments"
    tools.export.inform([selection])
    request = ("SELECT codePostalEtablissement, COUNT(*)\n"
               "FROM "+selection['expression']+"\n"
               "GROUP BY codePostalEtablissement")
    answer = tools.connect.execute(request)
    color = '#%02x%02x%02x' % selection["color"]
    m = folium.Map(location=[45.5, 4.819629], tiles="stamentoner", zoom_start=8, control_scale=True)
    folium.GeoJson(json.load(open("../sources/gregoiredavid/aura.geojson"))).add_to(m)
    factor = -0.008*len(answer)+5.48
    for a in answer:
        try:
            adr = a[0]
            weight = int(a[1])
            loc = tools.export.geocode(adr)
            loc.reverse()
            folium.CircleMarker(
                location=loc,
                radius=(weight**(1/2))*factor,
                popup=adr+": "+str(weight),
                color=color,
                fill=True,
                fill_color=color,
            ).add_to(m)
        except Exception as e:
            print("Error on "+str(a)+": "+str(e))
    m.save(FOLDER+"maps/"+selection['name']+'.html')

def figureEstablishmentsByWorkforce(*selections):
    assert tools.selections.checkKind(selections)=="establishments"
    tools.export.inform(selections)
    answers = []
    for selection in selections:
        request = ("SELECT trancheEffectifsEtablissement, COUNT(*)\n"
                   "FROM "+selection['expression']+"\n"
                   "GROUP BY trancheEffectifsEtablissement\n"
                   "ORDER BY trancheEffectifsEtablissement ASC")
        answers.append(tools.connect.execute(request))
    name, data = tools.export.homogenize(*answers)
    fig, x = tools.export.templateFigure(selections, data)
    fig.subplots_adjust(left=0.09, right=0.99, top=0.99, bottom=0.15)
    plt.xlabel("Tranche d'effectif de l'établissement")
    plt.ylabel("Nombre d'établissements")
    plt.xticks(x, [codes.insee.WORKFORCES[n] for n in name], rotation = 90)
    plt.savefig(FOLDER+"establishments_by_workforce/"+"_with_".join([t["name"] for t in selections])+".pdf")

def figureEstablishmentsByDivision(*selections):
    assert tools.selections.checkKind(selections)=="establishments"
    tools.export.inform(selections)
    answers = []
    for selection in selections:
        request = ("SELECT SUBSTRING(activitePrincipaleEtablissement, 1, 2), COUNT(*)\n"
                   "FROM "+selection["expression"]+"\n"
                   "GROUP BY SUBSTRING(activitePrincipaleEtablissement, 1, 2)\n"
                   "ORDER BY SUBSTRING(activitePrincipaleEtablissement, 1, 2) ASC")
        answers.append(tools.connect.execute(request))
    name, data = tools.export.homogenize(*answers)
    fig, x = tools.export.templateFigure(selections, data)
    fig.subplots_adjust(left=0.1, right=0.99, top=0.99, bottom=0.06)
    plt.xlabel("Division APE")
    plt.ylabel("Nombre d'établissements")
    plt.xticks(x, name)
    plt.yticks([500*i for i in range(21)])
    plt.savefig(FOLDER+"establishments_by_division/"+"_with_".join([t["name"] for t in selections])+".pdf")

def figureEnterprisesByDivision(*selections):
    assert tools.selections.checkKind(selections)=="establishments"
    tools.export.inform(selections)
    answers = []
    for selection in selections:
        request = ("SELECT SUBSTRING(activitePrincipaleEtablissement, 1, 2), COUNT(*)\n"
                   "FROM (\n"
                   "SELECT * FROM "+selection["expression"]+" GROUP BY siren) AS t\n"
                   "GROUP BY SUBSTRING(activitePrincipaleEtablissement, 1, 2)\n"
                   "ORDER BY SUBSTRING(activitePrincipaleEtablissement, 1, 2) ASC")
        answers.append(tools.connect.execute(request))
    name, data = tools.export.homogenize(*answers)
    fig, x = tools.export.templateFigure(selections, data)
    fig.subplots_adjust(left=0.1, right=0.99, top=0.99, bottom=0.06)
    plt.xlabel("Division APE")
    plt.ylabel("Nombre d'entreprises")
    plt.xticks(x, name)
    plt.yticks([500*i for i in range(19)])
    plt.savefig(FOLDER+"enterprises_by_division/"+"_with_".join([t["name"] for t in selections])+".pdf")

def figureEnterprisesByOwnedEstablishments(*selections):
    assert tools.selections.checkKind(selections)=="establishments"
    tools.export.inform(selections)
    answers = []
    for selection in selections:
        request = ("SELECT nb, COUNT(*) \n"
                   "FROM (\n"
                    "SELECT siren, COUNT(*) as nb\n"
                    "FROM "+selection["expression"]+"\n"
                    "GROUP BY siren) AS t\n"
                   "GROUP BY nb")
        answer = tools.connect.execute(request)
        a = []
        s = 0
        frontier = 10
        for i in range(len(answer)):
            if answer[i][0]>=frontier:
                s += answer[i][1]
            else:
                a.append([answer[i][0], answer[i][1]])
        a.append([frontier, s])
        answers.append(a)
    name, data = tools.export.homogenize(*answers)
    name[-1] = str(frontier)+" ou +"
    fig, x = tools.export.templateFigure(selections, data)
    fig.subplots_adjust(left=0.1, right=0.99, top=0.99, bottom=0.06)
    plt.xlabel("Nombre d'établissements possédés par l'entreprise en Auvergne-Rhône-Alpes")
    plt.ylabel("Nombre d'entreprises")
    plt.xticks(x, name)
    plt.savefig(FOLDER+"enterprises_by_owned_establishments/"+"_with_".join([t["name"] for t in selections])+".pdf")
