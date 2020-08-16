$(document).ready(function(){
    $("#srcService").change(function () {
        $("#srcServiceIcon").attr({
            src: $(this).find("option:selected").data("img-src"),
            alt: $(this).find("option:selected").data("img-alt")
        });
    });

    $("#destService").change(function () {
        $("#destServiceIcon").attr({
            src: $(this).find("option:selected").data("img-src"),
            alt: $(this).find("option:selected").data("img-alt")
        });
    });
});