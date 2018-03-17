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
    var $body = $('body');
    $(window).bind("load resize", function () {
        var topOffset = 50;
        var width = (this.window.innerWidth > 0) ? this.window.innerWidth : this.screen.width;
        if (width < 768) {
            $('div.navbar-collapse').addClass('collapse');
            topOffset = 100; // 2-row-menu
        } else {
            $('div.navbar-collapse').removeClass('collapse');
        }

        var height = ((this.window.innerHeight > 0) ? this.window.innerHeight : this.screen.height) - 1;
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

    function doPost(url, data, callback, errorCallback) {
        $.ajax({
            url: url,
            type: "POST",
            dataType: 'json',
            data: data,
            contentType: "application/json; charset=utf-8",
            success: callback,
            error: errorCallback
        });
    }

    var url = window.location;
    var element = $('ul.nav a').filter(function () {
        return this.href == url;
    }).addClass('active').parent().parent().addClass('in').parent();
    if (element.is('li')) {
        element.addClass('active');
    }


    $body.on('click', '.select-all', function () {
        $(this).select();
    });
    $body.on('click', '[data-copy]', function () {
        var targetId = "_hiddenCopyText_";
        var origSelectionStart, origSelectionEnd;
        // must use a temporary form element for the selection and copy
        target = document.getElementById(targetId);
        if (!target) {
            var target = document.createElement("textarea");
            target.style.position = "absolute";
            target.style.left = "-9999px";
            target.style.top = "0";
            target.id = targetId;
            document.body.appendChild(target);
            target.textContent = $(this).data('copy');
        }
        console.log($(this).data('copy'));
        // select the content
        var currentFocus = document.activeElement;
        target.focus();
        target.setSelectionRange(0, target.value.length);

        // copy the selection
        var succeed;
        try {
            succeed = document.execCommand("copy");
        } catch (e) {
            succeed = false;
        }
        // restore original focus
        if (currentFocus && typeof currentFocus.focus === "function") {
            currentFocus.focus();
        }
        target.textContent = "";
    });

    $('[data-toggle="tooltip"]').tooltip();

    $body.on('submit', '.project_edit_form', function (e) {
        e.preventDefault();
        if (!confirm('save?')) {
            return false;
        }
        var data = $('.project_edit_form').serializeJSON();
        var project_name = getProjectName();
        doPost('/admin/configuration/projects/' + project_name, data, function (result) {
            if (result.hasOwnProperty('success') && result.success) {
                notify('Configuration saved!');
                if ($('#new_project_name').length > 0) {
                    window.location.href = '/admin/configuration/projects/' + project_name
                }
            }
        });
    });

    $body.on('submit', '.comms_editing_form', function (e) {
        e.preventDefault();
        if (!confirm('save?')) {
            return false;
        }
        var data = $('.comms_editing_form').serializeJSON();
        var url = '/admin/configuration/comms';
        doPost(url, data, function (result) {
            if (result.hasOwnProperty('success') && result.success) {
                notify('Configuration saved!');
            }
        });
    });

    $body.on('submit', '.settings_editing_form', function (e) {
        e.preventDefault();
        if (!confirm('save?')) {
            return false;
        }
        var data = $('.settings_editing_form').serializeJSON();
        var url = '/admin/configuration/services';
        doPost(url, data, function (result) {
            if (result.hasOwnProperty('success') && result.success) {
                notify('Configuration saved!');
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

    $body.on('click', '.service_col', function () {
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
                result = result.replace('newpanel', 'in');
                $('.panel-collapse').removeClass('in');
                $('#project-service-config').append(result);
                $addServiceBtn.removeAttr("disabled");
                $addServiceBtn.text('Add service');
            },
            error: function (xhr, resp, text) {
                $addServiceBtn.removeAttr("disabled");
                $addServiceBtn.text('Add service');
                notify('Error while fetching service info', 'danger');
            }
        });
    });


    $('.counter').counterUp({
        delay: 5,
        time: 1000
    });
});
