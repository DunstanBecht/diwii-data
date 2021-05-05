#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

import matplotlib.pyplot as plt
import numpy as np
import requests, json
import urllib.parse

def inform(selections):
    print("- Exporting '"+"_with_".join([s["name"] for s in selections])+"'")

def homogenize(answers, default=0, name=None,):
    if name==None:
        name = []
        for a in answers:
            for t in a:
                if t[0] not in name:
                    name.append(t[0])
        name.sort()
    data = []
    for a in answers:
        d = [None for i in range(len(name))]
        for i in range(len(a)):
            if a[i][0] in name:
                d[name.index(a[i][0])] = a[i][1]
        for i in range(len(d)):
            if d[i]==None:
                d[i]=default
        data.append(d)
    name = [str(n) for n in name]
    return name, data

def barGeometry(selections):
    bar_width = 0.9/len(selections)
    if len(selections)==1:
        return bar_width, 0
    else:
        return bar_width, (len(selections)-1)*bar_width/2

def templateFigure(selections, data, figsize=(9, 11.5)):
    fig, ax = plt.subplots(figsize=figsize)
    plt.grid(True)
    bar_width, pitch = barGeometry(selections)
    x = np.arange(len(data[0]))
    for i in range(len(data)):
        plt.bar(x+i*bar_width, data[i], bar_width, color='#%02x%02x%02x' % selections[i]["color"])
    ax.legend([t["legend"] for t in selections])
    for p in ax.patches:
        number = p.get_height()
        X = p.get_x() + p.get_width()
        Y = p.get_y() + p.get_height()+ax.get_ylim()[1]/150
        plt.text(X, Y, number, horizontalalignment='right', rotation=90, fontsize='x-small', color='grey')
    return fig, x+pitch

def geocode(adr):
    api_url = "https://api-adresse.data.gouv.fr/search/?q="
    r = requests.get(api_url + urllib.parse.quote(adr)).content.decode('unicode_escape')
    return eval(r)["features"][0]["geometry"]["coordinates"]
