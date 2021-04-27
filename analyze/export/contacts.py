#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import csv

import tools.connect
import tools.terminals
import codes.insee

    #========= CONSTANTS =================================================#

FOLDER = "../exported/contacts/"

    #========= COLUMNS ===================================================#

def processEtablissementSiege(v):
    if "true" in v:
        return "Oui"
    return "Non"

def processActivitePrincipaleEtablissement(v):
    if v!="" and v!=None:
        if '\n' in v:
            return '\n'.join([processActivitePrincipaleEtablissement(u) for u in v.split('\n')])
        return "("+v+") : "+codes.insee.descriptionOfActivityCode(v)
    else:
        return ""

def processSection(v):
    if v!="" and v!=None:
        if '\n' in v:
            return '\n'.join([processSection(u) for u in v.split('\n')])
        section = codes.insee.enclosingActivityCode(1, v)
        return "("+section+") : "+codes.insee.descriptionOfActivityCode(section)
    else:
        return ""

def processTrancheEffectifsEtablissement(v):
    if v!="" and v!=None:
        if '\n' in v:
            return '\n'.join([processTrancheEffectifsEtablissement(u) for u in v.split('\n')])
        return "("+str(v)+") : "+codes.insee.WORKFORCES[v]+" employés"
    else:
        return ""

def processNumeroVoieEtablissement(v):
    if v==None:
        return ""
    return v

view_company = [
    [
        "name",
         "Nom de l'entreprise",
    ],
    [
        "siren",
        "Siren de l'entreprise",
    ],
    [
        "GROUP_CONCAT(DISTINCT activitePrincipaleEtablissement SEPARATOR '\n')",
        "Activité principale exercée",
        processActivitePrincipaleEtablissement
    ],
    [
        "GROUP_CONCAT(etablissementSiege SEPARATOR '\n')",
        "Siège social en AURA",
        processEtablissementSiege
    ],
    [
        "COUNT(*)",
        "Nombre de ses établissements répondants au filtrage",
    ],
    [
        "GROUP_CONCAT(siret SEPARATOR '\n')",
        "Sirets de ses établissements répondants au filtrage",
    ],
    [
        "GROUP_CONCAT(trancheEffectifsEtablissement SEPARATOR '\n')",
        "Tranches d'effectifs de ses établissements",
        processTrancheEffectifsEtablissement
    ],
    [   "GROUP_CONCAT(dateCreationEtablissement SEPARATOR '\n')",
        "Création de ses établissements",
    ],
    [
        "GROUP_CONCAT(codePostalEtablissement SEPARATOR '\n')",
        "Code postaux de ses établissements",
    ],
    [
        "phone",
        "Téléphone",
    ],
    [
        "mail",
        "Email",
    ],
    [
        "CONCAT('https://aurasmus.becht.network/', siren, '/', token)",
        "Lien vers questionnaire",
    ],
]

view_filter = [
        ["codePostalEtablissement",
         "codePostalEtablissement"],

        ["activitePrincipaleEtablissement",
         "activitePrincipaleEtablissement"],

        ["caractereEmployeurEtablissement",
         "caractereEmployeurEtablissement"],

        ["etatAdministratifEtablissement",
         "etatAdministratifEtablissement"],

        ["trancheEffectifsEtablissement",
         "trancheEffectifsEtablissement"],
    ]

    #========= VIEWS

views = {}

view_columns = view_company
sql = ("SELECT "+", ".join([c[0] for c in view_columns])+"\n"
       "FROM "+tools.selections.orderByHeadquarters(tools.selections.MAIN["C"])["expression"]+"\n"
       "WHERE mail NOT LIKE '' OR phone NOT LIKE ''\n"
       "GROUP BY siren")
views["enterprises"] = [sql, view_columns]

    #========= EXPORT FUNCTIONS ==========================================#

def spreadsheet():
    separator = ','
    for name in views:

        answer = tools.connect.execute(views[name][0])
        data = [[c[1] for c in views[name][1]]]+[[views[name][1][k][2](answer[j][k]) if len(views[name][1][k])==3 else answer[j][k] for k in range(len(views[name][1]))] for j in range(len(answer))]

        print('-> Exporting '+name+". ("+str(len(answer))+" rows)")

        f = open(FOLDER+name+".csv", "w", encoding='utf-8')
        f.write(u"\n".join([separator.join(['"'+str(v)+'"'
                                          for v in line])
                                for line in data]))
        f.close()

def spreadsheet2():
    sql = "SELECT siren, name, CONCAT('https://aurasmus.becht.network/', siren, '/', token) FROM Survey WHERE answerDate IS NULL;"
    answer = tools.connect.execute(sql)

    with open(FOLDER+'links.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
        for row in answer:
            spamwriter.writerow(row)
