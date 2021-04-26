#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import tools.connect
import tools.terminals
import tools.files

    #========= VARIABLES =================================================#

insertions_by_request = 1000

    #========= TERMINAL ==================================================#

print("Tool for saving data to the database.")
print("The table must have been created with initialize.py before.")
tools.terminals.stopInfo()

source, file = tools.files.selector()
handler = tools.files.Handler(source, file)

if tools.terminals.do("insert in table"):
    columns = handler.columns
    stmt = ("INSERT INTO "+handler.table+" "
            "("+', '.join(columns)+") "
            "VALUES ("+', '.join(["%s" for i in range(len(columns))])+");")

    while not handler.finished:
        data = handler.next(insertions_by_request)
        tools.connect.execute([stmt, data], True)

tools.terminals.finished()
