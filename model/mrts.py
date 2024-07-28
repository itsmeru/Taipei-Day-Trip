from sqlalchemy import text
async def getMrt(db):
    try:
        stmt = text("""
                SELECT MRT, COUNT(MRT) AS count 
                FROM spots 
                GROUP BY MRT 
                ORDER BY count DESC
            """)
            
        result = await db.execute(stmt)
        results = result.all()
        mrt_data = [result[0] for result in results]
        data = {"data": mrt_data}

            
        return data
    except Exception as e:
        print(f"Unhandled exception: {e}")
        return "error"