$(function () {

    $('#side-menu').metisMenu();

});

function notify(text, type) {
    if (!type) {
        type = 'success'
    }
    $.notify({
        // options
        message: text
    }, {
        // settings
        type: type,
        position: 'fixed',
        placement: {
            align: 'center'
        }
    });
}

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

    function getProjectName() {
        var project;
        if (window.location.href.indexOf('configuration/projects/') > 0) {
            project = window.location.href.split('configuration/projects/').pop();
            if (project == 'new') {
                project = $('#new_project_name').val();
            }
        }
        return project
    }

    var url = window.location;
    var element = $('ul.nav a').filter(function () {
        return this.href == url;
    }).addClass('active').parent().parent().addClass('in').parent();
    if (element.is('li')) {
        element.addClass('active');
    }

    $('[data-toggle="tooltip"]').tooltip();

    $('body').on('submit', '.project_edit_form', function (e) {
        e.preventDefault();
        if (!confirm('save?')) {
            return false;
        }
        var data = $(this).serializeJSON();
        var project_name = getProjectName()
        $.ajax({
            url: '/admin/configuration/projects/' + project_name,
            type: "POST",
            dataType: 'json',
            data: data,
            contentType: "application/json; charset=utf-8",
            success: function (result) {
                if (result.hasOwnProperty('success') && result.success) {
                    notify('Configuration saved!');
                    if ($('#new_project_name').length > 0) {
                        window.location.href = '/admin/configuration/projects/' + project_name
                    }
                }
            },
            error: function (xhr, resp, text) {
                console.log(xhr, resp, text);
            }
        });
    });

    $('#addServiceModal').on('shown.bs.modal', function (e) {
        var height = 0;
        $('.service_col').each(function () {
            if ($(this).height() > height) {
                height = $(this).height();
            }
        });
        $('.service_col').height(height);
    });

    function disableServiceModalBtn() {
        var $btn = $('#addServiceModalBtn');
        $btn.attr("disabled", "disabled");
        $btn.attr('title', 'You need to enter a project name <br /> before you can add services.');
        $btn.data('html', true);
        $btn.tooltip();
    }
    var $newProjectInput = $('#new_project_name');
    if ($newProjectInput.length > 0) {
        var $btn = $('#addServiceModalBtn');
        if ($newProjectInput.val().trim() === '') {
            disableServiceModalBtn()
        }

        $newProjectInput.keyup(function () {
            if ($newProjectInput.val().trim() !== '') {
                $btn.removeAttr('disabled');
                $btn.tooltip('destroy');
            } else {
                disableServiceModalBtn();
            }
        });
    }

    $('body').on('click', '.service_col', function () {
        $('#addServiceModal').modal('hide');
        var project_name = getProjectName();
        var service = $(this).data('service');
        var abort;
        if ($newProjectInput.length > 0 && $newProjectInput.val().trim() === '') {
            notify('You need to enter a project name!', 'warning');
            abort = true;
        }

        $('[name="service_name"]').each(function () {
            if ($(this).val() == service) {
                notify('This service already exists!', 'warning');
                abort = true;
            }
        });
        if (abort) {
            return false;
        }
        var $addServiceBtn = $('#addServiceModalBtn');
        $addServiceBtn.text('Adding..');
        $addServiceBtn.attr("disabled", "disabled");
        $.ajax({
            url: '/admin/templates/' + project_name + '/' + service,
            type: "GET",
            contentType: "application/json; charset=utf-8",
            success: function (result) {
                $('#project-service-config').append(result);
                $addServiceBtn.removeAttr("disabled");
                $addServiceBtn.text('Add service');
            },
            error: function (xhr, resp, text) {
                console.log(xhr, resp, text);
            }
        });
    });


    $('.counter').counterUp({
        delay: 5,
        time: 1000
    });
});
