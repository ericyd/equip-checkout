/* add this to index.html
head:
<script src="js/ajax_refresh.js"></script>

body:
<button type="button" onclick="getActiveTable()">Refresh</button>

*/

function myTest() {
    document.getElementById("inactive_items_panel").innerHTML = "fuck";
}


/* This is the AJAX refresh function called by the "refresh" button */

/* FROM http://www.w3schools.com/ajax/ajax_xmlhttprequest_create.asp
All modern browsers support the XMLHttpRequest object (IE5 and IE6 use an ActiveXObject).

The XMLHttpRequest object is used to exchange data with a server behind the scenes. This means that it is possible to update parts of a web page, without reloading the whole page.
*/

/* EXAMPLES: http://www.w3schools.com/ajax/ajax_examples.asp */

/*If you have more than one AJAX task on your website, you should create ONE standard function for creating the XMLHttpRequest object, and call this for each AJAX task.*/
var req;

function loadXMLDoc(url, callback_func)
{
/* create the XMLHttpRequest instance */
    if (window.XMLHttpRequest) {
        // code for IE7+, Firefox, Chrome, Opera, Safari
        req = new XMLHttpRequest();
    } else {
        // code for IE6, IE5
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }

    //document.getElementById("active_items").innerHTML="part way";
    /* If the state of the 'req' changes, make sure its valid before pushing the data*/
    /* read this for more information on this function: http://www.w3schools.com/ajax/ajax_xmlhttprequest_onreadystatechange.asp */
    req.onreadystatechange = callback_func;
    
    
    /*To send a request to a server, we use the open() and send() methods of the XMLHttpRequest object:*/
    
    /*open(method,url,async) where method=GET | POST, url=location of file on server, async = TRUE | FALSE
        async should always be true for it to work as AJAX 
        When using async=true, specify a function to execute when the response is ready in the onreadystatechange event: [inserted above]*/
    
    req.open("GET",url,true);
    /*send(string) where string is only used for POST requests*/
    req.send();
} /*end loadXMLDoc()*/

function getActiveTable() {
    /* to avoid getting a cached result, we use the below URL to get a newer version
    if a cached version doesn't matter, then take off the "?t=...." part 
    If the URL is a script (e.g. asp, php, py) then the script will perform an action before sending data back*/
    var url = "ajax_text.txt";//?t=" + Math.random();
    /*call loadXMLDoc, which is a generic wrapped to create an XMLHttpRequest instance
    send it the URL to query for data, and the function to run on state change (defined below)
    This makes the code more modular, so if multiple AJAX requests need to be made, they can re-use the XMLHttpRequest function*/
    loadXMLDoc("ajax_text.txt", function() {
        if (req.readyState==4 && req.status==200) {
            /* change to whatever div you want to update */
            /*req.responseText for text reply, or req.responseXML.  XML needs to be parsed, though, so probably better to do text???*/
            document.getElementById("active_items").innerHTML=req.responseText;
            document.getElementById("myDiv").innerHTML=req.responseText;
        }
    });
    
    getInactiveTable();

}/*end getActiveTable()*/

function getInactiveTable() {
    /* to avoid getting a cached result, we use the below URL to get a newer version
    if a cached version doesn't matter, then take off the "?t=...." part 
    If the URL is a script (e.g. asp, php, py) then the script will perform an action before sending data back*/
    var url = "../cgi-bin/get_inactive_table.py"; //?t=" + Math.random()
    var url = "ajax_text.txt"; //?t=" + Math.random()
    /*call loadXMLDoc, which is a generic wrapped to create an XMLHttpRequest instance
    send it the URL to query for data, and the function to run on state change (defined below)
    This makes the code more modular, so if multiple AJAX requests need to be made, they can re-use the XMLHttpRequest function*/
    loadXMLDoc(url, function() {
        //document.getElementById("active_items").innerHTML="further";
        if (req.readyState==4 && req.status==200) {
            /* change to whatever div you want to update */
            /*req.responseText for text reply, or req.responseXML.  XML needs to be parsed, though, so probably better to do text???*/
            document.getElementById("inactive_items").innerHTML=req.responseText;
        }
    });

}/*end getInactiveTable()*/

window.onload = function() {
    //document.getElementById("active_items").innerHTML='hello';
    getActiveTable();
}
/* Call once so that the table is populated on page load ???? */
