from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
from typing import Optional
import os
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASSWORD')

var_url = f'mongodb+srv://{db_user}:{db_pass}@cluster0.wlhbw.mongodb.net/py-fastapi?retryWrites=true&w=majority'


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient(var_url)

mydb = client['py-fastapi']
#books = mydb['books']
book_col = mydb['book_col']

class Book(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    author: str
    title: str
    nop: int

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

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

@app.get("/books")
async def get_books():
    books = []
    for book in mydb.book_col.find():
        books.append(Book(**book))
    print(books)
    return {'data': books}

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

