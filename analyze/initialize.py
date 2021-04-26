#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import tools.connect
import tools.terminals
import tools.files

    #========= TERMINAL ==================================================#

print("Tool for creating a table in the database.")
tools.terminals.stopInfo()

source, file = tools.files.selector()
handler = tools.files.Handler(source, file)

if tools.terminals.do("initialize table"):
    print('Table deletion (if exists).')
    tools.connect.execute("DROP TABLE IF EXISTS "+handler.table)
    print('Table creation.')
    tools.connect.execute(open("sql/create/"+handler.table+".sql", "r").read())
    print("Table name: "+handler.table)

tools.terminals.finished()
