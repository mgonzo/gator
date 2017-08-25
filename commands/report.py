#
# get the reports
# pull report by date and query
# format data in a legible way
#

import sqlite3

def printReport(cursor):
    cursor.execute('select * from results')
    for x in range(0, 10):
        print(cursor.fetchone())

def listReports(cursor):
    results = cursor.execute('select date, query from results group by date')
    print(results.fetchall())
    return

def viewReport(date, query, cursor):
    select = 'select * from results where date="{0}" and query="{1}"'.format(date, query)
    results = cursor.execute(select)
    print(results.fetchall())
    return

def viewLast(cursor):
    queries = cursor.execute('select date, query from results group by date')
    fetchall = queries.fetchall()[0]
    date = fetchall[0]
    query = fetchall[1]
    select = 'select * from results where date="{0}" and query="{1}"'.format(date, query)
    results = cursor.execute(select)
    print(results.fetchall())

