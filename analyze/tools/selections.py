#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

import tools.connect

    #========= FUNCTIONS =================================================#

def selectionSymbole(s):
    return "$\mathcal{"+s+"}$"

def useTable(selectionName):
    tableName = "Table"+selectionName
    selection = MAIN[selectionName]
    sql = "SHOW TABLES"
    if tableName not in [a[0] for a in tools.connect.execute(sql)]:
        print("Creation of table "+tableName)
        print(tools.connect.execute("CREATE TABLE "+tableName+" AS SELECT * FROM "+selection["expression"]))
    selection["expression"] = tableName+" AS Selection"+selectionName

def orderByHeadquarters(establishments):
    assert establishments["kind"]=='establishments'
    establishments = establishments.copy()
    establishments["expression"] = ("(SELECT *\n"
                                    "FROM "+establishments["expression"]+"\n"
                                    "ORDER BY siren ASC, etablissementSiege DESC\n"
                                    ") AS Selection"+establishments["name"]+"")
    return establishments

def groupByEnterprise(establishments):
    assert establishments["kind"]=='establishments'
    enterprises = orderByHeadquarters(establishments)
    enterprises["expression"] = ("(SELECT *\n"
                                 "FROM "+enterprises["expression"]+"\n"
                                 "GROUP BY siren\n"
                                 ") AS Selection"+enterprises["name"]+"")
    enterprises["kind"] = "enterprises"
    return enterprises

def checkKind(selections):
    for s in selections:
        if s["kind"]!=selections[0]["kind"]:
            raise Exception("Different kinds.")
    return selections[0]["kind"]

def checkPartition(selections, union):
    print("\nPartitioning verification: "+' (+) '.join([t["name"] for t in selections]))
    # comparable rows ?
    if not checkKind(selections) in ["enterprises", "establishments"]:
        print("Unknown kind.")
        return False
    # union ?
    parts = []
    for selection in selections:
        sql = "SELECT COUNT(*)/(SELECT COUNT(*) FROM "+union["expression"]+") FROM "+selection["expression"]+";"
        part = tools.connect.execute(sql)[0][0]
        if part==None:
            raise Exception("empty table: division by zero")
        parts.append(part)
    print("Union: "+" + ".join([str(p) for p in parts])+" = "+str(sum(parts)))
    # intersection ?
    if selections[0]["kind"]=="enterprises":
        sql = "SELECT COUNT(*) FROM "+selections[0]["expression"]+" JOIN "+selections[1]["expression"]+" ON Selection"+selections[0]["name"]+".siren = Selection"+selections[1]["name"]+".siren"
    else:
        sql = "SELECT COUNT(*) FROM "+selections[0]["expression"]+" JOIN "+selections[1]["expression"]+" ON Selection"+selections[0]["name"]+".siret = Selection"+selections[1]["name"]+".siret"
    intersection = tools.connect.execute(sql)[0][0]
    print("Intersections: "+str(intersection))
    if intersection!=0:
        return False
    return True

    #========= CONSTANTS =================================================#

KINDS = {
    "establishments": "établissements",
    "enterprises": "entreprises",
}

MAIN = {}

    #========= F

MAIN['F'] = {
    'expression': ("(SELECT *\n"
                   "FROM insee_StockEtablissement\n"
                   "WHERE\n"
                   "etatAdministratifEtablissement LIKE 'A' AND\n"
                   "caractereEmployeurEtablissement LIKE 'O'\n"
                   ") AS SelectionF"),
    'color': ( 58,  58,  58),
    'legend': "établissements français actifs employeurs"
}

    #========= A

FILTER_A = [
    '01',
    '03',
    '07',
    '15',
    '26',
    '38',
    '42',
    '43',
    '63',
    '69',
    '73',
    '74',
]
MAIN['A'] = {
    'expression': ("(SELECT *\n"
                   "FROM "+MAIN['F']["expression"]+"\n"
                   "WHERE\n"+" OR\n".join(["codePostalEtablissement LIKE '"+code+"%'" for code in FILTER_A])+"\n"
                   ") AS SelectionA"),
    'color': ( 95, 141, 211),
    'legend': "partie de "+selectionSymbole("F")+" en Auvergne-Rhône-Alpes",
}

    #========= D

