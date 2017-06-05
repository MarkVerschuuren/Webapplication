/**
 * Created by Mark Verschuuren on 26-5-2017.
 */
var limit = 1;
$('input.checkboxkeuze').on('change', function(evt) {
   if($(this).siblings(':checked').length >= limit) {
       this.checked = false;
   }
});
$('input.checkboxkeuze2').on('change', function(evt) {
   if($(this).siblings(':checked').length >= limit) {
       this.checked = false;
   }
});
$('input.checkboxkeuze3').on('change', function(evt) {
   if($(this).siblings(':checked').length >= limit) {
       this.checked = false;
   }
});