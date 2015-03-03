
var mr_cursor, lr_cursor;

$('message-button').click(function() {

	var payload;

	if (lr_cursor) {
		payload = {
			time: lr_cursor.toJSON()
		}
	}

	$.get(
		'/sent/api/tickets', 
		payload
	).success(function(data) {

		console.log(data)
		// if(data){
  //               var len = data.length;
  //               var txt = "";
  //               if(len > 0){
  //                   for(var i=0;i<len;i++){
  //                       if(data[i].city && data[i].cStatus){
  //                           txt += "<tr><td>"+data[i].city+"</td><td>"+data[i].cStatus+"</td></tr>";
  //                       }
  //                   }
  //                   if(txt != ""){
  //                       $("#table").append(txt).removeClass("hidden");
  //                   }
  //               }
  //           }
  //       },
  //       error: function(jqXHR, textStatus, errorThrown){
  //           alert('error: ' + textStatus + ': ' + errorThrown);
  //       }
  //   });
  //   return false;//suppress natural form submission
});
		
		// TODO: handle if nothing returned

		mr_cursor = new Date(data.items[0].date)

		lr_cursor = new Date(data.items[data.items.length-1].date)
	})
})
