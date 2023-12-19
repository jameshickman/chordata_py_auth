from chordate.server_env import ServerEnvironment
from chordate.util.tenant_prefix import tenant_prefix


def authenticate(e: ServerEnvironment, s: dict):
    prefix = tenant_prefix(e)
    injector = e.get_injection_manager()
    AuthenticationModel = injector.get('apps.authentication.local_lib.m.authenticate', 'AuthenticationModel')
    AuthenticateController = injector.get('apps.authentication.local_lib.c.authenticate', 'AuthenticateController')
    controller = AuthenticateController(
        s,
        e.get_configuration(),
        [
            AuthenticationModel(
                e.get_database(),
                {
                    **e.get_configuration(),
                    **{'tenant': e.get_tenant()}
                }
            )
        ]
    )
    r = {
        "authenticated": False
    }
    mode = e.get_data_type()
    if mode == "POST" or mode == "JSON":
        data = e.get_data()
        values = {
            'username': data.get('username', {}).get('value'),
            'password': data.get('password', {}).get('value'),
            'tenant': e.get_tenant()
        }
        r = controller.do_post(values)
        if not r['authenticated']:
            if mode == "POST":
                r['failed_login'] = True
                r['forward_to'] = e.query.get('forward_to', '')
                forward_to = e.query.get('forward_to', '/')
                return {}, {"redirect": prefix + "/authentication/login?failed=1&forward_to=" + forward_to}
            else:
                return r, {'serviceOf': 'json'}
        else:
            e.get_event_manager().send("user_authenticated", r)
    if mode == "JSON":
        return r, {'serviceOf': 'json'}
    else:
        forward_to = e.query.get('forward_to', '/')
        return {}, {"redirect": forward_to}


def end_session(e: ServerEnvironment, s: dict):
    keys = s.keys()
    for key in list(keys):
        del s[key]
    return {}, {'serviceOf': 'json'}


def login(e: ServerEnvironment, s: dict):
    r = {}
    query_string = e.get_query()
    forward_to = query_string.get('forward_to', '')
    if query_string.get('failed'):
        r['failed_login'] = True
    if forward_to == '':
        forward_to = e.get_configuration().get('user_landing')
        if forward_to is None or forward_to == '':
            # forward_to = "/authentication/profile"
            forward_to = "/test/index"
    r['forward_to'] = forward_to
    r['prefix'] = tenant_prefix(e)
    return r, {'template': 'login.vtpl', 'type': 'text/html'}


def logout(e: ServerEnvironment, s: dict):
    keys = s.keys()
    for key in list(keys):
        del s[key]
    return {}, {"redirect": tenant_prefix(e) + "/authentication/login"}


def get_user_info(e: ServerEnvironment, s: dict):
    return s.get('user_info'), {'serviceOf': 'json'}


def update_my_info(e: ServerEnvironment, s: dict):
    from apps.authentication.local_lib.c.user import UserController
    rv = {
        'updated': False
    }
    injector = e.get_injection_manager()
    if e.get_data_type() == 'POST':
        User = injector.get('apps.authentication.local_lib.m.user', 'User')
        c = UserController(
            s,
            e.get_configuration(),
            [
                User(e.get_database(), e.get_configuration())
            ]
        )
        data = e.get_data()
        c.set_user_info(
            data.get('username', {}).get('value'),
            data.get('first_name', {}).get('value'),
            data.get('last_name', {}).get('value'),
            data.get('email', {}).get('value'),
            data.get('organization', {}).get('value'),
            data.get('phone_number', {}).get('value'),
            data.get('password', {}).get('value')
        )
        rv['updated'] = True
    return rv, {'serviceOf': 'json'}
