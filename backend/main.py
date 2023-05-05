import mysql.connector
from fastapi import FastAPI
from setup import config, DB_NAME


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/songs")
async def songs():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("USE {}".format(DB_NAME))
    cursor.execute("SELECT * FROM songs")
    songs = cursor.fetchall()
    return songs
