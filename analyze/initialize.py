#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import tools.connect as connect
import tools.terminals as terminals
import tools.files as files

    #========= TERMINAL ==================================================#

print("Tool for creating a table in the database.")
terminals.stopInfo()

source, file = files.selector()
handler = files.Handler(source, file)

if input("Initialize table '"+handler.table+"'? Type 'go' to proceed: ")=="go":

    print('Table deletion.')
    connect.execute("DROP TABLE IF EXISTS "+handler.table)

    print('Table creation.')
    connect.execute(open("sql/create/"+handler.table+".sql", "r").read())

terminals.finished()
