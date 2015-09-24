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



def get_inactive():
    
    # Get cgi form fields and set location filter
    try:
        form = cgi.FieldStorage()
        filter = form["filter"].value
        duration = form["duration"].value
    except Exception, e:
        filter = "All"
        duration = "Forever"
    finally:
        if filter == "All":
            filter = ""
        else:
            filter = "AND Location='{f}'".format(f=filter)
            
        if duration == "Forever":
            duration = 100000
        elif duration == "30 days":
            duration = 30
        elif duration == "90 days":
            duration = 90
        else:
            duration = 365
    
    # Set Jinja templating variables
    env = j.Environment(loader=j.PackageLoader('html-templates', '/'))
    template = env.get_template("write_inactive_table.html")
    
    # Set CheckinTime and create filter for old items
    
    # new datetime class
    today = datetime.datetime
    # method returns current datetime in current timezone
    tz = GMT_7()
    now = today.now(tz)
    delta = datetime.timedelta(days=duration)
    notbefore = now - delta #returns prior to today; use for filtering mysql


    tail = ""

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
            #  AND CheckoutTime >= '{date}' ORDER BY id DSC
            cur.execute("SELECT * FROM Equipment WHERE Active=0 AND CheckoutTime >= '{date}' {location_filter} ORDER BY CheckinTime DESC".format(date=notbefore, location_filter=filter) )
            #cur.execute("SELECT * FROM Equipment WHERE Active=0 ORDER BY Id ASC")
            
            rows = cur.fetchall()
            
        if len(rows) == 0:
            tail = """<div class="panel panel-default">
                        <div class="panel-body">
                        No active items
                        </div>
                        </div>"""
        
    except mdb.Error, e:
        #rows = [{'Id':0, 'Item':"LH - 9", 'Name':"Eric Dauenhauer", 'Location':"ML115",'CheckoutTime':"1:01PM 08/06/2015", 'CheckinTime':"5:00PM 8/25/2015",'CheckinBy':"dauen", 'Notes':""},
                #{'Id':1, 'Item':"LH - 11", 'Name':"Eric Dauenhauer", 'Location':"ML115",'CheckoutTime':"2:02PM 08/07/2015", 'CheckinTime':"5:00PM 8/25/2015",'CheckinBy':"dauen", 'Notes':"There isn't anything to say, but if there were, it would go here"}]
        rows = ()
        tail = """<div class="alert alert-danger alert-dismissible" role="alert">
                <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <strong>Error:</strong> {0}: {1}
                </div>""".format(e.args[0],e.args[1])
    finally:
        if not len(rows) == 0:
            for r in rows:
                r['CheckoutTime'] = r['CheckoutTime'].strftime("%I:%M%p %m/%d/%Y")
                r['CheckinTime'] = r['CheckinTime'].strftime("%I:%M%p %m/%d/%Y")
                r['Item'] = r['Item'].upper()
        
        # Denotes content type
        print("Content-type:text/html\n\n")
        # renders the Jinja template with the data from MySQL Equipment table
        print(template.render({'rows':rows}))
        # Prints the tail (holder for errors)
        print(tail)



if __name__ == "__main__":
    get_inactive()

