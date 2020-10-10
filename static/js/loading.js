$(document).ready(function () {
    const meta_data =  $('#meta-data');
    window.location.replace(
        meta_data.data('summary_url').concat('?session_id=', meta_data.data('session_id'))
    );
});