$( function() {
    $( "#datepicker" ).datepicker();
  } );

  $(document).ready(function() {  
    $("#add-agenda").on("click", function() {  
        $("#agenda-box").append('<input class="form-control agendas" type="text" placeholder="Agenda "><br>');  
    });  
    $("#delete-agenda").on("click", function() {  
        $("#agenda-box").children().last().remove();  
    });  
});  