from mongoengine import connect
from urllib.parse import quote_plus
import configparser
import pathlib

config = configparser.ConfigParser()
config.read("config.ini")
file_config = pathlib.Path(__file__).parent.joinpath("config.ini")

config = configparser.ConfigParser()
config.read(file_config)

db_user = config.get("DB", "USER")
db_password = config.get("DB", "PASSWORD")
db_name = config.get("DB", "NAME")
db_domain = config.get("DB", "DOMAIN")
db_port = config.get("DB", "PORT")

connect(host=f"mongodb://{quote_plus(db_user)}:{quote_plus(db_password)}@{db_domain}/{db_name}?retryWrites=true&w=majority")
