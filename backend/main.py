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


@app.get("/artists/{artist_id}")
async def get_artist(artist_id: int, response: Response):
    """Get all songs from the playlist with the playlist_id."""
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("USE {}".format(DB_NAME))

    cursor.execute(
        "SELECT A.id, A.name, A.biography FROM artists A WHERE A.id = %s", (artist_id,)
    )
    artist = cursor.fetchone()

    if artist is None:
        response.status_code = 404
        return {"message": "Playlist not found"}

    cursor.execute(
        "SELECT * FROM songs WHERE artist_id = %s ORDER BY played_times DESC",
        (artist_id,),
    )
    songs = cursor.fetchall()
    artist["songs"] = songs

    cursor.close()
    cnx.close()

    return artist


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
    body: CreatePlaylistPayload,  # why is this needed?
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
    return {"message": "Ok"}


@app.get("/playlists/{playlist_id}")
async def get_playlist(playlist_id: int, response: Response):
    """Get all songs from the playlist with the playlist_id."""
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("USE {}".format(DB_NAME))

    cursor.execute(
        "SELECT P.id, P.name, U.username as owner FROM playlists P "
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
async def delete_playlist(
    playlist_id: int,
    response: Response,
    authorization: Annotated[Union[str, None], Header()] = None,  # auth is a must.
):
    """Delete a playlist for an authenticated user"""

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("USE {}".format(DB_NAME))

    try:
        user = JSONDecoder().decode(authorization)
        cursor.execute(
            "SELECT VerifyUser(%s, NULL, %s) as verified",
            (user["id"], user["password"]),
        )
        # gets the element in the dict, which is 1 if user is verified, 0 if not
        if not cursor.fetchone()["verified"]:
            raise Exception
    except:
        response.status_code = 401
        return {"message": "Not authorized"}

    if user["id"] == 1:  # if admin, he can delete any.
        # for some reason this does not work for the global songs playlist
        cursor.execute(
            "DELETE FROM playlists WHERE id = %s",
            (playlist_id,),
        )
    else:
        cursor.execute(
            "DELETE FROM playlists WHERE id = %s AND user_id = %s",
            (playlist_id, user["id"]),
        )

    rows_deleted = cursor.rowcount
    if rows_deleted == 0:
        response.status_code = 400
        return {"message": "Such playlist does not exist, or you are not the owner."}

    cnx.commit()
    cursor.close()
    cnx.close()
    return {"message": "Ok"}


@app.put("/playlists/{playlist_id}/{song_id}")
async def add_song_to_playlist(
    playlist_id: int,
    song_id: int,
    response: Response,
    authorization: Annotated[Union[str, None], Header()] = None,
):
    """Put a song with song_id into a playlist with playlist_id"""
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("USE {}".format(DB_NAME))

    try:
        user = JSONDecoder().decode(authorization)
        cursor.execute(
            "SELECT VerifyUser(%s, NULL, %s) as verified",
            (user["id"], user["password"]),
        )

        if not cursor.fetchone()["verified"]:
            raise Exception

        # check if the user owns the playlist
        cursor.execute(
            "SELECT * FROM playlists WHERE id = %s AND user_id = %s",
            (playlist_id, user["id"]),
        )
        if cursor.fetchone() is None and user["id"] != 1:
            raise Exception
    except:
        response.status_code = 401
        return {"message": "Not authorized"}

    try:
        cursor.execute(
            "INSERT INTO playlist_songs (playlist_id, song_id) VALUES (%s, %s)",
            (playlist_id, song_id),
        )
    except MySqlError as err:
        if err.errno == errorcode.ER_DUP_ENTRY:
            response.status_code = 400
            return {"message": "Song already in playlist"}

        response.status_code = 500
        return {"message": "Something went wrong..."}

    cnx.commit()
    cursor.close()
    cnx.close()

    return {"message": "Ok"}


@app.delete("/playlists/{playlist_id}/{song_id}")
async def delete_song_from_playlist(
    playlist_id: int,
    song_id: int,
    response: Response,
    authorization: Annotated[Union[str, None], Header()] = None,
):
    """Delete a song with song_id from a playlist with playlist_id"""
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("USE {}".format(DB_NAME))

    try:
        user = JSONDecoder().decode(authorization)
        cursor.execute(
            "SELECT VerifyUser(%s, NULL, %s) as verified",
            (user["id"], user["password"]),
        )

        if not cursor.fetchone()["verified"]:
            raise Exception

        # check if the user owns the playlist
        cursor.execute(
            "SELECT * FROM playlists WHERE id = %s AND user_id = %s",
            (playlist_id, user["id"]),
        )
        if cursor.fetchone() is None and user["id"] != 1:
            raise Exception
    except:
        response.status_code = 401
        return {"message": "Not authorized"}

    cursor.execute(
        "DELETE FROM playlist_songs WHERE playlist_id = %s AND song_id = %s",
        (playlist_id, song_id),
    )

    rows_deleted = cursor.rowcount
    if rows_deleted == 0:
        response.status_code = 400
        return {"message": "Such song does not exist in this playlist"}

    cnx.commit()
    cursor.close()
    cnx.close()

    return {"message": "Ok"}


@app.put("/song/{song_id}")
async def register_play(
    song_id: int,
    response: Response,
    # authorization: Annotated[Union[str, None], Header()] = None, Maybe not needed?
):
    """Registers a play for a song with song_id"""
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("USE {}".format(DB_NAME))
    try:
        cursor.execute(
            "UPDATE songs SET played_times = played_times + 1 WHERE id = %s",
            (song_id,),
        )
    except MySqlError as err:
        print(err.errno)

    rows_updated = cursor.rowcount
    if rows_updated == 0:
        response.status_code = 400
        return {"message": "Such song does not exist"}

    cnx.commit()
    cursor.close()
    cnx.close()

    response.status_code = 201
    return {"message": "Ok"}


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
