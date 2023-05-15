import mysql.connector
from mysql.connector import Error as MySqlError, errorcode
from fastapi import FastAPI, Response, Header
from setup import config, DB_NAME
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Annotated, Union
from json import JSONDecoder


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


@app.get("/playlists")
async def get_playlists(authorization: Annotated[Union[str, None], Header()] = None):
    """Get all public playlists. Include private playlists if authorization header is provided."""
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("USE {}".format(DB_NAME))

    try:
        user = JSONDecoder().decode(authorization)
        # select all public (from Spotipy) + private playlists from the user
        cursor.execute(
            "SELECT * FROM playlists WHERE user_id = %s OR user_id = 1", (user["id"],)
        )
    except:
        # select only public playlists from user 1 (Spotipy) if no authorization header is provided
        cursor.execute("SELECT * FROM playlists WHERE user_id = 1")

    songs = cursor.fetchall()
    cursor.close()
    cnx.close()
    return songs


class CreatePlaylistPayload(BaseModel):
    name: str


@app.post("/playlists")
async def create_playlist(
    body: CreatePlaylistPayload,
    response: Response,
    authorization: Annotated[Union[str, None], Header()] = None,
):
    """Create a new playlist for an authenticated user."""
    try:
        user = JSONDecoder().decode(authorization)
        print(user)
    except:
        response.status_code = 401
        return {"message": "Not authorized"}

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("USE {}".format(DB_NAME))
    cursor.execute(
        "INSERT INTO playlists (name, user_id) VALUES (%s, %s)",
        (body.name, user["id"]),
    )
    cnx.commit()
    cursor.close()
    cnx.close()
    return "Ok"


@app.get("/playlists/{playlist_id}")
async def get_playlist(playlist_id: int, response: Response):
    """Get all songs from the playlist with the playlist_id."""
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("USE {}".format(DB_NAME))

    cursor.execute(
        "SELECT name, user_id, username FROM playlists P "
        "   INNER JOIN users U ON P.user_id = U.id "
        "WHERE P.id = %s",
        (playlist_id,),
    )
    playlist = cursor.fetchone()

    if playlist is None:
        response.status_code = 404
        return {"message": "Playlist not found"}

    cursor.execute(
        "SELECT S.*, A.name as artist_name FROM playlist_songs PS "
        "   INNER JOIN songs S ON PS.song_id = S.id "
        "   INNER JOIN artists A ON S.artist_id = A.id "
        "WHERE playlist_id = %s",
        (playlist_id,),
    )
    songs = cursor.fetchall()
    playlist["songs"] = songs

    cursor.close()
    cnx.close()

    return playlist


@app.delete("/playlists/{playlist_id}")
async def delete_playlist(playlist_id: int):
    print(playlist_id + 1)

    return {"message": f"deleted playlist {playlist_id}"}


@app.put("/playlists/{playlist_id}/{song_id}")
async def add_song_to_playlist(playlist_id: int, song_id: int):
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


class UserPayload(BaseModel):
    id: int = None
    username: str
    password: str


@app.post("/users/signup")
async def create_user(body: UserPayload, response: Response):
    """Signs up a new user. Uses the `CreateUser` procedure to create a new user and give them a default playlist for their liked songs."""
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
    """Signs in a user by checking if the username and password match. No hashing or other security measures are taken, out of scope for this project."""
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
