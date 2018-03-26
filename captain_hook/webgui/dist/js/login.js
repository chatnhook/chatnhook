$(document).ready(function () {
    $('body').on('click', '#deniedBtn', function () {

        $.ajax({
            url: window.location.href+'/request-access',
            type: "POST",
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            success: function (result) {
                if (result.hasOwnProperty('success') && result.success) {
                    $('#denied').fadeOut(function () {
                       $('#request_pending').fadeIn();
                    });

                }
            },
            error: function (xhr, resp, text) {
                console.log(xhr, resp, text);
            }
        });
    });
    $('#login_container').fadeIn(1000);

});
