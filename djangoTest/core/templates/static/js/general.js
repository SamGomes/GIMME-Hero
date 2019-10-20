// Please see documentation at https://docs.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

// Write your JavaScript code.

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

    function closeModals() {
        rootEl.classList.remove('is-clipped');
        allModals.forEach(function (el) {
            el.classList.remove('is-active');
        });
    }

    // Functions
    function getAll(selector) {
        return Array.prototype.slice.call(document.querySelectorAll(selector), 0);
    }





    $("#dashboard").hide();
    setTimeout(
    function()
    {
        $("#welcomeBanner").hide();
        $("#dashboard").show();
    }, 2000);

    $(".minimizerButton").click(function(){
    	
    });

});
