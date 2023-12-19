HASH_ITERATIONS = 100000


def hash_password(password: str, salt: bytes):
    import hashlib
    import binascii
    secret = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        HASH_ITERATIONS
    )
    return binascii.hexlify(secret)


REQUIRED_PASSWORD_LENGTH = 12


def password_complexity_check(password: str):
    import re
    if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password)\
            and re.search(r'[0-9]', password) and len(password) < int(REQUIRED_PASSWORD_LENGTH):
        return True
    return False


def strip_hex(s):
    s = s[2:66]
    return s


def create_user(
        conn,
        user_name: str,
        email: str,
        password,
        first_name: str,
        last_name: str,
        phone: str,
        organization: str,
        roles: list
):
    import os
    import binascii
    from apps.authentication.local_lib.models.user import User
    from apps.authentication.local_lib.models.roles import Roles
    from apps.authentication.local_lib.models.usersroles import UsersRoles
    local_enabled = False
    if password is not False:
        salt = bytes(binascii.hexlify(os.urandom(32)))
        secret_hash = hash_password(str(password), salt)
        local_enabled = True
    else:
        salt = ''
        secret_hash = ''
    u = User(
        user_name=user_name,
        email=email,
        password_hash=secret_hash,
        password_salt=salt,
        local_login=local_enabled,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        organization=organization,
        active=True
    )
    conn.add(u)
    conn.commit()
    user_id = u.id
    for role in roles:
        r = conn.query(Roles).filter(Roles.name == str(role)).first()
        if r:
            ur = UsersRoles(
                user=user_id,
                role=r.id
            )
            conn.add(ur)
            conn.commit()
    return u
