#!/usr/bin/env python

import cgi
import cgitb
#cgitb.enable(display=0, logdir="/path/to/logdir")



if __name__ == "__main__":
    print("Content-type:text/html\n\n")
    print("""<table class="table">
    <tr>
        <th></th>
        <th>Item</th>
        <th>Location</th>
        <th>Name</th>
        <th>Check out time</th>
    </tr>
        <tr>
        <td>Return</td>
        <td>rudolf</td>
        <td>rudolf</td>
        <td>rudolf</td>
        <td>1:01PM 08/05/2015</td>
    </tr>
    </table>
    """)
    
