#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import cgi
import jinja2 as j

env = j.Environment(loader=j.PackageLoader('html-templates', '/'))
template = env.get_template("write_table.html")

def print_items():
    con = mdb.connect('localhost', 'eric', 'eric', 'testdb')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        
        cur.execute("SELECT * FROM CheckOutItems WHERE Active=1")
        
        rows = cur.fetchall()

    if len(rows) == 0:
        return 'nothing'
    else:
        return template.render({'rows':rows})
        #return "something"


#print(print_items())
print("something")
