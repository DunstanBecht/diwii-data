#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import tools.connect
import tools.terminals

    #========= TERMINAL ==================================================#

print("SQL command prompt.")
tools.terminals.stopInfo()

def promptSQL():
    return input("\nSQL ["+tools.connect.DB["database"]+"]> ")

request = promptSQL()
while request!=tools.terminals.STOP:
    print(tools.connect.execute(request))
    request = promptSQL()

tools.terminals.finished()
