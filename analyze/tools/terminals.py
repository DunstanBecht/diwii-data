#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= CONSTANTS =================================================#

STOP = 'stop'

    #========= FUNCTIONS =================================================#

def stopInfo():
    print("Type '"+STOP+"' to exit.")

def finished():
    input("\nPress enter to exit.")

def do(action):
    print("\n"+action.capitalize()+"?")
    answer = input("Type 'yes' to proceed: ")
    if answer==STOP:
        raise SystemExit()
    return answer=="yes"
