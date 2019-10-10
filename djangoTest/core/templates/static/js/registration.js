// Please see documentation at https://docs.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

// Write your JavaScript code.

$(document).ready(function(){

	var passCheck = function(){
    	$("#submitButton").attr("disabled", ($("#password").val().localeCompare($("#repPassword").val()) != 0) || ($("#password").val().length <= 0 || $("#repPassword").val().length <= 0));
    };

    $("#dashboard").hide();
    setTimeout(
    function()
    {
        $("#welcomeBanner").hide();
        $("#dashboard").show();
    }, 2000);

    console.log($("#password").val());
    passCheck();
    $("#password").on('input',passCheck);
    $("#repPassword").on('input',passCheck);
});
