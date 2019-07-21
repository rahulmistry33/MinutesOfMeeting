$( function() {
    $( "#datepicker" ).datepicker();
  } );
  $(document).ready(function(){

    var counter = 2;
		
    $("#addButton").click(function () {
				
	if(counter>10){
            alert("Only 10 agendas allowed");
            return false;
	}   
		
	var newTextBoxDiv = $(document.createElement('div'))
	     .attr("id", 'TextBoxDiv' + counter);
                
	newTextBoxDiv.after().html('<label>Agenda '+ counter + ' : </label>' +
	      '<input type="text" name="textbox' + counter + 
	      '" id="textbox' + counter + '" value=""  ><br>');
            
     newTextBoxDiv.appendTo("#TextBoxesGroup");
     


				
	counter++;
     });

     $("#removeButton").click(function () {
	if(counter==1){
          alert("No more textbox to remove");
          return false;
       }   
        
	counter--;
			
        $("#TextBoxDiv" + counter).remove();
			
     });
    });

