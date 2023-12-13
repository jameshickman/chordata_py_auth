def get_roles(conn, username: str):
    from sqlalchemy.sql import text
    rv = []
    q = """
    SELECT 
        r.name
    FROM
        authentication.user AS u,
        authentication.roles AS r,
        authentication.users_roles AS ur
    WHERE
        (u.user_name = :user OR u.email = :user)
        AND ur.user = u.id
        AND r.id = ur.role
    """
    statement = text(q)
    results = conn.execute(statement, {"user": username}).all()
    if len(results) > 0:
        for result in results:
            rv.append(result[0])
    return rv
