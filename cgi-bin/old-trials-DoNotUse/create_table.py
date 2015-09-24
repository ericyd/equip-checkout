#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys


try:
    #                 <hostname>   <user>  <pass>  <db name>
    con = mdb.connect('localhost', 'eric', 'eric', 'testdb');

    cur = con.cursor()
    cur.execute("SELECT VERSION()")

    ver = cur.fetchone()
    
    print "Database version : %s " % ver
    
except mdb.Error, e:
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
finally:    
        
    if con:    
        con.close()

con = mdb.connect('localhost', 'eric', 'eric', 'testdb');
with con:
    # opens using a dictionary cursor, so we can reference things by their column name
    cur = con.cursor(mdb.cursors.DictCursor)
    
    cur.execute("CREATE TABLE CheckOutItems(Id INT PRIMARY KEY AUTO_INCREMENT, Item VARCHAR(25), Firstname VARCHAR(30), Lastname VARCHAR(30), PSUId INT, Active INT)")
    
    
    #cur.execute("USE CheckOutItems")
