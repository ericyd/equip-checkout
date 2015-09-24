I am trying to use AJAX to update a table with data returned from a Python script.  When I request the Python script using AJAX, the returned text is the entire python script file, not just the content in the `print` commands.  

My AJAX file:

    ...standard loadXMLDoc function with callback from W3C AJAX tutorial...


    function doNow()
    {

    loadXMLDoc("cgi-bin/get.py",function()
      {
      if (request.readyState==4 && request.status==200)
        {
        document.getElementById("active_items").innerHTML=request.responseText;
        }
      });
    }

    window.onload=doNow();


For simplicity, I've used python files as simple as:

    print("<div>something</div>")

When I load the page, the content of `<div id="active_items">` is:

    print("
    something
    ")

I have already:

 - Set the `get.py` file to executable using `chmod 755 get.py`
 - Verified that CGI privileges are enabled on my server (i.e. other .cgi
 - Verified that my AJAX script works with other static files, such as a `.txt` file

I'm sure I'm missing something obvious, but I would love some help!
