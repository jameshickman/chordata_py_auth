from chordata.interfaces.model import ModelBase


"""
Default implementation for pure database authentication.
Not suitable for multitenant where the session can span tenants.
If using URL based tenancy support, consider injecting an LDAP
implementation.
"""


class AuthenticationModel(ModelBase):
    def login(self, username: str, password: str):
        from apps.authentication.lib.table.user import test_login
        return test_login(self.connection, username, password)

    def roles(self, username):
        from apps.authentication.lib.table.roles import get_roles
        return {
            self.configuration['tenant']: get_roles(self.connection, username)
        }
