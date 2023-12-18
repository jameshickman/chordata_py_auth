from chordate.interfaces.controller import ControllerBase
from apps.authentication.local_lib.m.authenticate import AuthenticationModel


class AuthenticateController(ControllerBase):
    authenticationmodel = AuthenticationModel()

    def do_post(self, data: dict):
        r = {
            "authenticated": False
        }
        roles = None
        username = data.get('username')
        password = data.get('password')
        user_data = self.authenticationmodel.login(username, password)
        if user_data is False and self.configuration.get('founder_username', None) is not None:
            """
            Check against the user defined in the configuration
            """
            if (username == self.configuration.get('founder_username')
                    and self.configuration.get('founder_password') == password):
                r['authenticated'] = True
                user_data = {
                    'user_name': username,
                    'email': self.configuration.get('founder_email', ''),
                    'first_name': self.configuration.get('founder_first_name', ''),
                    'last_name': self.configuration.get('founder_last_name', '')
                }
                roles = self.configuration.get('founder_roles').split(',')
        if user_data is not False:
            if roles is None:
                roles = self.authenticationmodel.roles(username)
            tenants = self.authenticationmodel.tenants(data.get('tenant'))
            r = {
                "authenticated": True,
                "user_data": user_data,
                "roles": roles,
                "tenants": tenants
            }
            self.session['user_data'] = user_data
            self.session['roles'] = roles
            self.session['tenants'] = tenants
        return r
