$(document).ready(function(){

    // modals
    var rootEl = document.documentElement;
    var allModals = getAll('.modal');
    var modalButtons = getAll('.modal-button');
    var modalCloses = getAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button');

    if (modalButtons.length > 0) {
        modalButtons.forEach(function (el) {
            el.addEventListener('click', function () {
                var target = document.getElementById(el.dataset.target);
                rootEl.classList.add('is-clipped');
                target.classList.add('is-active');
            });
        });
    }

    if (modalCloses.length > 0) {
        modalCloses.forEach(function (el) {
            el.addEventListener('click', function () {
                closeModals();
            });
        });
    }

    document.addEventListener('keydown', function (event) {
            var e = event || window.event;
            if (e.keyCode === 27) {
                closeModals();
        }
    });

    var closeModals = function() {
        rootEl.classList.remove('is-clipped');
        allModals.forEach(function (el) {
            el.classList.remove('is-active');
        });
    }

    // general animations and element functionalities
    $("#dashboard").hide();
    setTimeout(
    function()
    {
        $("#welcomeBanner").hide();
        $("#dashboard").show();
    }, 1500);

    $(".minimizerButton").click(function(){
    	
    });

});

var getAll = function(selector) {
    return Array.prototype.slice.call(document.querySelectorAll(selector), 0);
}

var parseSessionAttribute = function(attributeStr){
    return JSON.parse(attributeStr.replace(/&quot;/g,"\""))
}
