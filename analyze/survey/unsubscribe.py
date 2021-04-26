#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import tools.connect
import tools.terminals

    #========= TERMINAL ==================================================#

print('\nAlready unsubscribed enterprises:')
sql = "SELECT name, siren FROM Survey WHERE unsubscribed IS NOT NULL;"
answer = tools.connect.execute(sql)
for a in answer:
    print("("+str(a[1])+") "+a[0])

siren = input("\nSiren: ")
if siren!=tools.terminals.STOP:
    sql = "SELECT name FROM Survey WHERE siren = "+siren+";"
    answer = tools.connect.execute(sql)

    if len(answer)>=1:
        print("Unsubscribe "+answer[0][0]+"?")
        if input("Type 'yes' to proceed: ")=="yes":
            sql = "UPDATE Survey SET unsubscribed='1' WHERE siren = "+siren+";"
            print(tools.connect.execute(sql))
        else:
            print("Aborted.")
    else:
        print("No matching enterprise.")
