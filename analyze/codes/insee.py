#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import pandas

    #========= CONSTANTS =================================================#

WORKFORCES = {
    'NN': 'non employeur',
    '00': '0',
    '01': '1 ou 2',
    '02': '3 à 5',
    '03': '6 à 9',
    '11': '10 à 19',
    '12': '20 à 49',
    '21': '50 à 99',
    '22': '100 à 199',
    '31': '200 à 249',
    '32': '250 à 499',
    '41': '500 à 999',
    '42': '1000 à 1999',
    '51': '2000 à 4999',
    '52': '5000 à 9999',
    '53': '10000 et +',
    '': '?',
}

ACTIVITY_LEVEL_ACCORDING_TO_CHAIN_LENGTH = {
    1: 1,
    2: 2,
    4: 3,
    5: 4,
    6: 5,
}

ACTIVITIES_BY_LEVELS = []
location = '../sources/insee/naf/'
files = [
    'naf2008_liste_n1.xls',
    'naf2008_liste_n2.xls',
    'naf2008_liste_n3.xls',
    'naf2008_liste_n4.xls',
    'naf2008_liste_n5.xls',
]
files = [location+path for path in files]
for i in range(len(files)):
    df = pandas.read_excel(files[i], dtype=str)
    activities = {}
    for j in range(2, len(df)):
        activities[str(df[df.columns[0]][j])] = df[df.columns[1]][j]
    ACTIVITIES_BY_LEVELS.append(activities)

ACTIVITY_TREE = pandas.read_excel(location+'naf2008_5_niveaux.xls', dtype=str)

DEPARTMENTS = {
    '01': 'Ain',
    '03': 'Allier',
    '07': 'Ardèche',
    '15': 'Cantal',
    '26': 'Drôme',
    '38': 'Isère',
    '42': 'Loire',
    '43': 'Haute-Loire',
    '63': 'Puy-de-Dôme',
    '69': 'Rhône',
    '73': 'Savoie',
    '74': 'Haute-Savoie',
}
    #========= FUNCTIONS =================================================#

def levelOfActivityCode(code):
    """Returns the NAF level of the code 'code'."""
    return ACTIVITY_LEVEL_ACCORDING_TO_CHAIN_LENGTH[len(code)]

def enclosingActivityCode(level, code):
    """Returns the enclosing NAF code of level 'level' for code 'code'."""
    current_level = levelOfActivityCode(code)
    if level > current_level:
        raise Exception("Inferior level!")
    for i in range(0, len(ACTIVITY_TREE[ACTIVITY_TREE.columns[5-current_level]])):
        if ACTIVITY_TREE[ACTIVITY_TREE.columns[5-current_level]][i]==code:
            return ACTIVITY_TREE[ACTIVITY_TREE.columns[5-level]][i]
    return None

def descriptionOfActivityCode(code):
    """Returns the description for the activity code 'code'."""
    if code==None:
        return ''
    level = levelOfActivityCode(code)
    return ACTIVITIES_BY_LEVELS[level-1][code]
