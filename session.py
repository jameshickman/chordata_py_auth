from chordata.server_env import ServerEnvironment
from chordata.util.tenant_prefix import tenant_prefix


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
        return [r, {'serviceOf': 'json'}]
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
