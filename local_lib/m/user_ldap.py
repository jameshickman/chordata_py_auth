from chordataweb.interfaces.model import BaseModel


class User(BaseModel):
    def update(self,
               username: str,
               first_name: str,
               last_name: str,
               email: str = None,
               organization: str = None,
               phone_number: str = None,
               password: str = None):
        from chordataweb.ldap.interface import DirectoryServices
        ds = DirectoryServices(self.configuration)
        ds.connect(
            self.connection.get('ldap_bind_user'),
            self.connection.get('ldap_bind_password')
        )
        ds.update_user_fields(email,
                              {
                                  'sn': first_name,
                                  'givenName': last_name,
                                  'businessCategory': organization,
                                  'mobile': phone_number
                              }
                              )
        if password is not None and len(password) > 0:
            ds.update_password(email, password)
        return
