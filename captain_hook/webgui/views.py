import json

import flask_login as login
import flask_admin as admin
from flask_admin import helpers, expose
from flask import redirect, url_for, request, render_template, jsonify, make_response, session
from datetime import datetime

from flask_dance.contrib.github import make_github_blueprint, github

from loginform import LoginForm
from services import find_and_load_services
from comms import find_and_load_comms
from utils import config
import auth

# Create customized index view class that handles login & registration
class AdminIndexView(admin.AdminIndexView):
    def __init__(self, *args, **kwargs):
        config = kwargs.pop('config')
        inspector = kwargs.pop('inspector')
        hook_log = kwargs.pop('hook_log')
        app = kwargs.pop('app')
        self.app_config = config
        self.inspector = inspector
        self.hook_log = hook_log
        self.app = app
        self.logged_in_user = ''
        self.app.config["GITHUB_OAUTH_CLIENT_ID"] = self.app_config.get('auth', {}).get('github', {}).get('client_id')
        self.app.config["GITHUB_OAUTH_CLIENT_SECRET"] = self.app_config.get('auth', {}).get('github', {}).get('client_secret')

        github_bp = make_github_blueprint(redirect_url='/admin/')
        self.app.register_blueprint(github_bp, url_prefix="/admin/login")

        super(AdminIndexView, self).__init__(*args, **kwargs)

    def parseTime(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')

    @expose('/')
    def index(self):
        self.logged_in_user = auth.is_authorized(self.app_config, 'github')
        if not self.logged_in_user:
            return redirect(url_for('.login_view'))

        self.header = 'Dashboard'
        self.db_inspections = self.inspector.get_inspections(5)
        self.db_hooklog = self.hook_log.get_logged_hooks(5)
        return render_template('admin/pages/dashboard.html', admin_view=self,
                               parseTime=self.parseTime)


    @expose('/configuration/comms')
    def comm_config(self):
        self.logged_in_user = auth.is_authorized(self.app_config, 'github')
        if not self.logged_in_user:
            return redirect(url_for('.login_view'))

        self.header = 'Comms configuration'
        comms = find_and_load_comms(self.app_config)
        return render_template('admin/configuration/comms.html', admin_view=self, comms=comms)

    @expose('/configuration/services')
    def service_config(self):
        self.logged_in_user = auth.is_authorized(self.app_config, 'github')
        if not self.logged_in_user:
            return redirect(url_for('.login_view'))

        self.header = 'Service configuration'
        services = find_and_load_services(self.app_config, None)

        return render_template('admin/configuration/services.html', admin_view=self,
                               services=services)

    @expose('/configuration/projects/<string:project>', ['GET', 'POST'])
    def project_config(self, project):
        self.logged_in_user = auth.is_authorized(self.app_config, 'github')
        if not self.logged_in_user:
            return redirect(url_for('.login_view'))

        if request.method == 'POST':
            data = json.loads(request.data)
            service = data.get('service_name')
            del data['service_name']
            self.app_config['hooks'][project][service] = data
            config.save_config(self.app_config)
            print 'Config saved'
            return jsonify({'success': True})

        self.header = 'Editing project ' + project
        project_config = self.app_config.get('hooks', {}).get(project, {})
        services = find_and_load_services(self.app_config, None)
        comms = find_and_load_comms(self.app_config)

        return render_template('admin/configuration/projects/edit.html',
                               admin_view=self,
                               project=project_config,
                               project_name=project,
                               comms=comms,
                               services=services
                               )

    @expose('/configuration/projects')
    def project_config_list(self):
        self.logged_in_user = auth.is_authorized(self.app_config, 'github')
        if not self.logged_in_user:
            return redirect(url_for('.login_view'))

        self.header = 'Projects configuration'
        projects = self.app_config.get('hooks', {})
        return render_template('admin/configuration/projects/list.html', admin_view=self,
                               projects=projects)

    @expose('/inspector')
    def webhook_inspector(self):
        self.logged_in_user = auth.is_authorized(self.app_config, 'github')
        if not self.logged_in_user:
            return redirect(url_for('.login_view'))

        self.header = 'Webhook inspector'
        self.db_inspections = self.inspector.get_inspections()
        return render_template('admin/inspections/list.html', admin_view=self,
                               parseTime=self.parseTime)

    @expose('/webhook-log')
    def webhook_log(self):
        self.logged_in_user = auth.is_authorized(self.app_config, 'github')
        if not self.logged_in_user:
            return redirect(url_for('.login_view'))

        self.header = 'Recently processed webhooks'
        self.recent_hooks = self.hook_log.get_logged_hooks()
        return render_template('admin/webhooks/list.html', admin_view=self,
                               parseTime=self.parseTime)

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
        self.logged_in_user = auth.is_authorized(self.app_config, 'github')
        if not self.logged_in_user:
            return redirect(url_for('.login_view'))
        self.inspector.clear_inspections()

        return redirect(url_for('.webhook_inspector'))

    @expose('/webhook-log/clear')
    def webhook_processed_clear(self):
        self.logged_in_user = auth.is_authorized(self.app_config, 'github')
        if not self.logged_in_user:
            return redirect(url_for('.login_view'))
        self.hook_log.clear_logged_hooks()

        return redirect(url_for('.webhook_log'))

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):

        github_login = url_for("github.login")

        if auth.is_authorized(self.app_config, 'github'):
            return redirect(url_for('.index'))
        return render_template('admin/login.html', github_login=github_login)

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        session.clear()
        return redirect(url_for('.index'))


class BlankView(admin.BaseView):
    @expose('/')
    def index(self):
        return render_template('admin/pages/blank.html', admin_view=self)
