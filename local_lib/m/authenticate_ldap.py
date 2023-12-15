from chordate.interfaces.database import BaseDatabase
from chordate.interfaces.model import ModelBase
from chordate.ldap.interface import DirectoryServices


class AuthenticationModel(ModelBase):
    directory_services = None

    def __init__(self, database: BaseDatabase = None, configuration: dict = None):
        super().__init__(database, configuration)
        self.directory_services = DirectoryServices(self.configuration)
        pass

    def login(self, username: str, password: str) -> (dict, bool):
        user_info = self.directory_services.test_credentials(username, password)
        return {
            'user_name': username,
            'email': username,
            'first_name': user_info['sn'][0],
            'last_name': user_info['givenName'][0]
        }

    def roles(self, username) -> dict:
        rv = {}
        tenants = self.directory_services.list_tenants()
        for tenant in tenants:
            rv[tenant[0]] = self.directory_services.get_groups(tenant[0], username)
        return rv

    def tenants(self, tenant: str):
        return self.directory_services.list_tenants()

