#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import cgi
import datetime

class GMT_7(datetime.tzinfo): 
    def utcoffset(self,dt): 
        #8 hours behind GMT 
        return datetime.timedelta(hours=-7) 
    def tzname(self,dt): 
        return "GMT -8" 
    def dst(self,dt): 
        return datetime.timedelta(minutes=60) 

def add_item():
    
    tail = ""
    
    # Get variables from cgi GET (passed in the URL)
    try:
        form = cgi.FieldStorage()
        location = form["location"].value
        name = form["name"].value
        item = form["item"].value
        psuid = form["psuid"].value
        
        
        if location == "1":
            location = "ML 115"
        elif location == "2":
            location = "IDSC"
        elif location == "3":
            location = "FRINQ"
        elif location == "4":
            location = "SINQ"
        elif location == "5":
            location = "ICC"
        elif location == "6":
            location = "NH 461/5"
        else:
            location = "default"
            
    except Exception, e:
        tail = tail + e
        location = "test_loc"
        name = "test_name"
        item = "test_item"
        psuid = "test_psu"
    
    # set CheckoutTime
    
    # new datetime class
    today = datetime.datetime
    
    # method returns current datetime in current timezone
    tz = GMT_7()
    now = today.now(tz)
    
    #format the datetime
    # this returns in 24 clock mode
    # to format for 12-hour clock, use %I:%M:%S %p - %p includes am/pm
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    try:
        # database: ericydco_Checkout
        # User: ericydco_Equip
        # Pass: @X0l0t15*
        # Table: Equipment
        #    CREATE TABLE Equipment(Id INT PRIMARY KEY AUTO_INCREMENT, Item VARCHAR(20), Name VARCHAR(50), Location VARCHAR(10), CheckoutTime DATETIME, CheckinTime DATETIME, CheckinBy VARCHAR(15), Notes VARCHAR(100));
        con = mdb.connect('localhost', 'ericydco_Equip', '@X0l0t15*', 'ericydco_Checkout')
        with con:
            cur = con.cursor(mdb.cursors.DictCursor)
            
            cur.execute("USE ericydco_Checkout")
            
            cur.execute("INSERT INTO Equipment(Location, Name, Item, Psuid, CheckoutTime, Active) VALUES('{Location}', '{Name}', '{Item}', '{Psuid}', '{CheckoutTime}', 1)".format(Location=location, Name=name, Item=item, Psuid=psuid, CheckoutTime=now))
            
    except mdb.Error, e:
        tail = """<div class="alert alert-danger alert-dismissible" role="alert">
                <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <strong>Error:</strong> {0}: {1}
                </div>""".format(e.args[0],e.args[1])
        
    finally:
        # Denotes content type
        print("Content-type:text/html\n\n")
        # Prints the tail (holder for errors)
        print(tail)
    
    return

if __name__ == "__main__":
    add_item()
