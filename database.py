from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_CLIENT_CONNECTION'))
db = client.scraper
collection = db.olx_data

data = db.data