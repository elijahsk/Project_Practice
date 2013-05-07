
function initialize() {
  var myLatlng = new google.maps.LatLng(1.2991,103.8826);
  var mapOptions = {
    zoom: 12,
    center: myLatlng,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  }
  var map = new google.maps.Map(document.getElementById('mapcanvas'), mapOptions);

  var marker = new google.maps.Marker({
      position: myLatlng,
      map: map,
      title: 'Dunman High'
  });
}

google.maps.event.addDomListener(window, 'load', initialize);

    </script>
	<script>
$(document).ready(function() {
//// Start Contact Form ////
	$('#ajaxcontactform').submit(function(){$('input[type=submit]', this).attr('disabled', 'disabled');});
	
	
	$('#ajaxcontactform').submit(
	
		function parseResponse() {
	
			var usersname = $("#name");
			var usersemail = $("#email");
			var usersphonenumber = $("#phone");
			var usersmessage = $("#comment");
			var contactformid = $("#contactformid");
			var url = "contact.php";
			
				var emailReg = new RegExp(/^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i);
				var valid = emailReg.test(usersemail.val());
			 
				if(!valid) {
					$("#contactwarning").html('<p class="rejectionalert"><span>Your email is not valid!</span></p>').slideDown().delay(2000).slideUp();
					$('input[type=submit]', $("#ajaxcontactform")).removeAttr('disabled');
					return false;
				}
			
			  if (usersname.val() == "" || usersname.val() == "Please Insert Your Name") {				  
				   $("#contactwarning").html('<p class="rejectionalert"><span>Please Insert Your Name!</span></p>').slideDown().delay(2000).slideUp();
				   $('input[type=submit]', $("#ajaxcontactform")).removeAttr('disabled');
				   return false;			   
			  }
			  if (usersemail.val() == "" || usersemail.val() == "Please Insert Your Email") {
				   $("#contactwarning").html('<p class="rejectionalert"><span>Please Insert Your Email!</span></p>').slideDown().delay(2000).slideUp();
				   $('input[type=submit]', $("#ajaxcontactform")).removeAttr('disabled');
				   return false;
			  }
			  if (usersphonenumber.val() == "" || usersphonenumber.val() == "Please Insert Your Phone Number") {
				   $("#contactwarning").html('<p class="rejectionalert"><span>Please Insert Your Phone Number!</span></p>').slideDown().delay(2000).slideUp();
				   $('input[type=submit]', $("#ajaxcontactform")).removeAttr('disabled');
				   return false;
			  }
			  if (usersmessage.val() == "" || usersmessage.val() == "Please Leave A Message") {
				   $("#contactwarning").html('<p class="rejectionalert"><span>You forgot to leave a message!</span></p>').slideDown().delay(2000).slideUp();
				   $('input[type=submit]', $("#ajaxcontactform")).removeAttr('disabled');
				   return false;
			  }

					$.post(url,{ usersname: usersname.val(), usersemail: usersemail.val(), usersphonenumber: usersphonenumber.val(), usersmessage: usersmessage.val(), contactformid: contactformid.val() } , function(data) {
						$('#contactajax').html(data);
						$('#contactajax').slideDown().delay(3000).slideUp();
						$("#name").val('Please Insert Your Name');
						$("#email").val('Please Insert Your Email');
						$("#phone").val('Please Insert Your Phone Number');
						$("#comment").val('Please Leave A Message');
						$('input[type=submit]', $("#ajaxcontactform")).removeAttr('disabled');
					});
			  
		  }
	  
	  );
//// End Contact Form ////

 });

