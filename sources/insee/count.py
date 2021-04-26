#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

file = 'StockEtablissement.csv'
print("Counting the number of records in '"+file+"'...")
fd = open(file, 'r', encoding='utf8')
n = 0
line = fd.readline()
while line :
    line = fd.readline()
    n += 1
print(str(n)+" rows")
input('')