FILTER_D = [
    '10',
    '11',
    '12',
    '13',
    '14',
    '15',
    '16',
    '17',
    '18',
    '19',
    '20',
    '21',
    '22',
    '23',
    '24',
    '25',
    '26',
    '27',
    '28',
    '29',
    '30',
    '31',
    '32',
    '33',
    '35',
    '86',
]
MAIN['D'] = {
    'expression': ("(SELECT *\n"
                   "FROM "+MAIN['A']["expression"]+"\n"
                   "WHERE\n"+" OR\n".join(["activitePrincipaleEtablissement LIKE '"+code+"%'" for code in FILTER_D])+"\n"
                   ") AS SelectionD"),
    'color': ( 90, 160,  44),
    'legend': "partie de "+selectionSymbole("A")+" de divisions sélectionnées",
}
useTable('D')

    #========= E

FILTER_E = [
    '12',
    '21',
    '22',
    '31',
    '32',
    '41',
    '42',
]
MAIN["E"] = {
    'expression': ("(SELECT *\n"
                   "FROM "+MAIN['D']["expression"]+"\n"
                   "WHERE\n"+" OR\n".join(["trancheEffectifsEtablissement LIKE '"+code+"'" for code in FILTER_E])+"\n"
                   ") AS SelectionE"),
    'color': ( 22,  80,  45),
    'legend': "partie de "+selectionSymbole("D")+" de tranches d'effectifs sélectionnées",
}
useTable('E')

    #========= C

if "TableC" not in [a[0] for a in tools.connect.execute("SHOW TABLES")]:
    print("Creation of table C")
    print(tools.connect.execute(open("sql/create/TableC.sql").read()))

MAIN["C"] = {
    'expression': "(SELECT *\n"
                  "FROM TableC\n"
                  ") AS SelectionC",
    'color': (128,  51,   0),
    'legend': "partie de "+selectionSymbole("E")+" contactée",
}

    #========= R

MAIN["R"] = {
    'expression': ("(SELECT *\n"
                   "FROM "+MAIN["C"]["expression"]+"\n"
                   "WHERE\n"
                   "answerDate IS NOT NULL\n"
                  ") AS SelectionR"),
    'color': (255, 127,  42),
    'legend': "partie de "+selectionSymbole("C")+" ayant répondu",
}

    #========= M

FILTER_M = [
    '13',
    '14',
    '15',
    '16',
    '17',
    '18',
    '22',
    '24',
    '25',
    '26',
    '27',
    '28',
    '29',
    '30',
    '31',
    '32',
    '33',
]
MAIN["M"] = {
    'expression': ("(SELECT *\n"
                   "FROM "+MAIN["R"]["expression"]+"\n"
                   "WHERE\n"+" OR\n".join(["activitePrincipaleEtablissement LIKE '"+str(code)+ "%'" for code in FILTER_M])+"\n"
                   ") AS SelectionM"),
    'color': (255,  42,  42),
    'legend': "partie de "+selectionSymbole("R")+" de type manufacturière",
}

    #========= P

FILTER_P = [
    '10',
    '11',
    '12',
    '19',
    '20',
    '21',
    '23',
    '35',
    '86',
]
MAIN["P"] = {
    'expression': ("(SELECT *\n"
                   "FROM "+MAIN["R"]["expression"]+"\n"
                   "WHERE\n"+" OR\n".join(["activitePrincipaleEtablissement LIKE '"+str(code)+ "%'" for code in FILTER_P])+"\n"
                   ") AS SelectionP"),
    'color': (170,   0,   0),
    'legend': "partie de "+selectionSymbole("R")+" de type process",
}

    #========= X

FILTER_X = [
    '12',
]
MAIN["X"] = {
    'expression': ("(SELECT *\n"
                   "FROM "+MAIN["R"]["expression"]+"\n"
                   "WHERE\n"+" OR\n".join(["trancheEffectifsEtablissement LIKE '"+str(code)+ "'" for code in FILTER_X])+"\n"
                   ") AS SelectionX"),
    'color': (170, 135, 222),
    'legend': "partie de "+selectionSymbole("R")+" de $-$ de 50 employés",
}

    #========= Y

FILTER_Y = [
    '21',
    '22',
    '31',
    '32',
    '41',
    '42',
]
MAIN["Y"] = {
    'expression': ("(SELECT *\n"
                   "FROM "+MAIN["R"]["expression"]+"\n"
                   "WHERE\n"+" OR\n".join(["trancheEffectifsEtablissement LIKE '"+str(code)+ "'" for code in FILTER_Y])+"\n"
                   ") AS SelectionY"),
    'color': ( 68,  33, 120),
    'legend': "partie de "+selectionSymbole("R")+" de $+$ de 50 employés",
}

    #========= MX MY PX PY

