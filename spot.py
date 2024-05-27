import json
import mysql.connector
import re
def connect_mysql():
    con=mysql.connector.connect(
        user="root",
        password="betty520",
        host="localhost",
        database="spot"
    )
    return con

with open("data/taipei-attractions.json","r",encoding="utf-8")as file:
    data = json.load(file)
    results = data["result"]["results"]
    con=connect_mysql()
    
    with con.cursor() as cursor:
        for item in results:
            name = item["name"]
            category = item["CAT"]
            description = item["description"]
            address = item["address"].strip().replace(" ","")
            transpot = item["direction"]
            mrt = item["MRT"]
            lat = item["latitude"]
            lng = item["longitude"]
            images = item["file"].lower()
            pattern = r"https?://[^\s]+?\.jpg"
            jpg_urls = []
            matches = re.findall(pattern, images)
            jpg_urls.extend(matches)
            cursor.execute("INSERT INTO spots(name,category,description,address,transpot,mrt,lat,lng) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(name,category,description,address,transpot,mrt,lat,lng))
            con.commit()
            spot_id = cursor.lastrowid
            for img_url in jpg_urls:
                cursor.execute("INSERT INTO spot_imgs (img_id, img_url) VALUES(%s,%s)",(spot_id,img_url))
            con.commit()
  

