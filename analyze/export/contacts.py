#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import csv

import tools.connect
import tools.terminals
import codes.insee as insee

    #========= CONSTANTS =================================================#

FOLDER = "../exported/contacts/"

    #========= VARIABLES =================================================#

tables = ["Orbis_2021_02_18", "insee_StockEtablissement_Filtered"]
tables_alias = ["orbis", "insee"]
joins = ["AutreNdegdidentificationdelentreprise", "siren"]

    #========= COLUMNS ===================================================#

def processEtablissementSiege(v):
    if v=="true":
        return "Oui"
    elif v=="false":
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

view_establishment = [
        ["siret",
         "Siret (établissement)"],

        ["name",
         "["+tables_alias[0]+"]\nNom"],

        ["phone",
         "["+tables_alias[0]+"]\nTéléphone"],

        ["mail",
         "["+tables_alias[0]+"]\nEmail"],

        ["etablissementSiege",
         "["+tables_alias[1]+"]\nSiège de l'entreprise",
         processEtablissementSiege],

        ["activitePrincipaleEtablissement",
         "["+tables_alias[1]+"]\nActivité principale exercée",
         processActivitePrincipaleEtablissement],

        ["activitePrincipaleEtablissement",
         "["+tables_alias[1]+"]\nSection",
         processSection],

        ["trancheEffectifsEtablissement",
         "["+tables_alias[1]+"]\nTranche effectif de l'établissement",
         processTrancheEffectifsEtablissement],

        ["dateCreationEtablissement",
         "["+tables_alias[1]+"]\nDate création établissement"],

        ["numeroVoieEtablissement",
         "["+tables_alias[1]+"]\nNuméro",
         processNumeroVoieEtablissement],

        ["typeVoieEtablissement",
         "["+tables_alias[1]+"]\nType"],

        ["libelleVoieEtablissement",
         "["+tables_alias[1]+"]\nVoie"],

        ["codePostalEtablissement",
         "["+tables_alias[1]+"]\nCode postal"],

        ["libelleCommuneEtablissement",
         "["+tables_alias[1]+"]\nCommune"],
    ]

view_company = [
        ["siren",
         "Siren (entreprise)"],

        ["NomdelentrepriseLatinalphabet",
         "["+tables_alias[0]+"]\nNom"],

        ["Telephone",
         "["+tables_alias[0]+"]\nTéléphone"],

        ["Email",
         "["+tables_alias[0]+"]\nEmail"],

        ["etablissementSiege",
         "["+tables_alias[1]+"]\nA son siège en AURA",
         processEtablissementSiege],

        ["COUNT(*)",
         "["+tables_alias[1]+"]\nNombre d'établissements actifs en AURA répondants au filtrage"],

        ["GROUP_CONCAT(DISTINCT activitePrincipaleEtablissement SEPARATOR '\n')",
         "["+tables_alias[1]+"]\nActivité principale exercée",
         processActivitePrincipaleEtablissement],

        ["GROUP_CONCAT(DISTINCT activitePrincipaleEtablissement SEPARATOR '\n')",
         "["+tables_alias[1]+"]\nSection",
         processSection],

        ["GROUP_CONCAT(trancheEffectifsEtablissement SEPARATOR '\n')",
         "["+tables_alias[1]+"]\nTranches effectif des établissements actifs en AURA répondants au filtrage",
         processTrancheEffectifsEtablissement],

        ["GROUP_CONCAT(dateCreationEtablissement SEPARATOR '\n')",
         "["+tables_alias[1]+"]\nDate création établissements"],

        ["numeroVoieEtablissement",
         "["+tables_alias[1]+"]\nNuméro",
         processNumeroVoieEtablissement],

        ["typeVoieEtablissement",
         "["+tables_alias[1]+"]\nType"],

        ["libelleVoieEtablissement",
         "["+tables_alias[1]+"]\nVoie"],

        ["codePostalEtablissement",
         "["+tables_alias[1]+"]\nCode postal"],

        ["libelleCommuneEtablissement",
         "["+tables_alias[1]+"]\nCommune"],
    ]

view_filter = [
        ["codePostalEtablissement",
         "["+tables_alias[1]+"]\ncodePostalEtablissement"],

        ["activitePrincipaleEtablissement",
         "["+tables_alias[1]+"]\nactivitePrincipaleEtablissement"],

        ["caractereEmployeurEtablissement",
         "["+tables_alias[1]+"]\ncaractereEmployeurEtablissement"],

        ["etatAdministratifEtablissement",
         "["+tables_alias[1]+"]\netatAdministratifEtablissement"],

        ["trancheEffectifsEtablissement",
         "["+tables_alias[1]+"]\ntrancheEffectifsEtablissement"],
    ]

    #========= VIEWS

views = {}

view_columns = view_establishment
sql = ("SELECT "+", ".join([c[0] for c in view_columns])+"\n"
       "FROM "+tables[0]+"\n"
       "INNER JOIN "+tables[1]+"\n"
       "ON "+tables[0]+"."+joins[0]+" = "+tables[1]+"."+joins[1]+"\n"
       "ORDER BY siren ASC, etablissementSiege DESC")
views["establishments"] = [sql, view_columns]

view_columns = view_company
sql = ("SELECT "+", ".join([c[0] for c in view_columns])+"\n"
       "FROM (\n"
           "SELECT *\n"
           "FROM "+tables[0]+"\n"
           "INNER JOIN "+tables[1]+"\n"
           "ON "+tables[0]+"."+joins[0]+" = "+tables[1]+"."+joins[1]+"\n"
           "ORDER BY siren ASC, etablissementSiege DESC"
       ") AS t\n"
       "WHERE Email NOT LIKE '' OR Telephone NOT LIKE ''\n"
       "GROUP BY siren")
views["enterprises"] = [sql, view_columns]

view_columns = view_establishment
sql = ("SELECT "+", ".join([c[0] for c in view_columns])+"\n"
       "FROM "+tables[0]+"\n"
       "LEFT JOIN "+tables[1]+"\n"
       "ON "+tables[0]+"."+joins[0]+" = "+tables[1]+"."+joins[1]+"")
views["all_"+tables_alias[0]] = [sql, view_columns]

view_columns = view_establishment
sql = ("SELECT "+", ".join([c[0] for c in view_columns])+"\n"
       "FROM "+tables[0]+"\n"
       "RIGHT JOIN "+tables[1]+"\n"
       "ON "+tables[0]+"."+joins[0]+" = "+tables[1]+"."+joins[1]+"")
views["all_"+tables_alias[1]] = [sql, view_columns]

view_columns = view_filter
sql = ("SELECT "+", ".join([c[0] for c in view_columns])+"\n"
       "FROM "+tables[0]+" AS a\n"
       "INNER JOIN Insee_StockEtablissement AS b\n"
       "ON a."+joins[0]+" = b."+joins[1]+"\n"
       "WHERE a."+joins[0]+" NOT IN (SELECT "+joins[1]+" FROM "+tables[1]+")")
views["errors"] = [sql, view_columns]

    #========= TERMINAL ===================================================#

if __name__ == '__main__':
    print("Tool for exporting contacts data.")
    tools.terminals.stopInfo()

    if tools.terminals.do("export qualitative table"):
        folder = "../../Qualitative/Contacts/"
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

    if tools.terminals.do("export quantitative table"):
        sql = "SELECT siren, name, CONCAT('https://aurasmus.becht.network/', siren, '/', token) FROM Survey WHERE answerDate IS NULL;"
        answer = tools.connect.execute(sql)

        with open(FOLDER+'links.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
            for row in answer:
                spamwriter.writerow(row)

    tools.terminals.finished()
