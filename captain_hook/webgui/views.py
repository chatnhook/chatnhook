import json

import flask_login as login
import flask_admin as admin
import os
from flask_admin import expose
from flask import redirect, url_for, request, render_template, jsonify, session, send_from_directory
from datetime import datetime

from flask_dance.contrib.github import make_github_blueprint

from services import find_and_load_services
from comms import find_and_load_comms
from utils import config
from auth import UserNotFoundError, Authorization


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
        self.version = app.version
        self.services = find_and_load_services(self.app_config, None)
        self.comms = find_and_load_comms(self.app_config)

        self.app.config["GITHUB_OAUTH_CLIENT_ID"] = self.app_config.get('auth', {}).get('github',
                                                                                        {}).get(
            'client_id')
        self.app.config["GITHUB_OAUTH_CLIENT_SECRET"] = self.app_config.get('auth', {}).get(
            'github', {}).get('client_secret')

        github_bp = make_github_blueprint(redirect_url='/admin/')
        self.app.register_blueprint(github_bp, url_prefix="/admin/login")

        self.cache_service_events = {}

        super(AdminIndexView, self).__init__(*args, **kwargs)

    def parseTime(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')

    def set_user_data(self):
        if login.current_user.is_authenticated:
            self.logged_in_user = login.current_user.get_id()  # return username in get_id()
        else:
            self.logged_in_user = None  # or 'some fake value', whatever

    def get_service_events(self, service):
        if service not in self.cache_service_events:
            self.cache_service_events[service] = self.services[service].get_events()
            return self.cache_service_events[service]
        else:
            return self.cache_service_events[service]

    @expose('/dist/<path:path>')
    def send_dist(self, path):
        first_dir = path.split('/')[0]
        if first_dir in ['css', 'js', 'fonts', 'images']:
            return send_from_directory(os.path.join(self.app.root_path, 'webgui/dist'), path)
        else:
            return render_template('404.html'), 404

    @expose('/')
    def index(self):
        try:
            if not Authorization.is_authorized(self.app_config, 'github'):
                return redirect(url_for('.login_view'))
        except UserNotFoundError:
            return redirect(url_for('.login_view', error='denied'))
        self.set_user_data()

        self.header = 'Dashboard'
        self.db_inspections = self.inspector.get_inspections(5)
        self.db_hooklog = self.hook_log.get_logged_hooks(5)
        return render_template('admin/pages/dashboard.html', admin_view=self,
                               parseTime=self.parseTime)

    @expose('/log/inspector')
    def webhook_inspector(self):
        try:
            if not Authorization.is_authorized(self.app_config, 'github'):
                return redirect(url_for('.login_view'))
        except UserNotFoundError:
            return redirect(url_for('.login_view', error='denied'))
        self.set_user_data()

        self.header = 'Webhook inspector'
        self.db_inspections = self.inspector.get_inspections()
        return render_template('admin/inspections/list.html', admin_view=self,
                               parseTime=self.parseTime)

    @expose('/log/webhook-log')
    def webhook_log(self):
        try:
            if not Authorization.is_authorized(self.app_config, 'github'):
                return redirect(url_for('.login_view'))
        except UserNotFoundError:
            return redirect(url_for('.login_view', error='denied'))
        self.set_user_data()

        self.header = 'Recently processed webhooks'
        self.recent_hooks = self.hook_log.get_logged_hooks()
        return render_template('admin/webhooks/list.html', admin_view=self,
                               parseTime=self.parseTime)

    @expose('/inspector/show/<string:guid>')
    def webhook_inspector_show(self, guid):
        try:
            if not Authorization.is_authorized(self.app_config, 'github'):
                return redirect(url_for('.login_view'))
        except UserNotFoundError:
            return redirect(url_for('.login_view', error='denied'))
        self.set_user_data()

        self.header = 'Inspecting webhook'
        inspection = self.inspector.get_inspection(guid)
        return render_template('admin/inspections/show.html', admin_view=self,
                               inspection=inspection, parseTime=self.parseTime)

    @expose('/inspector/clear')
    def webhook_inspector_clear(self):
        try:
            if not Authorization.is_authorized(self.app_config, 'github'):
                return redirect(url_for('.login_view'))
        except UserNotFoundError:
            return redirect(url_for('.login_view', error='denied'))
        self.set_user_data()

        self.inspector.clear_inspections()

        return redirect(url_for('.webhook_inspector'))

    @expose('/webhook-log/clear')
    def webhook_processed_clear(self):
        try:
            if not Authorization.is_authorized(self.app_config, 'github'):
                return redirect(url_for('.login_view'))
        except UserNotFoundError:
            return redirect(url_for('.login_view', error='denied'))
        self.set_user_data()

        self.hook_log.clear_logged_hooks()

        return redirect(url_for('.webhook_log'))

    @expose('/configuration/telegram')
    def telegram_bot_config(self):
        try:
            if not Authorization.is_authorized(self.app_config, 'github'):
                return redirect(url_for('.login_view'))
        except UserNotFoundError:
            return redirect(url_for('.login_view', error='denied'))
        self.set_user_data()

        self.header = 'Telegram bot configuration'

        if request.method == 'POST':
            pass

        return render_template('admin/configuration/telegram.html', admin_view=self,
                               bot_config=self.app_config.get('services', {}).get('telegram'))

    @expose('/configuration/comms', ['GET', 'POST'])
    def comm_config(self):
        try:
            if not Authorization.is_authorized(self.app_config, 'github'):
                return redirect(url_for('.login_view'))
        except UserNotFoundError:
            return redirect(url_for('.login_view', error='denied'))

        self.set_user_data()

        self.header = 'Comms configuration'

        if request.method == 'POST':
            data = json.loads(request.data)
            data = data.get('comms', {})
            self.app_config['comms'] = data
            config.save_config(self.app_config)
            return jsonify({'success': True})

        return render_template('admin/configuration/comms.html', admin_view=self, comms=self.comms)

    @expose('/configuration/services', ['GET', 'POST'])
    def service_config(self):
        try:
            if not Authorization.is_authorized(self.app_config, 'github'):
                return redirect(url_for('.login_view'))
        except UserNotFoundError:
            return redirect(url_for('.login_view', error='denied'))
        self.set_user_data()

        self.header = 'Service configuration'

        if request.method == 'POST':
            data = json.loads(request.data)
            data = data.get('services', {})
            self.app_config['services'] = data
            config.save_config(self.app_config)
            return jsonify({'success': True})

        return render_template('admin/configuration/services.html', admin_view=self,
                               services=self.services)

    @expose('/configuration/inspector', ['GET', 'POST'])
    def inspector_config(self):
        try:
            if not Authorization.is_authorized(self.app_config, 'github'):
                return redirect(url_for('.login_view'))
        except UserNotFoundError:
            return redirect(url_for('.login_view', error='denied'))
        self.set_user_data()

        self.header = 'Inspector configuration'

        self.inspector_config_form = [
            {
                'name': 'enabled',
                'label': 'Enabled',
                'type': 'checkbox',
                'description': ''
            },
            {
                'name': 'inspect_hooks',
                'label': 'Inspect webhooks',
                'type': 'checkbox',
                'description': ''
            },
            {
                'name': 'verification_key',
                'label': 'Verification key',
                'type': 'text',
                'description': ''
            },
            {
                'name': 'forward_url',
                'label': 'Forward url',
                'type': 'text',
                'description': ''
            },
            {
                'name': 'allowed_methods',
                'label': 'Allowed methods',
                'type': 'array_checkbox',
                'values': [
                    {'label': 'GET', 'value': 'GET'},
                    {'label': 'POST', 'value': 'POST'},
                    {'label': 'PUT', 'value': 'PUT'},
                    {'label': 'PATCH', 'value': 'PATCH'},
                    {'label': 'DELETE', 'value': 'DELETE'},
                    {'label': 'COPY', 'value': 'COPY'},
                    {'label': 'HEAD', 'value': 'HEAD'},
                    {'label': 'OPTIONS', 'value': 'OPTIONS'},
                    {'label': 'LINK', 'value': 'LINK'},
                    {'label': 'UNLINK', 'value': 'UNLINK'},
                    {'label': 'PURGE', 'value': 'PR'},
                ],
                'description': ''
            },
        ]

        if request.method == 'POST':
            data = json.loads(request.data)
            data = data.get('inspector', {})
            self.app_config['inspector'] = data
            config.save_config(self.app_config)
            return jsonify({'success': True})

        return render_template('admin/configuration/inspector.html', admin_view=self,
                               form=self.inspector_config_form)

    @expose('/configuration/projects/new', ['GET', 'POST'])
    def new_project(self):
        self.header = 'Creating new project'

        comm_list = list(self.comms.keys())
        services_list = list(self.services.keys())
        return render_template('admin/configuration/projects/new.html',
                               admin_view=self,
                               comm_list=comm_list,
                               services_list=services_list
                               )

    @expose('/templates/<string:project_name>/<string:service>', ['GET', 'POST'])
    def get_template(self, project_name, service):
        try:
            if not Authorization.is_authorized(self.app_config, 'github'):
                return redirect(url_for('.login_view'))
        except UserNotFoundError:
            return redirect(url_for('.login_view', error='denied'))
        self.set_user_data()

        project = {
            service: {
                'send_to': {

                }
            }
        }
        return render_template('admin/configuration/projects/partials/project-panel.html',
                               admin_view=self,
                               comms=self.comms,
                               service=service,
                               services=self.services,
                               project=project,
                               project_name=project_name
                               )

    @expose('/configuration/projects/<string:project>', ['GET', 'POST'])
    def project_config(self, project):
        try:
            if not Authorization.is_authorized(self.app_config, 'github'):
                return redirect(url_for('.login_view'))
        except UserNotFoundError:
            return redirect(url_for('.login_view', error='denied'))
        self.set_user_data()

        if request.method == 'POST':
            data = json.loads(request.data)
            del data['service_name']
            if not self.app_config.get('hooks'):
                self.app_config['hooks'] = {}

            if not self.app_config.get('hooks', {}).get(project):
                self.app_config['hooks'][project] = {}

            self.app_config['hooks'][project] = data[project]
            config.save_config(self.app_config)
            print 'Config saved'
            return jsonify({'success': True})

        self.header = 'Editing project ' + project
        project_config = self.app_config.get('hooks', {}).get(project, {})

        comm_list = list(self.comms.keys())
        services_list = list(self.services.keys())
        services_list.remove('telegram')
        return render_template('admin/configuration/projects/edit_main.html',
                               admin_view=self,
                               project=project_config,
                               project_name=project,
                               comms=self.comms,
                               services=self.services,
                               comm_list=comm_list,
                               services_list=services_list
                               )

    @expose('/configuration/projects')
    def project_config_list(self):
        try:
            if not Authorization.is_authorized(self.app_config, 'github'):
                return redirect(url_for('.login_view'))
        except UserNotFoundError:
            return redirect(url_for('.login_view', error='denied'))
        self.set_user_data()

        self.header = 'Projects configuration'
        projects = self.app_config.get('hooks', {})
        return render_template('admin/configuration/projects/list.html', admin_view=self,
                               projects=projects)

    @expose('/configuration/users/')
    def user_config(self):
        try:
            if not Authorization.is_authorized(self.app_config, 'github'):
                return redirect(url_for('.login_view'))
        except UserNotFoundError:
            return redirect(url_for('.login_view', error='denied'))
        self.set_user_data()

        self.header = 'Projects configuration'
        auth_user_list = self.app_config.get('auth', {})
        return render_template('admin/configuration/users/list.html', admin_view=self,
                               auth_user_list=auth_user_list,
                               pending_auth_list=self.app.auth.get_pending_list()
                               )

    @expose('/configuration/users/accept', methods=['POST'])
    def user_config_accept(self):
        try:
            if not Authorization.is_authorized(self.app_config, 'github'):
                return redirect(url_for('.login_view'))
        except UserNotFoundError:
            return redirect(url_for('.login_view', error='denied'))
        self.set_user_data()
        if request.data:
            user_data = json.loads(request.data)

            if not self.app_config.get('auth', {}).get(user_data.get('auth_provider')):
                return jsonify({'success': False})

            allowed_users = self.app_config['auth'][user_data.get('auth_provider')]['allowed_users']
            if not user_data.get('id') in allowed_users:
                self.app_config['auth'][user_data.get('auth_provider')]['allowed_users'].append(
                    user_data.get('id'))
                self.app.auth.remove_user_from_pending_list(user_data.get('auth_provider'),
                                                            user_data.get('id'))
                config.save_config(self.app_config)
                return jsonify({'success': True})

        return jsonify({'success': False})

    @expose('/configuration/users/delete', methods=['POST'])
    def user_config_delete(self):
        try:
            if not Authorization.is_authorized(self.app_config, 'github'):
                return redirect(url_for('.login_view'))
        except UserNotFoundError:
            return redirect(url_for('.login_view', error='denied'))
        self.set_user_data()
        if request.data:
            user_data = json.loads(request.data)

            if not self.app_config.get('auth', {}).get(user_data.get('auth_provider')):
                return jsonify({'success': False})

            self.app.auth.remove_user_from_pending_list(user_data.get('auth_provider'),
                                                        user_data.get('id'))
            try:
                self.app_config['auth'][user_data.get('auth_provider')]['allowed_users'].remove(
                    user_data.get('id'))
            except ValueError:
                pass

            config.save_config(self.app_config)
            return jsonify({'success': True})

        return jsonify({'success': False})

    @expose('/login/<string:error>')
    @expose('/login/')
    def login_view(self, error=''):

        github_login = url_for("github.login")
        github_authenticated_user = None
        has_pending_request = None
        try:
            if Authorization.is_authorized(self.app_config, 'github'):
                return redirect(url_for('.index'))
        except UserNotFoundError as e:
            github_authenticated_user = e.user
            if self.app.auth.has_pending_request(e.user):
                has_pending_request = True
        return render_template('admin/login.html', github_login=github_login, error=error,
                               github_authenticated_user=github_authenticated_user,
                               has_pending_request=has_pending_request)

    @expose('/login/denied/request-access', methods=['POST'])
    def request_access(self):

        try:
            if Authorization.is_authorized(self.app_config, 'github'):
                return jsonify({'success': False})
        except UserNotFoundError as e:
            self.app.auth.add_user_to_pending_authorization(e.user)
            return jsonify({'success': True})

        return jsonify({'success': False})

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        session.clear()
        return redirect(url_for('.index'))
