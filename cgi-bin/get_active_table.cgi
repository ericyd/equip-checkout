#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import cgi
import jinja2 as j
import datetime

class GMT_7(datetime.tzinfo): 
    def utcoffset(self,dt): 
        #8 hours behind GMT 
        return datetime.timedelta(hours=-7) 
    def tzname(self,dt): 
        return "GMT -8" 
    def dst(self,dt): 
        return datetime.timedelta(minutes=60)  



def get_active():

    # Get cgi form fields and set location filter
    try:
        form = cgi.FieldStorage()
        filter = form["filter"].value
    except Exception, e:
        filter = "All"
    finally:
        if filter == "All":
            filter = ""
        else:
            filter = "AND Location='{f}'".format(f=filter)
    
    # Set Jinja templating variables
    env = j.Environment(loader=j.PackageLoader('html-templates', '/'))
    template = env.get_template("write_active_table.html")
    
    # Set date variable for "old" checkout items
    today = datetime.datetime
    tz = GMT_7()
    now = today.now(tz)
    delta = datetime.timedelta(days=1)
    old = now - delta #returns 12 weeks prior to today; use for filtering mysql

    
    
    tail = ""

    try:
        # database: ericydco_Checkout
        # User: ericydco_Equip
        # Pass: @X0l0t15*
        # Table: Equipment
        #    CREATE TABLE Equipment(Id INT PRIMARY KEY AUTO_INCREMENT, Item VARCHAR(20), Name VARCHAR(50), Location VARCHAR(10), CheckoutTime DATETIME, CheckinTime DATETIME, CheckinBy VARCHAR(15), Notes VARCHAR(100), Active INT, Psuid VARCHAR(20));
        con = mdb.connect('localhost', 'ericydco_Equip', '@X0l0t15*', 'ericydco_Checkout')
        with con:
            cur = con.cursor(mdb.cursors.DictCursor)
            
            cur.execute("USE ericydco_Checkout")
            cur.execute("SELECT * FROM Equipment WHERE Active=1 AND CheckoutTime <= '{date}' {location_filter} ORDER BY CheckoutTime DESC".format(date=old, location_filter=filter))
            
            old_rows = cur.fetchall()
            
            cur.execute("SELECT * FROM Equipment WHERE Active=1 AND CheckoutTime > '{date}' {location_filter} ORDER BY CheckoutTime DESC".format(date=old, location_filter=filter))
            
            new_rows = cur.fetchall()
            
            
            
        if len(new_rows) == 0 and len(old_rows) == 0:
            tail = """<div class="panel panel-default">
                        <div class="panel-body">
                        No active items
                        </div>
                        </div>"""
                        

        
    except mdb.Error, e:
        rows = ()
        tail = """<div class="alert alert-danger alert-dismissible" role="alert">
                <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <strong>Error:</strong> {0}: {1}
                </div>""".format(e.args[0],e.args[1])

    finally:
        
        if not len(new_rows) == 0:
            for r in old_rows:
                r['CheckoutTime'] = r['CheckoutTime'].strftime("%I:%M%p %m/%d/%Y")
                r['Item'] = r['Item'].upper()
            
            for r in new_rows:
                r['CheckoutTime'] = r['CheckoutTime'].strftime("%I:%M%p %m/%d/%Y")
                r['Item'] = r['Item'].upper()
                
            
        
        # Denotes content type
        print("Content-type:text/html\n\n")
        # renders the Jinja template with the data from MySQL Equipment table
        print(template.render({'new_rows':new_rows, 'old_rows':old_rows}))
        # Prints the tail (holder for errors)
        print(tail)
    
    return

if __name__ == "__main__":
    get_active()
