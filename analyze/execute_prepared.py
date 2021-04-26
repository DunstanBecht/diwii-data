#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import os

import tools.connect
import tools.terminals

    #========= CONSTANTS =================================================#

FOLDER = 'sql/prepared/'

    #========= TERMINAL ==================================================#

print("Prepared SQL requests.")
tools.terminals.stopInfo()

while True:
    files = os.listdir(FOLDER)
    print('')
    for i in range(len(files)):
        print('|'+str(i+1)+'| '+files[i].split('.')[0])
    choice = input('|>| select: ')
    if choice==tools.terminals.STOP:
        break
    choice = int(choice)
    if choice>len(files) or choice<1:
        break
    print('')
    print(tools.connect.execute(open(FOLDER+files[choice-1]).read()))

tools.terminals.finished()
