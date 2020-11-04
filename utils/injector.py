#! /usr/bin/env python
import logging
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)


def inject(data: dict, url: str) -> dict:
    cnx = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv(
            'DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    cursor = cnx.cursor()
    sql = "INSERT INTO shot_40_44 (first_name, locations, maitron_url) VALUES (%s, %s, %s)"

    val = (data.get('name'), ",".join(
        [x.get('location') for x in data.get('locations')]), url)
    cursor.execute(sql, val)
    cnx.commit()

    query = ("SELECT * FROM shot_40_44 WHERE first_name =%s")
    cursor.execute(query, (data.get('name'), ))

    for row in cursor:
        print(row)

    cursor.close()
