def test_login(conn, username: str, password: str):
    from apps.authentication.local_lib.utility import strip_hex, hash_password
    from sqlalchemy.sql import text
    import datetime
    q = """
    SELECT
        id,
        user_name,
        email,
        password_hash,
        password_salt,
        local_login,
        first_name,
        last_name,
        phone,
        organization,
        active,
        created,
        last_login
    FROM authentication.user
    WHERE
        user_name = :user
        OR email = :user
    """
    statement = text(q)
    result = conn.execute(statement, {"user": username}).first()
    if result is None:
        return False
    pass_hash = strip_hex(str(str(result[3]).encode('utf-8')))
    salt = str(result[4]).encode('utf-8')
    hashed_password = strip_hex(str(hash_password(password, salt)))
    if str(pass_hash) != str(hashed_password):
        return False
    user_id = int(result[0])
    q = """
        UPDATE authentication.user
        SET last_login = :ts
        WHERE id = :id
    """
    statement = text(q)
    conn.execute(statement, {"ts": str(datetime.datetime.now().isoformat()), "id": int(user_id)})
    conn.commit()
    return {
        'id': int(result[0]),
        'user_name': str(result[1]),
        'email': str(result[2]),
        'local_login': bool(result[5]),
        'first_name': result[6],
        'last_name': result[7],
        'phone': result[8],
        'organization': result[9],
        'active': bool(result[10]),
        'created': result[11],
        'last_login': result[12]
    }


def load_user(conn, user_name: str):
    from sqlalchemy.sql import text
    q = """
    SELECT
        id,
        user_name,
        email,
        local_login,
        first_name,
        last_name,
        phone,
        organization,
        active,
        created,
        last_login
    FROM authentication.user
    WHERE user_name = :user
    """
    statement = text(q)
    result = conn.execute(statement, {"user": user_name}).first()
    if result is None:
        return False
    return {
        "id": result[0],
        "user_name": result[1],
        "email": result[2],
        "local_login": result[3],
        "first_name": result[4],
        "last_name": result[5],
        "phone": result[6],
        "organization": result[7],
        "active": result[8],
        "created": result[9],
        "last_login": result[10]
    }


def begin_email_reset(conn, user_email):
    from sqlalchemy.sql import text
    import uuid
    import datetime
    secret = str(uuid.uuid4())
    q = """
        UPDATE authentication.user SET
            reset_hash = :secret,
            reset_timestamp = :ts
        WHERE
            email = :email
    """
    statement = text(q)
    conn.execute(
        statement,
        {
            'secret': str(secret),
            'ts': str(datetime.datetime.now().isoformat()),
            'email': str(user_email)
        }
    )
    conn.commit()
    return secret


def get_reset_code_and_timestamp(conn, email: str):
    from sqlalchemy.sql import text
    q = """
        SELECT
            reset_hash,
            reset_timestamp
        FROM
            authentication.user
        WHERE
            email = :email
    """
    statement = text(q)
    result = conn.execute(statement, {"email": email}).first()
    if result is False:
        return False
    else:
        return {
            'hash': str(result[0]),
            'timestamp': str(result[1])
        }


def update_password(conn, email: str, password_hash: str, salt: str):
    from sqlalchemy.sql import text
    q = """
        UPDATE authentication.user SET
            password_hash = :password_hash,
            password_salt = :salt
        WHERE
            email = :email
    """
    statement = text(q)
    conn.execute(
        statement,
        {
            'password_hash': str(password_hash),
            'salt': str(salt),
            'email': str(email)
        }
    )
    conn.commit()
    return
