#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= CONSTANTS =================================================#

COMMON_PARTS = {
    1: "J'ai déjà entendu parler de :",
    2: "Une nouvelle technologie aurait vocation à :",
    3: "J'ai déjà implémenté de nouveaux concepts ou technologies dans :",
    4: "Les thématiques suivantes m'intéressent :",
    5: "Dans la mise en place d'une technologie la part de l'humain est de :",
    6: "A propos des financements :",
}

ANSWERS = {
    1: {
        "answer1a": "Industrie 4.0",
        "answer1b": "Industrie du futur",
        "answer1c": "Campus région du numérique",
        "answer1d": "Plateforme DIWII",
    },
    2: {
        "answer2b": "Améliorer la communication",
        "answer2c": "S'orienter vers de nouveaux marchés",
        "answer2d": "Personnaliser l'offre (mass customization)",
        "answer2e": "Participer à la transition écologique",
        "answer2f": "Améliorer l'efficicence des processus de production",
        "answer2g": "Augmenter les volumes de production",
        "answer2h": "Relocaliser ma fabrication",
    },
    3: {
        "answer3a": "Objets connectés et Internet industriel",
        "answer3b": "Technologies de production avancées",
        "answer3c": "Nouvelle approche de l'Homme au travail",
        "answer3d": "Usines et lignes/îlots connectés et optimisés",
        "answer3e": "Relations clients/fournisseurs intégrées",
        "answer3f": "Nouveaux modèles économiques et sociétaux",
    },
    4: {
        "answer4a": "Objets connectés et Internet industriel",
        "answer4b": "Technologies de production avancées",
        "answer4c": "Nouvelle approche de l'Homme au travail",
        "answer4d": "Usines et lignes/îlots connectés et optimisés",
        "answer4e": "Relations clients/fournisseurs intégrées",
        "answer4f": "Nouveaux modèles économiques et sociétaux",
    },
    5: {
        'a': " 0% à  20%",
        'b': "20% à  40%",
        'c': "40% à  60%",
        'd': "60% à  80%",
        'e': "80% à 100%",
    },
    6: {
        "answer6a": "Déjà fait appel à des financements\nrégionaux pour l'aide à l'investissement",
        "answer6b": "Je souhaiterais de l'information",
    },
}
