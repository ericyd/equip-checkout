#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import cgi


def add_item():
    con = mdb.connect('localhost', 'eric', 'eric', 'testdb')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        
        # not necessary, already exists
        #cur.execute("CREATE TABLE CheckOutItems(Id INT PRIMARY KEY AUTO_INCREMENT, Item VARCHAR(25), Firstname VARCHAR(30), Lastname VARCHAR(30), PSUId INT, Active INT)")
        
        
        
        item = raw_input("item: ")
        firstname = raw_input("first: ")
        lastname = raw_input("last: ")
        PSUId = raw_input("id #: ")
        
        # This is one way to select the "next" Id, or you can do it automatically by telling which values you will set for CheckOutItems
        #num = cur.execute("SELECT COUNT(Id) AS 'Number Of Rows' FROM CheckOutItems") 
        #num = cur.execute("SELECT 'Number Of Rows' FROM CheckOutItems") 
        #num = num+1
        #cur.execute("INSERT INTO CheckOutItems VALUES({Id}, '{item}', '{firstname}', '{lastname}', {PSUId}, {active})".format(Id=num, item=item, firstname=firstname, lastname=lastname, PSUId=int(PSUId), active=1 ))
        
        # Or you can pass in just the values you want to add
        cur.execute("INSERT INTO CheckOutItems(Item, Firstname, Lastname, PSUId, Active) VALUES('{item}', '{firstname}', '{lastname}', {PSUId}, {active})".format(item=item, firstname=firstname, lastname=lastname, PSUId=int(PSUId), active=1 ))

def deactivate_item():

    remove = raw_input("remove item? ")
    if remove:

        con = mdb.connect('localhost', 'eric', 'eric', 'testdb')
        with con:
            cur = con.cursor(mdb.cursors.DictCursor)
            
            try:
                cur.execute("UPDATE CheckOutItems SET Active = 0 WHERE Item = '{}'".format(remove)  )
            except mdb.Error, e:
                print("Couldn't find item, {} {}".format(e.args[0],e.args[1]))
            
    
def print_items():
    con = mdb.connect('localhost', 'eric', 'eric', 'testdb')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        
        cur.execute("SELECT * FROM CheckOutItems WHERE Active=1")
        
        rows = cur.fetchall()

        desc = cur.description
        # this is a tuple of tuples with most weird characters
        #print desc
        
        print "{0} {1} {2} {3} {4} {5}".format(desc[0][0], desc[1][0], desc[2][0], desc[3][0], desc[4][0], desc[5][0])
        
        text = ""
        
        if len(rows) == 0:
            print('nothing')
        else:
            for row in rows:
                text = text + row['Item'] + row['Firstname'] + row['Lastname']
                
    return text
    
    
def delete_item():
    con = mdb.connect('localhost', 'eric', 'eric', 'testdb')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("DELETE FROM CheckOutItems WHERE Id=6")
        
def delete_all_items():
    sure = raw_input("Are you sure (y/n)?: ")
    if sure == 'y':
        cur.execute("TRUNCATE CheckOutItems")
        print("Table truncated")
    else:
        print("Cancelling")



add_item()

deactivate_item()

print_items()

