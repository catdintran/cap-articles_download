

function makePostCall(url, data) { // here the data and url are not hardcoded anymore
   var json_data = JSON.stringify(data);

    return $.ajax({
        type: "POST",
        url: url,
        data: json_data,
        dataType: "json",
        contentType: "application/json;charset=utf-8"
    });
}

function callAjax(url, data, myDiv,needTable) { // here the data and url are not hardcoded anymore
	    return $.ajax({
	        type: "GET",
	        url: url,
	        data: data,
	        cur_div: myDiv,
	        showTable: needTable,
	        dataType: "json",
	        contentType: "application/json;charset=utf-8",
	        success: function(response,status) {
	        	//alert(response.data)
	        	var myDiv=$("#myBody");
	        	if (needTable) {
	        		showTable(response.data);
	        	} else {
	        		myDiv.html("<textarea rows='50' cols='100'> "+ response.data + " </textarea>");
	        	}
	        	return response.data;
	        }
	    });
	}

function displayAlphabet() {
	var hder=$("#alphabet");
	var text="<div class='pagination'><div class='pages'>";
	for (var i = 65; i <= 90; i++) {
	    text += "<a href='#' " + (i==65 ? "class='active'" : "" ) + " id='alpha_" + String.fromCharCode(i) +"' onclick='showDictAlpha(this.id)' > "+ String.fromCharCode(i) + " </a>" + "";
	}
	
	text += "</div></div>";
	hder.html(text);
}

function undisplayAlphabet() {
	$("#alphabet").html("");
}

function showDictAlpha(cur_alpha) {
	var myDiv=$("#myBody");
	myDiv.html("<div class='loader'></div>");
	callAjax("/cgi-bin/python-cgi.py",{"step":"alphabet","character":cur_alpha.split("alpha_")[1]},0,1) 
}

function showTable(dataJson) {
	var data = dataJson.split(" ', '");
	var myDiv=$("#myBody");
	var text = "<table border='1px solid red'>";
	text += "<tr>   <th>Terms</th>   <th>Definition</th> </tr>";
	for (var i=0; i< data.length; ++i) {
		lspl = data[i].split("': '");
		text += "<tr> <td> "+ lspl[0].replace(/{'/g,"") + "</td>" + "<td>" + lspl[1].replace(/'}/g,"") + "</td>"; 
	}	
	text += "</table>";
	myDiv.html(text);
	
}

function submitMyStep(cur_step) {
	var myDiv=$("#myBody");
	myDiv.html("<div class='loader'></div>");
	var hder=$("#main_header");
	var alphabet=$("#alphabet");
	if (cur_step.indexOf("clean_step") !=-1) {
		//alert("clean")
		callAjax("/cgi-bin/python-cgi.py",{"step":"clean"},cur_step,1) ;
		hder.html("3. Clean data");
		displayAlphabet();
	} else if (cur_step.indexOf("map_step") != -1) {
		//alert("map")
		callAjax("/cgi-bin/python-cgi.py",{"step":"map"},cur_step) ;
		hder.html("2. Map data");
		undisplayAlphabet();
	} else if (cur_step.indexOf("display_step") !=-1) {
		//alert("display")
		
	} else { // request step
		//alert("request")
		hder.html("1. Request");
		undisplayAlphabet();
		callAjax("/cgi-bin/python-cgi.py",{"step":"request"},cur_step) ;
		
	}
		
}
