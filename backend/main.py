import mysql.connector
from mysql.connector import Error as MySqlError, errorcode
from fastapi import FastAPI, Response
from setup import config, DB_NAME
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/songs")
async def songs():
    """Get all songs"""
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("USE {}".format(DB_NAME))
    cursor.execute(
        "SELECT songs.*, artists.name as artist FROM songs INNER JOIN artists ON songs.artist_id = artists.id"
    )
    songs = cursor.fetchall()
    cursor.close()
    cnx.close()
    return songs


@app.get("/playlists") 
async def playlists():
    """Get all playlists"""

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("USE {}".format(DB_NAME))
    cursor.execute("SELECT * FROM playlists")
    songs = cursor.fetchall()
    cursor.close()
    cnx.close()
    return songs


class Playlist(BaseModel):
    name: str
    user_id: int


@app.post("/playlists")
async def playlists(playlist: Playlist):
    """Create a new playlist."""
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("USE {}".format(DB_NAME))
    cursor.execute(
        "INSERT INTO playlists (name, user_id) VALUES (%s, %s)",
        (playlist.name, playlist.user_id),
    )
    cnx.commit()
    cursor.close()
    cnx.close()
    return "Ok"


@app.get("/playlists/{playlist_id}")
async def playlists(playlist_id: int):
    """Get all songs from the playlist with the playlist_id."""
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("USE {}".format(DB_NAME))
    cursor.execute(
        "SELECT * FROM playlist_songs WHERE playlist_id = %s",
        (playlist_id,),
    )
    playlist_songs = cursor.fetchall()
    cursor.execute(
        "SELECT name, user_id FROM playlists WHERE id = %s",
        (playlist_id,),
    )
    playlist_songs.insert(0, cursor.fetchall()[0])
    cursor.close()
    cnx.close()
    return playlist_songs

@app.put("/playlists/{playlist_id}")
async def update_playlist(playlist_id: int):
    print(playlist_id + 1)

    return {"message": f"updating playlist {playlist_id}"}


@app.delete("/playlists/{playlist_id}")
async def delete_playlist(playlist_id: int):
    print(playlist_id + 1)

    return {"message": f"deleted playlist {playlist_id}"}

@app.post("/playlists/{playlist_id}/{song_id}")
async def playlists(playlist_id: int, song_id: int):
    """Put a song with song_id into a playlist with playlist_id"""
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("USE {}".format(DB_NAME))
    cursor.execute(
        "INSERT INTO playlist_songs (playlist_id, song_id) VALUES (%s, %s)",
        (playlist_id, song_id),
    )
    cnx.commit()
    cursor.close()
    cnx.close()

    return "Ok"

@app.get("/myPlaylists/{user_id}")
async def playlists(user_id: int):
    """Get all playlists created by user user_id"""
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("USE {}".format(DB_NAME))
    cursor.execute(
        "SELECT * FROM playlists WHERE user_id = %s",
        (user_id,),
    )
    playlists = cursor.fetchall()

    cursor.close()
    cnx.close()
    return playlists


class UserPayload(BaseModel):
    id: int = None
    username: str
    password: str


@app.post("/users/signup")
async def create_user(body: UserPayload, response: Response):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("USE {}".format(DB_NAME))
    try:
        cursor.execute(
            "CALL CreateUser(%s, %s)",
            (body.username, body.password),
        )
        cursor.execute("SELECT * FROM users WHERE username = %s", (body.username,))
        user = cursor.fetchone()
        cnx.commit()
    except MySqlError as err:
        if err.errno == errorcode.ER_DUP_ENTRY:
            response.status_code = 409
            return {"message": "User already exists"}
        else:
            print(err)
            response.status_code = 500
            return {"message": "Unknown error"}

    response.status_code = 201
    return {"message": "ok", "user": user}


@app.post("/users/signin")
async def login_user(body: UserPayload, response: Response):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("USE {}".format(DB_NAME))
    cursor.execute(
        "SELECT * FROM users WHERE username = %s AND password = %s",
        (body.username, body.password),
    )
    user = cursor.fetchone()

    if user is None:
        response.status_code = 401
        return {"message": "Invalid credentials"}

    response.status_code = 200
    return {"message": "ok", "user": user}
