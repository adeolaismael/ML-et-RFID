// Please see documentation at https://docs.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

// Write your JavaScript code.


/* Fonction pour afficher la liste déroulante */
function afficher() {
    var dropdown = document.getElementById("myDropdown");
    dropdown.classList.toggle("show");

}


/* Fermer la liste déroulante si on clique en dehors de celle-ci */
window.onclick = function (event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

   
var rangeInput = document.getElementById('hyperparameter1');
var rangeValue = document.getElementById('rangeValue');

// Fonction pour mettre à jour la valeur au fur et à mesure que le curseur est déplacé
rangeInput.addEventListener('input', function () {
    rangeValue.textContent = rangeInput.value;
});


var rangeInput2 = document.getElementById('hyperparameter2');
 var rangeValue2 = document.getElementById('rangeValue2');
 rangeInput2.addEventListener('input', function () {
    rangeValue2.textContent = rangeInput2.value;
 });




//var rangeInput3 = document.getElementById('hyperparameter3');
//var rangeValue3 = document.getElementById('rangeValue3');

// Fonction pour mettre à jour la valeur au fur et à mesure que le curseur est déplacé
//rangeInput3.addEventListener('input', function () {
   // rangeValue3.textContent = rangeInput3.value;
//});


$(document).ready(function () {
    $('.info-tooltip').tooltip();
});


