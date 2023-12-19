from chordate.interfaces.model import ModelBase


class User(ModelBase):
    def update(self,
               username: str,
               first_name: str,
               last_name: str,
               email: str = None,
               organization: str = None,
               phone_number: str = None,
               password: str = None):
        import uuid
        from apps.authentication.local_lib.table.user import set_user_info, update_password
        from apps.authentication.local_lib.utility import hash_password, strip_hex
        conn = self.database.get_connection()
        set_user_info(
            conn,
            username,
            first_name,
            last_name,
            email,
            organization,
            phone_number
        )
        salt = bytes(str(uuid.uuid4()), encoding="utf-8")
        password_hash = hash_password(password, salt)
        if password is not None and len(password) > 0:
            update_password(
                conn,
                email,
                password_hash,
                strip_hex(str(salt))
            )
        return
