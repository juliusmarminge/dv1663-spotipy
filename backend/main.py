import mysql.connector
from fastapi import FastAPI
from setup import config, DB_NAME
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    cursor.close()
    cnx.close()
    return songs


@app.get("/playlists/{playlist_id}")
async def playlists(playlist_id: int):
    print(playlist_id + 1)

    return {"message": playlist_id}


class Playlist(BaseModel):
    name: str
    # user_id: int


@app.get("/playlists")
async def playlists():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("USE {}".format(DB_NAME))
    cursor.execute("SELECT * FROM playlists")
    songs = cursor.fetchall()
    cursor.close()
    cnx.close()
    return songs


@app.post("/playlists")
async def playlists(name: str):
    # Create a new playlist for a user
    print("HELLOO")
    # playlist = body.dict()

    USER_ID = 5

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("USE {}".format(DB_NAME))
    cursor.execute(
        "INSERT INTO playlists (name, user_id) VALUES (%s, %s)", (name, USER_ID)
    )
    cnx.commit()
    cursor.close()
    cnx.close()

    return "Ok"


@app.put("/playlists/{playlist_id}")
async def update_playlist(playlist_id: int):
    print(playlist_id + 1)

    return {"message": f"updating playlist {playlist_id}"}


@app.delete("/playlists/{playlist_id}")
async def delete_playlist(playlist_id: int):
    print(playlist_id + 1)

    return {"message": f"deleted playlist {playlist_id}"}
