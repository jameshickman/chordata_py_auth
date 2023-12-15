from chordate.interfaces.controller import ControllerBase
from apps.authentication.local_lib.m.authenticate import AuthenticationModel


class AuthenticateController(ControllerBase):
    authenticationmodel = AuthenticationModel()

    def do_post(self, data: dict):
        r = {
            "authenticated": False
        }
        username = data.get('username')
        user_data = self.authenticationmodel.login(username, data.get('password'))
        if user_data is not False:
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
