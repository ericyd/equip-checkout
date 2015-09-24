/**************************
 * jQuery
 * ************************/
$(document).ready(function() { //this declaration makes the below scripts capable of running before the page loads
    /* Behavior for "Inactive Items" table */
    $('.show_inactive_text:eq(1)').hide();
    
    $('#show_inactive_button').click(function() {
        $('#show_inactive_icon').toggleClass('glyphicon-plus-sign glyphicon-minus-sign');
        $('.show_inactive_text').toggle();
    });
    
    /* Event bindings */
    $("#refresh-entries").click(getActiveTable);
    $('#submit-button').click(function(event) {
        checkOut(event);
    });
    $("#check-out-form").submit(function(event) {
        checkOut(event);
    });
    
    function checkOut(event) {
        event.preventDefault();
        /* Check validity of form */
        
        var location = $("#id_location").val() == "";
        var name = $("#id_name").val() == "";
        var psuid = $("#id_psuid").val() == "";
        var numeric = !$.isNumeric( $("#id_psuid").val() );
        var start = "<div class='alert alert-danger alert-dismissible' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button>"
        var end = "</div>"
        
        if (location) {
            $("#add_item_errors").html(start + "Enter the user's name" + end);
        } else if (name) {
            $("#add_item_errors").html(start + "Select a location" + end);
        } else if (psuid) {
            $("#add_item_errors").html(start + "Enter the user's PSU ID" + end);
        } else if (numeric) {
            $("#add_item_errors").html(start + "PSU ID must contain only numbers" + end);
        } else {
            /* otherwise add item */
            addItem();
            $("#check-out-form")[0].reset();
            $("#add_item_errors").html("");
        }
        
        
    }
    
    /*****************
     * Check in form
     * ****************/
    $(".item-options").hide();
    $(".item-options.visible").show();
    
    /* Change Item options based on location selection */
    $("#id_location").change(function(event) {
        
        $(".item-options").hide();
        $(".item-options").removeClass("visible");
        
        var location = $(this).val();
        
        if (location == 1) {
            $("#ml115-items").show();
            $("#ml115-items").addClass("visible");
        } else if (location == 2) {
            $("#idsc-items").show();
            $("#idsc-items").addClass("visible");
        } else if (location == 3) {
            $("#frinq-items").show();
            $("#frinq-items").addClass("visible");
        } else if (location == 4) {
            $("#sinq-items").show();
            $("#sinq-items").addClass("visible");
        } else if (location == 5) {
            $("#icc-items").show();
            $("#icc-items").addClass("visible");
        } else if (location == 6) {
            $("#nh461-items").show();
            $("#nh461-items").addClass("visible");
        } else {
            $(".item-options").hide();
            $(".item-options").removeClass("visible");
            $("#select-location").show();
        }
    });
    
    
    /********************
     * Modal: return item
     * *****************/
    
    /* Something for proper modal functioning in bootstrap */
    $('#myModal').on('shown.bs.modal', function () {
        $('#myInput').focus();
    });
    
    /* Customize modal to display text relevant to returned item */
    $('#return-modal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var itemid = button.data('itemid'); // Extract info from data-itemid attribute
        var title = button.attr('title'); // Extract info from title attribute
        // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
        // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
        var modal = $(this);
        modal.find('.modal-title').text(title);
        modal.find('.modal-body #return-id').val(itemid);
    });
    
    /* make input button react the same as button click */
    var form = $('#return-modal').find( "form" ).on( "submit", function( event ) {
      event.preventDefault();
      returnItem();
      $('#return-modal').modal('hide');
    });
    
    /* Call function on "return" button press */
    $('#return-item-button').on("click", function() {
        returnItem();
        // hide modal
        $('#return-modal').modal('hide');
    });
    
    /* Reset modal on close */
    $('#return-modal').on('hide.bs.modal', function (e) {
        var form = $('#return-form');
        form[0].reset();
    })
    

    
    /* set behavior for location selector buttons */
    $('.active-item-location').on("click", function() {
        $('.active-item-location').removeClass('active');
        $(this).addClass('active');
        getActiveTable();
    });
    
    $('.inactive-item-location').on("click", function() {
        $('.inactive-item-location').removeClass('active');
        $(this).addClass('active');
        getInactiveTable();
    });
    
    $('.inactive-item-duration').on("click", function() {
        $('.inactive-item-duration').removeClass('active');
        $(this).addClass('active');
        getInactiveTable();
    });

    /* Determine active Location selector */
    
    function getActiveLocation() {
        var filter = $('.active-item-location.active').text();
        return filter;
    }
    
    function getInactiveLocation() {
        var filter = $('.inactive-item-location.active').text();
        return filter;
    }
    
    function getInactiveDuration() {
        var filter = $('.inactive-item-duration.active').text();
        return filter;
    }
    



/******************************************
 * AJAX - scripting for database processing
 * ****************************************/

/* Global request variable for AJAX calls */
var request;

/* General AJAX call function */
function loadXMLDoc(url,cfunc) {
    if (window.XMLHttpRequest) {
        // code for IE7+, Firefox, Chrome, Opera, Safari
        request=new XMLHttpRequest();
    }
    else {
        // code for IE6, IE5
        request=new ActiveXObject("Microsoft.XMLHTTP");
    }
    request.onreadystatechange=cfunc;
    request.open("GET",url,true);
    request.send();
}

/* Get active table info and return to active_items div.  Call getInactiveTable() on completion */
function getActiveTable() {
    var filter = getActiveLocation();

    loadXMLDoc("cgi-bin/get_active_table.cgi?filter=" + filter + "&t=" + Math.random(),function() {
        if (request.readyState==4 && request.status==200) {
            document.getElementById("active_items").innerHTML=request.responseText;
            getInactiveTable();
        }
    });
}

/* Get inactive table info and return to inactive_items div */
function getInactiveTable() {
    var filter = getInactiveLocation();
    var duration = getInactiveDuration();

    loadXMLDoc("cgi-bin/get_inactive_table.cgi?filter=" + filter + "&duration=" + duration + "&t=" + Math.random(),function() {
        if (request.readyState==4 && request.status==200) {
            document.getElementById("inactive_items").innerHTML=request.responseText;
        }
    });
}

function addItem() {
    
    var location = document.getElementById("id_location").value;
    var item = $(".item-options.visible").val();
    var name = document.getElementById("id_name").value;
    var psuid = document.getElementById("id_psuid").value;
    
    var scriptURL = "cgi-bin/add_item.cgi?location=" + location  + "&item=" + item + "&name=" + name + "&psuid=" + psuid;
    
    loadXMLDoc(scriptURL,function() {
        if (request.readyState==4 && request.status==200) {
            document.getElementById("add_item_errors").innerHTML=request.responseText;
            getActiveTable();
        }
    });
    
}


function returnItem() {
    
    // get values and send to returnItem()
    var itemid = document.getElementById('return-id').value;
    var odin = document.getElementById('id_odin').value;
    var notes = document.getElementById('id_notes').value;
    
    if (notes == "") {
        notes = "%20"
    }
    
    var scriptURL = "cgi-bin/remove_item.cgi?itemid=" + itemid  + "&notes=" + notes + "&odin=" + odin;
    
    loadXMLDoc(scriptURL,function() {
        if (request.readyState==4 && request.status==200) {
            // Update tables
            getActiveTable();
            
            // Add errors if applicable
            document.getElementById("add_item_errors").innerHTML=request.responseText;
            
            // reset form
            var form = document.getElementById('return-form');
            form[0].reset();
        }
    });
    
}

/* Perform action on window load */
window.onload = getActiveTable();

});
