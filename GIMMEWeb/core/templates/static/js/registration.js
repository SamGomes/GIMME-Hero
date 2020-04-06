$(document).ready(function(){

	var passCheck = function(){
    	$("#submitButton").attr("disabled", ($("#password").val().localeCompare($("#repPassword").val()) != 0) || ($("#password").val().length <= 0 || $("#repPassword").val().length <= 0));
    };

    passCheck();
    $("#password").on('input',passCheck);
    $("#repPassword").on('input',passCheck);
});