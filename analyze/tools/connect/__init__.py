#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import mysql.connector

try:
    from tools.connect.admin import *
    print("Admin access to database.")
except ImportError as error:
    from tools.connect.reader import *
    print("Reader access to database.")

    #========= FUNCTIONS =================================================#

def execute(request, many=False):
    """Returns the query result given by the database.
    If 'many' is True, 'request' must be like: [stmt, data]
    Otherwise, by default, 'request' is a string containing a sql query.
    """
    try:
        result = None
        cnx = mysql.connector.connect(**DB)
        cur = cnx.cursor(buffered=True)
        if many:
            # execute the given operation multiple times
            cur.executemany(*request)
        elif request.count(";")>1:
            # execute multiple operations
            for q in request.split(';')[:-1]:
                print('-> '+str(execute(q)))
            result = '-> Done!'
        else:
            # execute one operation and fetch its result for a reading request
            cur.execute(request)
            request = request.replace(' ', '').replace('\n', '')
            if request[0:6]=="SELECT" or request[0:4]=="SHOW":
                result = cur.fetchall()
        cnx.commit()
        cur.close()
        cnx.close()
        return result
    except Exception as e:
        print(str(e))
        return None
