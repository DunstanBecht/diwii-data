#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import tools.connect as connect
import tools.terminals as terminals

    #========= TERMINAL ==================================================#

print("Unsuscribe an enterprise.")
terminals.stopInfo()

print('\nAlready unsubscribed enterprises:')
sql = "SELECT name FROM Survey WHERE unsubscribed IS NOT NULL;"
answer = connect.execute(sql)
for a in answer:
    print('- '+a[0])

siren = input("\nSiren: ")
if siren!=terminals.STOP:
    sql = "SELECT name FROM Survey WHERE siren = "+siren+";"
    answer = connect.execute(sql)

    if len(answer)>=1:
        if input("Unsubscribe "+answer[0][0]+"? Type 'yes' to proceed: ")=="yes":
            sql = "UPDATE Survey SET unsubscribed='1' WHERE siren = "+siren+";"
            print(connect.execute(sql))
        else:
            print("Aborted.")
    else:
        print("No matching enterprise.")

terminals.finished()
