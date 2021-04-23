#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import tools.connect as connect
import tools.terminals as terminals
import tools.files as files

    #========= VARIABLES =================================================#

insertions_by_request = 1000

    #========= TERMINAL ==================================================#

print("Tool for saving data to the database.")
print("The table must have been created with initialize.py before.")
terminals.stopInfo()

source, file = files.selector()
handler = files.Handler(source, file)

if input("Insert in table '"+handler.table+"'? Type 'go' to proceed: ")=="go":
    columns = handler.columns
    stmt = ("INSERT INTO "+handler.table+" "
            "("+', '.join(columns)+") "
            "VALUES ("+', '.join(["%s" for i in range(len(columns))])+");")

    while not handler.finished:
        data = handler.next(insertions_by_request)
        connect.execute([stmt, data], True)

terminals.finished()
