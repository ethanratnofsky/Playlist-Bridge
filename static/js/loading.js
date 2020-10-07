$(document).ready(function () {
    window.location.replace(
        $('#data').data('summary_url').concat('?session_id=', $('#data').data('session_id'))
    );
});