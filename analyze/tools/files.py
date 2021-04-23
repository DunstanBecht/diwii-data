#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import os.path
import importlib
import csv
import unidecode

    #========= FUNCTIONS =================================================#

def selector():
    source = input("\nSource: ") # Test
    file = input("File: ") # Test.csv
    return source, file

def formatColumn(c):
    c = unidecode.unidecode(c)
    c = c.replace(' ', '')
    c = c.replace("'", '')
    c = c.replace("[", '')
    c = c.replace("]", '')
    c = c.replace("(", '')
    c = c.replace(")", '')
    c = c.replace("%", '')
    c = c.replace(".", '')
    c = c.replace("=", '')
    c = c.replace("-", '')
    c = c.replace("\n", '')
    c = c.replace("&", 'and')
    c = c.replace(":", '')
    if len(c)>64:
        c = c[0:64]
    return c

    #========= TERMINAL ==================================================#

class Handler:

    def __init__(self, source, file):
        self.source = source
        self.table = source+"_"+file.split('.')[0]
        self.path = "../sources/"+source+"/"+file
        self.extension = file.split('.')[1]
        if self.extension!="csv":
            raise Exception("incorrect extension")
        self.delimiter = input("Delimiter: ")
        self.quotechar = input("Quotechar: ")
        self.file = open(self.path, "r", newline='', encoding='utf-8')
        self.reader = csv.reader(self.file,
                                 delimiter=self.delimiter,
                                 quotechar=self.quotechar)
        self.columns = [formatColumn(c) for c in next(self.reader)]
        self.finished = False
        path1 = "sql/reate/"+self.table+".sql"
        if not os.path.exists(path1):
            self.createFile1(path1)
        path2 = "process/"+self.table+".py"
        if not os.path.exists(path2):
            self.createFile2(path2)
        self.process = importlib.import_module("process."+self.table).process

    def next(self, n):
        val = []
        while len(val)<n:
            data = next(self.reader, None)
            if data==None:
                self.finished = True
                break
            data = self.process(data)
            if len(data)==len(self.columns):
                val.append(data)
            else:
                print(("incorrect data size: "+str(data)))
        return val

    def createFile1(self, path1):
        print('SQL request file creation.')
        file = open(path1, "a")
        file.write("CREATE TABLE "+self.table)
        file.write("\n(\n")
        file.write(",\n".join([column+" VARCHAR(100)" for column in self.columns]))
        file.write("\n)")
        file.close()

    def createFile2(self, path2):
        print('Process file creation.')
        file = open(path2, "a")
        file.write("def process(data):\n    return data")
        file.close()
