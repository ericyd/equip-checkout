/* Global request variable for AJAX calls */
var request;

/* General AJAX call function */
function loadXMLDoc(url,cfunc)
{
if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
    request=new XMLHttpRequest();
    }
else
    {// code for IE6, IE5
    request=new ActiveXObject("Microsoft.XMLHTTP");
    }
request.onreadystatechange=cfunc;
request.open("GET",url,true);
request.send();
}

/* Get active table info and return to active_items div.  Call getInactiveTable() on completion */
function getActiveTable()
{
loadXMLDoc("cgi-bin/get_active_table.cgi?t=" + Math.random(),function()
    {
        if (request.readyState==4 && request.status==200)
            {
            document.getElementById("active_items").innerHTML=request.responseText;
            getInactiveTable();
            }
    });
}

/* Get inactive table info and return to inactive_items div */
function getInactiveTable()
{
loadXMLDoc("cgi-bin/get_inactive_table.cgi",function()
    {
        if (request.readyState==4 && request.status==200)
            {
            document.getElementById("inactive_items").innerHTML=request.responseText;
            }
    });
}

function addItem() {
    
    var location = document.getElementById("id_location").value;
    var item = document.getElementById("item_id").value;
    var name = document.getElementById("id_name").value;
    var psuid = document.getElementById("id_psuid").value;
    
    var scriptURL = "cgi-bin/add_item.cgi?location=" + location  + "&item=" + item + "&name=" + name + "&psuid=" + psuid;
    
    loadXMLDoc(scriptURL,function()
    {
        if (request.readyState==4 && request.status==200)
            {
            document.getElementById("add_item_errors").innerHTML=request.responseText;
            getActiveTable();
            }
    });
    
}


function returnItem() {
    
    var location = document.getElementById("id_location").value;
    var item = document.getElementById("id_category").value;
    var name = document.getElementById("id_name").value;
    var psuid = document.getElementById("id_psuid").value;
    
    var scriptURL = "cgi-bin/remove_item.cgi?location=" + location  + "&item=" + item + "&name=" + name + "&psuid=" + psuid;
    
    loadXMLDoc(scriptURL,function()
    {
        if (request.readyState==4 && request.status==200)
            {
            document.getElementById("add_item_errors").innerHTML=request.responseText;
            getActiveTable();
            }
    });
    
}


/* jQuery to create modal dialog for item return*/
$(function() {

    var dialog, form;

    dialog = $( "#dialog-form" ).dialog({
      autoOpen: false,
      height: 300,
      width: 350,
      modal: true,
      
      buttons: {
        // this needs to have a valid function after it
        // but, that function can exist outside of jquery (e.g. AJAX)
        // Actually, this button isn't required at all, but it makes it a bit better looking
        "Return Item": nothing,
        Cancel: function() {
          dialog.dialog( "close" );
        }
      },
      close: function() {
        form[ 0 ].reset();
        allFields.removeClass( "ui-state-error" );
      }
    });
 
    form = dialog.find( "form" ).on( "submit", function( event ) {
      event.preventDefault();
      addUser();
    });
 
    $( ".return-item" ).button().on( "click", function() {
      dialog.dialog( "open" );
    });
    
    
  });

/* End jQuery modal dialog */

function nothing() {
    alert("shit");
 }






