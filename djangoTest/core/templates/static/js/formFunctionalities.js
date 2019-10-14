$(document).ready(function(){

    var completeCheck = function(){
        var formCompleted = true;
        $(".requiredFormField").each(function(i, obj){
            if(formCompleted && $( this ).val() == ""){
                formCompleted = false;
            }else{
                return;
            }
        });
        $("#submitButton").attr("disabled", !formCompleted);
    };

    completeCheck();
    $("#password").on('input',completeCheck);
    $("#repPassword").on('input',completeCheck);
});

