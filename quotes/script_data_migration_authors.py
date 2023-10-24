import psycopg2
from pymongo import MongoClient

# Подключение к MongoDB
mongo_client = MongoClient('mongodb+srv://amarakheo:AYwoHw8KHtGl9rgx@cluster0.wun00kb.mongodb.net/?retryWrites=true&w=majority')
mongo_db = mongo_client['library_app']
mongo_collection = mongo_db['author']

# Подключение к PostgreSQL
conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='567234'")
cur = conn.cursor()

# Извлечение данных из MongoDB и загрузка их в PostgreSQL
for record in mongo_collection.find():
    fullname = record['fullname']
    born_date = record['born_date']
    description = record['description']
    born_location = record['born_location']
    user_id = 1
    try:
        goodreads_url = record['goodreads_url']
    except:
        goodreads_url = None

    cur.execute(
        "INSERT INTO authorsapp_author (fullname, born_date, description, born_location, goodreads_url, user_id) VALUES (%s, %s, %s, %s, %s, %s)",
        (fullname, born_date, description, born_location, goodreads_url, user_id)
    )

conn.commit()
conn.close()