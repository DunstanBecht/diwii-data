#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import matplotlib.pyplot as plt
import numpy as np
import requests, json
import urllib.parse
import folium

import tools.connect as connect
import tools.terminals as terminals
import tools.selections
import codes.insee as insee
import codes.i2df as i2df
import tools.export

    #========= CONSTANTS =================================================#

FOLDER = "../exported/aif/"

    #========= GENERATORS ================================================#

def figureTopics(*selections):
    answers = []
    for selection in selections:
        request = ("SELECT "+", ".join(["AVG("+topic+")" for topic in i2df.TOPICS])+"\n"
                   "FROM "+selection["expression"]+"\n")
        answer = connect.execute(request)[0]
        answers.append([[i2df.TOPICS_CODES[i], answer[i]] for i in range(len(i2df.TOPICS))])
    name, data = tools.export.homogenize(*answers)
    fig, x = tools.export.templateFigure(selections, data)
    fig.subplots_adjust(left=0.09, right=0.99, top=0.99, bottom=0.15)
    plt.xlabel("Thématique")
    plt.ylabel("Indice")
    plt.ylim(0, 10)
    plt.xticks(x, name, rotation = 90)
    plt.savefig(FOLDER+"topics/"+"_with_".join([t["name"] for t in selections])+".pdf")

def figureLevers(*selections):
    answers = []
    for selection in selections:
        request = ("SELECT "+", ".join(["AVG("+topic+")" for topic in i2df.TOPICS])+"\n"
                   "FROM "+selection["expression"]+"\n")
        answer = connect.execute(request)[0]
        answer = [[i2df.TOPICS_CODES[i], answer[i]] for i in range(len(i2df.TOPICS))]
        avg = [[] for i in range(len(i2df.LEVERS))]
        for a in answer:
            avg[i2df.LEVERS_CODES.index(a[0][0])].append(a[1])
        for i in range(len(avg)):
            avg[i] = [i2df.LEVERS_CODES[i], sum(avg[i])/len(avg[i])]
        answers.append(avg)
    name, data = tools.export.homogenize(*answers)
    fig, x = tools.export.templateFigure(selections, data)
    fig.subplots_adjust(left=0.09, right=0.99, top=0.99, bottom=0.15)
    plt.xlabel("Leviers")
    plt.ylabel("Indice")
    plt.ylim(0, 10)
    plt.xticks(x, name, rotation = 90)
    plt.savefig(FOLDER+"levers/"+"_with_".join([t["name"] for t in selections])+".pdf")