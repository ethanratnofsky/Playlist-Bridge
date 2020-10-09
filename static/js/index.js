$(document).ready(function () {
    $("#src-service").change(function () {
        $("#src-service-icon").attr({
            src: $(this).find("option:selected").data("img-src"),
            alt: $(this).find("option:selected").data("img-alt")
        });
    });

    $("#dest-service").change(function () {
        $("#dest-service-icon").attr({
            src: $(this).find("option:selected").data("img-src"),
            alt: $(this).find("option:selected").data("img-alt")
        });
    });
});