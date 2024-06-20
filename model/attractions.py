def getAttractions(db_pool,start_index, items_per_page, keyword):
    try: 
        with db_pool.get_connection() as con:
            with con.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT  COUNT(*)  FROM spots WHERE MRT = %s OR name LIKE %s ", (keyword, '%' + keyword + '%'))
                results = cursor.fetchall()
                total_num = total_num = results[0]["COUNT(*)"]
                total_page = total_num / 12
                if not results:
                    return None,0
                
                cursor.execute("SELECT * FROM spots WHERE MRT = %s OR name LIKE %s LIMIT %s,%s", (keyword, '%' + keyword + '%', start_index, items_per_page))
                results = cursor.fetchall()
                for result in results:
                    id = result["id"]
                    cursor.execute("SELECT images FROM spot_imgs WHERE img_id = %s", (id,))
                    img_urls = [row["images"] for row in cursor.fetchall()]
                    result["images"] = img_urls
                return results,total_page
    except Exception as e:
        print(f"Unhandled exception: {e}")
        return "error"
