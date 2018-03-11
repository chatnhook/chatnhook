$(function () {

    $('#side-menu').metisMenu();

});

//Loads the correct sidebar on window load,
//collapses the sidebar on window resize.
// Sets the min-height of #page-wrapper to window size
$(function () {
    $(window).bind("load resize", function () {
        topOffset = 50;
        width = (this.window.innerWidth > 0) ? this.window.innerWidth : this.screen.width;
        if (width < 768) {
            $('div.navbar-collapse').addClass('collapse');
            topOffset = 100; // 2-row-menu
        } else {
            $('div.navbar-collapse').removeClass('collapse');
        }

        height = ((this.window.innerHeight > 0) ? this.window.innerHeight : this.screen.height) - 1;
        height = height - topOffset;
        if (height < 1) height = 1;
        if (height > topOffset) {
            $("#page-wrapper").css("min-height", (height) + "px");
        }
    });

    var url = window.location;
    var element = $('ul.nav a').filter(function () {
        return this.href == url;
    }).addClass('active').parent().parent().addClass('in').parent();
    if (element.is('li')) {
        element.addClass('active');
    }

    $('[data-toggle="tooltip"]').tooltip();

    $('.project_edit_form').submit(function (e) {
        e.preventDefault();
        var data = $(this).serializeJSON();
        $.ajax({
            url: window.location.href, // url where to submit the request
            type: "POST", // type of action POST || GET
            dataType: 'json', // data type
            data: data, // post data || get data
            contentType:"application/json; charset=utf-8",
            success: function (result) {
                // you can see the result from the console
                // tab of the developer tools
                console.log(result);
            },
            error: function (xhr, resp, text) {
                console.log(xhr, resp, text);
            }
        });
    })
});
