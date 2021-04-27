#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import tools.connect

    #========= VARIABLES =================================================#

restriction_table = "TableE"
contacts_table = input("Contacts table: ") # "orbis_2021_02_18"
siren_column = input("Siren column: ") # "AutreNdegdidentificationdelentreprise"
phone_column = input("Phone column: ") # "Telephone"
mail_column = input("Mail column: ") # "Email"
name_comumn = input("Name column: ") # "NomdelentrepriseLatinalphabet"

    #========= INSERTION =================================================#

sql = ("SELECT COLUMN_NAME\n"
       "FROM INFORMATION_SCHEMA.COLUMNS\n"
       "WHERE\n"
       "TABLE_SCHEMA = Database()\n"
       "AND TABLE_NAME = '"+restriction_table+"';")
restriction_columns = [a[0] for a in tools.connect.execute(sql)]

sql = ("INSERT INTO TableC\n"
       "(phone, mail, name, "+", ".join(restriction_columns)+")\n"
       "SELECT \n"
       "contacts."+phone_column+" AS phone,\n"
       "contacts."+mail_column+" AS mail,\n"
       "contacts."+name_comumn+" AS name,\n"
       ""+", ".join(["restriction."+c for c in restriction_columns])+"\n"
       "FROM\n"
       ""+restriction_table+" AS restriction\n"
       "INNER JOIN\n"
       ""+contacts_table+" AS contacts\n"
       "ON restriction.siren = contacts."+siren_column+"\n"
       "WHERE siren NOT IN (SELECT siren FROM TableC);\n"
       "UPDATE TableC\n"
       "SET token = MD5(siren)\n"
       "WHERE token IS NULL;")

print(tools.connect.execute(sql))
