
$(document).ready(function() {

  //0



	// 1. 
  /*
   $('#newRecord').on('show.bs.modal', function (event) {
  	var button = $(event.relatedTarget) // Button that triggered the modal
  	var voice = button.data('voice') // Extract info from data-* attributes
  	// If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  	// Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  	var modal = $(this)
  	modal.find('.modal-title').text('New message to ' + voice)
  	modal.find('.modal-body input').val(recipient)
	});

   // 2. 
   // select following SEED or COLLECTIVE voice
   /* 
	$('#start_rec').click(function(){
		var e = document.getElementById("follow")
		var text = e.options[e.selectedIndex].text
		var value = e.options[e.selectedIndex].value
  		//show recording ing button
  	document.getElementById("rec_ing").setAttribute('style', '')
  		//hide record button
  	document.getElementById("start_rec").setAttribute('style', 'display: none')
  		// record
    var vv = "{{recording_list}}"
  	document.getElementById("demo").textContent = vv
	});
  */

/*
$("#id_username").change(function () {
      var form = $(this).closest("form");
      $.ajax({
        url: form.attr("data-validate-username-url"),
        data: form.serialize(),
        dataType: 'json',
        success: function (data) {
          if (data.is_taken) {
            alert(data.error_message);
          }
        }
      });

    });
*/


});

