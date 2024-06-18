def getSignUp(db_pool, name, email, password):
    try:
        with db_pool.get_connection() as con:
            with con.cursor(dictionary = True) as cursor:
                cursor.execute("select id from account where email = %s",(email,))
                existing_user = cursor.fetchone()
                if existing_user : 
                    return "mailrepeat"
                cursor.execute("insert into account(name,email,password) values(%s,%s,%s)",(name,email,password))
                con.commit()
                data = {"ok": True}
                return data
    except Exception as e:
        print(f"Unhandled exception: {e}")
        return "error"
        