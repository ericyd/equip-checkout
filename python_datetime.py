#The DATETIME type is used for values that contain both date and time parts. 
#MySQL retrieves and displays DATETIME values in ‘YYYY-MM-DD HH:MM:SS’ format. 
#The supported range is ‘1000-01-01 00:00:00′ to ‘9999-12-31 23:59:59′.

# When querying the inactive cells, do this
#SELECT * 
#FROM ctx_bookings 
#WHERE DATE(booking_time) <= '2012-12-28' AND Active = 0
#ORDER BY id DSC (or ASC if I want ascending)


import datetime

delta = datetime.timedelta(weeks=12)


# new datetime class
today = datetime.datetime
# method returns current datetime in current timezone
now = today.now()
#format the datetime
# this returns in 24 clock mode
# to format for 12-hour clock, use %I:%M:%S %p - %p includes am/pm
now = now.strftime("%Y-%m-%d %H:%M:%S")

notbefore = now - delta #returns 12 weeks prior to today; use for filtering mysql

cur.execute("INSERT INTO Books(Title, CheckoutTime) VALUES('War and Peace', '{checkout}')".format(checkout=now));

inactive_items = cur.execute("Select * FROM Books WHERE Date >= '{notbefore}' AND Active = 0".format(notbefore=notbefore));