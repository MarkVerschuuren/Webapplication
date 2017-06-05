/**
 * Created by Mark Verschuuren on 19-5-2017.
 */
$("#FormParentHiddden" ).toggle();
$("#FormParentHiddden2" ).toggle();
$(function() {
    $( ".addbtn" ).click(function() {
        $("#FormParentHiddden" ).toggle();
        $(".addbtn").toggle();


    });
    $(".addbtn2").click(function () {
        $("#FormParentHiddden2" ).toggle();
        $(".addbtn2").toggle();

    })
});
