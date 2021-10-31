from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
from typing import Optional
import os
from pydantic import BaseModel

load_dotenv()

db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASSWORD')

var_url = f'mongodb+srv://{db_user}:{db_pass}@cluster0.wlhbw.mongodb.net/py-fastapi?retryWrites=true&w=majority'

app = FastAPI()

client = MongoClient(var_url)

mydb = client['py-fastapi']
#books = mydb['books']
book_col = mydb['book_col']

class Book(BaseModel):
    author: str
    title: str
    nop: int

@app.get("/")
def read_root():
    return {"message": "Hello World!!"}
'''
@app.post("/Ins_Rec/{Auth_Name}", status_code=201)
def insert_record(Auth_Name: str) -> dict:
    record_dict = dict()
    record_dict = {
        "author": Auth_Name,
    }
    mydb.books.insert_one(record_dict)
    # I need to check for success here
    return {"message": "Success"}
'''

@app.post("/Insert", status_code=201)
async def insert_record(data: Book) -> dict:
    author = data.author
    title = data.title
    nop = data.nop
    print(author)
    print(title)
    print(nop)
    record_dict = dict()
    record_dict = {
        "author": author,
        "title": title,
        "nop": nop
    }
    mydb.book_col.insert_one(record_dict)

    return {"message": "Record added successfully"}

