#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import cgi
import datetime
import pw

class GMT_7(datetime.tzinfo): 
    def utcoffset(self,dt): 
        #8 hours behind GMT 
        return datetime.timedelta(hours=-7) 
    def tzname(self,dt): 
        return "GMT -8" 
    def dst(self,dt): 
        return datetime.timedelta(minutes=60) 

def remove_item():
    
    tail = ""
    
    # Get variables from cgi GET (passed in the URL)
    try:
        
        form = cgi.FieldStorage()
        itemid = form["itemid"].value
        odin = form["odin"].value
        notes = form["notes"].value
        
    except Exception, e:
        tail = tail + e
        itemid = "test_id"
        odin = "test_odin"
        notes = "test_notes"
    
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
        database = pw.MySQL.database
        username = pw.MySQL.username
        password = pw.MySQL.password
        table = pw.MySQL.table
        #    CREATE TABLE Equipment(Id INT PRIMARY KEY AUTO_INCREMENT, Item VARCHAR(20), Name VARCHAR(50), Location VARCHAR(10), CheckoutTime DATETIME, CheckinTime DATETIME, CheckinBy VARCHAR(15), Notes VARCHAR(100), Active INT, Psuid VARCHAR(20));
        con = mdb.connect('localhost', username, password, database)
        with con:
            cur = con.cursor(mdb.cursors.DictCursor)
            
            cur.execute("USE {0}".format(database))
            
            #cur.execute("INSERT INTO Equipment(Location, Name, Item, Psuid, CheckoutTime, Active) VALUES('{Location}', '{Name}', '{Item}', '{Psuid}', '{CheckoutTime}', 1)".format(Location=location, Name=name, Item=item, Psuid=psuid, CheckoutTime=now))
            cur.execute("UPDATE Equipment SET Active=0, CheckinBy='{CheckinBy}', CheckinTime='{date}', Notes='{Notes}' WHERE Id={ID}".format(CheckinBy=odin, date=now, Notes=notes, ID=itemid) )
        
    except mdb.Error, e:
        tail = tail + """<div class="alert alert-danger alert-dismissible" role="alert">
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
    remove_item()
