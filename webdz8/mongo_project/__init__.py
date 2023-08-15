from pathlib import Path
from datetime import datetime
from mongo_project.connection import connection_to_mongo
import configparser
import psycopg2
import json
import redis
from redis_lru import RedisLRU
from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)
cache = RedisLRU(client)

config = configparser.ConfigParser()
config.read('config.ini')

db_user = config.get('DB', 'USER')
db_password = config.get('DB', 'PASSWORD')
db_name = config.get('DB', 'DB_NAME')
db_domain = config.get('DB', 'DOMAIN')
db_port = config.getint('DB', 'PORT')

def read_data(filename: str) -> list:
    try:
        with open(Path(__file__).parent.parent.joinpath(filename), 'r') as fh:
            return json.load(fh)
    except FileNotFoundError as e:
        print(e)
    return []

def connection_to_postgresql():
    connection = psycopg2.connect(
        user=db_user,
        password=db_password,
        host=db_domain,
        port=db_port,
        dbname=db_name
    )
    return connection

if __name__ == '__main__':
    connection_to_mongo()
    connection_to_postgresql()

    authors_file = "authors.json"
    quotes_file = "quotes.json"

    for author in read_data(authors_file):
        record = Author(
            fullname=author.get('fullname'),
            born_date=datetime.strptime(author.get('born_date'), "%B %d, %Y").date(),
            born_location=author.get('born_location'),
            description=author.get('description')
        ).save()

    for quote in read_data(quotes_file):
        author_name = quote.get('author')
        author = Author.objects(fullname=author_name).first()
        if author:
            record = Quote(
                tags=quote.get('tags'),
                author=author,
                quote=quote.get('quote')
            ).save()
