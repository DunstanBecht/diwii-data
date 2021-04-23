#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import tools.connect as connect
import tools.terminals as terminals

    #========= TERMINAL ==================================================#

print("SQL command prompt.")
terminals.stopInfo()

def promptSQL():
    return input("\nSQL ["+connect.DB["database"]+"]> ")

request = promptSQL()
while request!=terminals.STOP:
    print(connect.execute(request))
    request = promptSQL()

terminals.finished()
