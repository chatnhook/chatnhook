import flask_login as login
import flask_admin as admin
from flask_admin import helpers, expose
from flask import redirect, url_for, request, render_template

from loginform import LoginForm
import stub as stub

                       
# Create customized index view class that handles login & registration
class AdminIndexView(admin.AdminIndexView):

    def _stubs(self):
        self.nav = {
            "tasks" : stub.get_tasks(),
            "messages" : stub.get_messages_summary(),
            "alerts" : stub.get_alerts()
        }
        
        (cols, rows) = stub.get_adv_tables()
        (scols, srows, context) = stub.get_tables()
        
        self.tables = {
            "advtables" : { "columns" : cols, "rows" : rows },
            "table" : { "columns" : scols, "rows" : srows, "context" : context}
        }
        
        self.panelswells = {
            "accordion" : stub.get_accordion_items(),
            "tabitems" : stub.get_tab_items()
        }
            
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
            
        self._stubs()
        self.header = 'Dashboard'
        return render_template('admin/pages/dashboard.html', admin_view=self)
    
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
            
        self.header = 'Service configuration'
        return render_template('admin/pages/blank.html', admin_view=self)

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
        return render_template('admin/pages/blank.html', admin_view=self)


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
