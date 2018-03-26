$(document).ready(function () {
    $('.accept').click(function () {
        var data = $(this).data('user');
        var row = $(this).parent().parent().parent();
        $.ajax({
            url: document.location.pathname + 'accept',
            type: "POST",
            data: JSON.stringify(data),
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            success: function (result) {
                if (result.hasOwnProperty('success') && result.success) {
                    notify('User accepted');
                    row.find('td').slideUp(function () {
                        row.remove();
                    });
                }
            },
            error: function (xhr, resp, text) {
                console.log(xhr, resp, text);
            }
        });
    });

    $('.delete').click(function () {
        var btn = $(this);
        var data = btn.data('user');
        var row = $(this).parent().parent();
        if (btn.hasClass('auth')) {
            row = row.parent();
        }
        $.ajax({
            url: document.location.pathname + 'delete',
            type: "POST",
            data: JSON.stringify(data),
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            success: function (result) {
                if (result.hasOwnProperty('success') && result.success) {
                    if (btn.hasClass('auth')) {
                        notify('Authorization request deleted', 'danger');

                    } else {
                        notify('User deleted', 'danger');
                    }
                    row.find('td').slideUp(function () {
                        row.remove();
                    });

                }
            },
            error: function (xhr, resp, text) {
                console.log(xhr, resp, text);
            }
        });
    });
});
