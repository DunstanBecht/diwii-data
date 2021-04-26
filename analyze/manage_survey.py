#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import tools.terminals

    #========= TERMINAL ==================================================#

print("Tool for managing the survey.")
tools.terminals.stopInfo()

if tools.terminals.do("unsuscribe enterprise"):
    import survey.unsubscribe

if tools.terminals.do("add contacts"):
    import survey.add

tools.terminals.finished()
