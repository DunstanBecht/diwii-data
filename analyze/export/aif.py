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

def figureTopics(*selections):
    answers = []
    for selection in selections:
        request = ("SELECT "+", ".join(["AVG("+topic+")" for topic in codes.i2df.TOPICS])+"\n"
                   "FROM "+selection["expression"]+"\n")
        answer = tools.connect.execute(request)[0]
        answers.append([[codes.i2df.TOPICS_CODES[i], int(100*answer[i])/100] for i in range(len(codes.i2df.TOPICS))])
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
        request = ("SELECT "+", ".join(["AVG("+topic+")" for topic in codes.i2df.TOPICS])+"\n"
                   "FROM "+selection["expression"]+"\n")
        answer = tools.connect.execute(request)[0]
        answer = [[codes.i2df.TOPICS_CODES[i], answer[i]] for i in range(len(codes.i2df.TOPICS))]
        avg = [[] for i in range(len(codes.i2df.LEVERS))]
        for a in answer:
            avg[codes.i2df.LEVERS_CODES.index(a[0][0])].append(a[1])
        for i in range(len(avg)):
            avg[i] = [codes.i2df.LEVERS_CODES[i], int(100*sum(avg[i])/len(avg[i]))/100]
        answers.append(avg)
    name, data = tools.export.homogenize(*answers)
    fig, x = tools.export.templateFigure(selections, data)
    fig.subplots_adjust(left=0.09, right=0.99, top=0.99, bottom=0.15)
    plt.xlabel("Leviers")
    plt.ylabel("Indice")
    plt.ylim(0, 10)
    plt.xticks(x, name, rotation = 90)
    plt.savefig(FOLDER+"levers/"+"_with_".join([t["name"] for t in selections])+".pdf")
