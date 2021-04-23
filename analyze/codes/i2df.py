#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= CONSTANTS =================================================#

LEVERS = {
    'A': "Objets connectés et Internet industriel",
    'B': "Technologies de production avancées",
    'C': "Nouvelle approche de l'Homme au travail, Organisation et management innovants",
    'D': "Usines et lignes/îlots connectés, pilotés et optimisés",
    'E': "Relations clients/fournisseurs intégrées",
    'F': "Nouveaux modèles économiques et sociétaux, Stratégie et alliances",
}

LEVERS_CODES = [lever for lever in LEVERS]

TOPICS_BY_LEVERS = {
    'A': {
        1: "Produits connectés",
        2: "Technologies de connexion des machines",
        3: "Infrastructure d'échange de données",
    },
    'B': {
        1: "Nouveaux matériaux et matériaux intelligents",
        2: "Procédés de fabrication innovants",
        3: "Procédés éco-responsables",
        4: "Robotique avancée et machines intelligentes",
        5: "Automatisation, machines et robots industriels",
        6: "Composants intelligents",
        7: "Surveillance et captation multi-physique",
        8: "Contrôle Commande",
    },
    'C': {
        1: "Applications mobiles et sociales",
        2: "Qualité de Vie au Travail",
        3: "Assistance physique",
        4: "Assistance cognitive",
        5: "Conduite du changement",
    },
    'D': {
        1: "La virtualisation pour l'optimisation du système de production",
        2: "Intelligence opérationnelle : traitement en temps réel des données",
        3: "Management des opérations industrielles",
        4: "Ingénierie numérique des produits et des procédés",
        5: "Contrôle produit",
    },
    'E': {
        1: "Digitalisation de la chaîne de valeur",
        2: "Innovation et production collaborative",
        3: "Gestion du cycle de vie des produits étendue aux services",
    },
    'F': {
        1: "Insertion dans la collectivité, bien commun",
        2: "Nouveau business model",
        3: "Entreprise étendue et agile",
        4: "Entreprise stratège",
        5: "Capital immatériel",
    }
}

TOPICS = {}
for lever in TOPICS_BY_LEVERS:
    for topic in TOPICS_BY_LEVERS[lever]:
            TOPICS[lever+str(topic)] = TOPICS_BY_LEVERS[lever][topic]

TOPICS_CODES = [topic for topic in TOPICS]
