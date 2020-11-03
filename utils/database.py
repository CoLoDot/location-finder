#! /usr/bin/env python
import logging
import os
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)


shot_40_44 = (
    "CREATE TABLE `shot_40_44` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(60),"
    "  `birth_place` varchar(60),"
    "  `death_place` varchar(60),"
    "  `locations` varchar(1000),"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")


try:
    logging.info('Connexion to MySQL database : PENDING')

    cnx = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv(
            'DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    cursor = cnx.cursor()
    logging.info('Connexion to MySQL database : SUCCESS')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        logging.info("Something is wrong with your user name or password")
        exit(1)
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        logging.info('Database does not exist')
        exit(1)
    else:
        logging.error(err)
        exit(1)

try:
    logging.info("Creating table shot_40_44: PENDING")
    cursor.execute("DROP TABLE shot_40_44")
    cursor.execute(shot_40_44)
    logging.info("Creating table shot_40_44: SUCCESS")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        logging.info("Creating table shot_40_44: TABLE ALREADY EXISTS")
        cursor.execute("SHOW TABLES")
        for x in cursor:
            logging.info(" %s", x)
    else:
        logging.error(err.msg)
        exit(1)
