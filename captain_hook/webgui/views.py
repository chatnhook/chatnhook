import flask_login as login
import flask_admin as admin
from flask_admin import helpers, expose
from flask import redirect, url_for, request, render_template
from datetime import datetime
from loginform import LoginForm
import stub as stub


# Create customized index view class that handles login & registration
class AdminIndexView(admin.AdminIndexView):
    def __init__(self, *args, **kwargs):
        config = kwargs.pop('config')
        inspector = kwargs.pop('inspector')
        self.app_config = config
        self.inspector = inspector

        super(AdminIndexView, self).__init__(*args, **kwargs)

    def parseTime(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')

    def tuple_without(self, original_tuple, element_to_remove):
        new_tuple = []
        for s in list(original_tuple):
            print s
            if not s == element_to_remove:
                new_tuple.append(s)
        return tuple(new_tuple)

    def _stubs(self):
        self.nav = {
            "alerts": stub.get_alerts()
        }

        self.panelswells = {
            "accordion": stub.get_accordion_items(),
            "tabitems": stub.get_tab_items()
        }

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))

        self._stubs()
        self.header = 'Dashboard'
        self.db_inspections = self.inspector.get_inspections(5)
        return render_template('admin/pages/dashboard.html', admin_view=self, parseTime=self.parseTime)

    @expose('/ui/panelswells')
    def panelswells(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))

        self._stubs()
        self.header = "Panels Wells"
        return render_template('admin/pages/ui/panels-wells.html', admin_view=self)

    @expose('/configuration/comms')
    def comm_config(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))

        self._stubs()
        self.header = 'Comms configuration'
        return render_template('admin/pages/blank.html', admin_view=self)

    @expose('/configuration/services')
    def service_config(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))

        self._stubs()
        self.header = 'Service configuration'
        return render_template('admin/pages/configuration/services.html', admin_view=self)

    @expose('/configuration/projects')
    def project_config(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))

        self.header = 'Projects configuration'
        return render_template('admin/pages/blank.html', admin_view=self)

    @expose('/inspector')
    def webhook_inspector(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))

        self.header = 'Webhook inspector'
        self.db_inspections = self.inspector.get_inspections()
        return render_template('admin/inspections/list.html', admin_view=self, parseTime=self.parseTime)

    @expose('/inspector/show/<string:guid>')
    def webhook_inspector_show(self, guid):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))

        self.header = 'Inspecting webhook'
        inspection = self.inspector.get_inspection(guid)
        return render_template('admin/inspections/show.html', admin_view=self,
                               inspection=inspection, parseTime=self.parseTime)

    @expose('/inspector/clear')
    def webhook_inspector_clear(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        self.inspector.clear_inspections()

        return redirect(url_for('.webhook_inspector'))


    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return render_template('admin/pages/login.html', form=form)

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


class BlankView(admin.BaseView):
    @expose('/')
    def index(self):
        return render_template('admin/pages/blank.html', admin_view=self)
