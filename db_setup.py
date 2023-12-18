def schema():
    return "authentication"


def setup(database):
    from sqlalchemy import Table, Column, ForeignKey, MetaData, Integer, String, Boolean, DateTime
    database.create_schema(schema())
    engine = database.get_engine()
    meta = MetaData(schema='authentication')

    Table(
        'user', meta,
        Column('id', Integer, primary_key=True, autoincrement=True, unique=True),
        Column('user_name', String(128)),
        Column('email', String(128)),
        Column('password_hash', String(256)),
        Column('password_salt', String(128)),
        Column('dav_password', String(128)),
        Column('local_login', Boolean()),
        Column('first_name', String(128)),
        Column('last_name', String(128)),
        Column('phone', String(128)),
        Column('organization', String(128)),
        Column('active', Boolean()),
        Column('created', DateTime()),
        Column('last_login', DateTime()),
        Column('reset_hash', String(128)),
        Column('reset_timestamp', DateTime())
    )

    Table(
        'roles', meta,
        Column('id', Integer, primary_key=True, autoincrement=True, unique=True),
        Column('name', String(32))
    )

    Table(
        'users_roles', meta,
        Column('user', ForeignKey("user.id")),
        Column('role', ForeignKey("roles.id"))
    )

    Table(
        'oauth', meta,
        Column('provider', String(128), primary_key=True),
        Column('client_id', String(255)),
        Column('secret', String(255)),
        Column('redirect', String(255))
    )

    meta.create_all(engine, checkfirst=True)
    init_roles(database)
    return


def init_roles(database):
    from apps.authentication.local_lib.models.roles import Roles
    sess = database.get_connection()
    roles = ['user', "owner", "manager"]
    for role in roles:
        existing = sess.query(Roles).filter(Roles.name == role).first()
        if existing is None:
            new_role = Roles(name=role)
            sess.add(new_role)
            sess.commit()
    sess.close()
    return