MAIN["MX"] = {
    'expression': ("(SELECT *\n"
                   "FROM "+MAIN["M"]["expression"]+"\n"
                   "WHERE\n"+" OR\n".join(["trancheEffectifsEtablissement LIKE '"+str(code)+ "'" for code in FILTER_X])+"\n"
                   ") AS SelectionMX"),
    'color': (255,  42,  42),
    'legend': "partie de "+selectionSymbole("R")+" manufacturière de $-$ de 50 employés",
}

MAIN["MY"] = {
    'expression': ("(SELECT *\n"
                   "FROM "+MAIN["M"]["expression"]+"\n"
                   "WHERE\n"+" OR\n".join(["trancheEffectifsEtablissement LIKE '"+str(code)+ "'" for code in FILTER_Y])+"\n"
                   ") AS SelectionMY"),
    'color': (170,   0,   0),
    'legend': "partie de "+selectionSymbole("R")+" manufacturière de $+$ de 50 employés",
}

MAIN["PX"] = {
    'expression': ("(SELECT *\n"
                   "FROM "+MAIN["P"]["expression"]+"\n"
                   "WHERE\n"+" OR\n".join(["trancheEffectifsEtablissement LIKE '"+str(code)+ "'" for code in FILTER_X])+"\n"
                   ") AS SelectionX"),
    'color': (170, 135, 222),
    'legend': "partie de "+selectionSymbole("R")+" de type process de $-$ de 50 employés",
}

MAIN["PY"] = {
    'expression': ("(SELECT *\n"
                   "FROM "+MAIN["P"]["expression"]+"\n"
                   "WHERE\n"+" OR\n".join(["trancheEffectifsEtablissement LIKE '"+str(code)+ "'" for code in FILTER_Y])+"\n"
                   ") AS SelectionX"),
    'color': ( 68,  33, 120),
    'legend': "partie de "+selectionSymbole("R")+" de type process de $+$ de 50 employés",
}

    #========= I

MAIN["I"] = {
    'expression': ("(SELECT * FROM aif_I2DF) AS SelectionI"),
    'color': ( 90, 160,  44),
    'legend': "partie de "+selectionSymbole("A")+" évaluée par l'I2DF",
    'kind': "enterprises"
}

    #========= W

FILTER_W = [
    '0-13',
    '14-19',
    '20-49',
]
MAIN["W"] = {
    'expression': ("(SELECT *\n"
                   "FROM "+MAIN["I"]["expression"]+"\n"
                   "WHERE\n"+" OR\n".join(["Effectif LIKE '%"+str(code)+ "%'" for code in FILTER_W])+"\n"
                   ") AS SelectionW"),
    'color': (  50,  50,  50),
    'legend': "partie de "+selectionSymbole("I")+" de $-$ de 50 employés",
    'kind': "enterprises"
}

    #========= G

FILTER_G = [
    '50-249',
    '250-499',
    '500-5000',
]
MAIN["G"] = {
    'expression': ("(SELECT *\n"
                   "FROM "+MAIN["I"]["expression"]+"\n"
                   "WHERE\n"+" OR\n".join(["Effectif LIKE '%"+str(code)+ "%'" for code in FILTER_G])+"\n"
                   ") AS SelectionG"),
    'color': ( 100, 100, 100),
    'legend': "partie de "+selectionSymbole("I")+" de $+$ de 50 employés",
    'kind': "enterprises"
}

    #========= FOR ALL IN MAIN

for selection in MAIN:
    MAIN[selection]["name"] = selection
    MAIN[selection]["legend"] = selectionSymbole(selection)+" : "+MAIN[selection]["legend"]
    if not "kind" in MAIN[selection]:
        MAIN[selection]["kind"] = "establishments"


DIVISIONS = {}

for div in FILTER_D:
    DIVISIONS[div] = {
        'expression': ("(SELECT *\n"
                       "FROM "+MAIN['D']["expression"]+"\n"
                       "WHERE SUBSTRING(activitePrincipaleEtablissement, 1, 2) = '"+div+"'"
                       ") AS SelectionD"+div),
        'color': ( 22,  80,  45),
        'name': "D"+div,
        'legend': " $\mathcal{D}_{"+div+"}$ : partie de "+selectionSymbole("D")+" de division "+div,
        'kind': "establishments"
    }
