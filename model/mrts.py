def getMrt(db_pool):
    try:
        with db_pool.get_connection() as con:
            with con.cursor() as cursor:
                cursor.execute("SELECT MRT, COUNT(MRT) AS count FROM spots GROUP BY MRT ORDER BY count DESC")
                results = cursor.fetchall()
            mrt_data = [result[0] for result in results]
            data = {"data": mrt_data}
            return data
    except Exception as e:
        print(f"Unhandled exception: {e}")
        return "error"