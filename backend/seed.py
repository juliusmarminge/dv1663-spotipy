from mysql.connector import MySQLConnection, Error as MySQLError, errorcode
from setup import config, DB_NAME

ARTISTS = [
    {"name": "Coldplay", "biography": "blah blah blah"},
    {"name": "Miles Teller", "biography": "blah blah blah2"},
    {"name": "One Republic", "biography": "blah blah blah3"},
]

SONGS = [
    {
        "title": "Sky Full of Stars",
        "artist_id": 1,
        "mp3_path": "/static/sky-full-of-stars.mp3",
        "cover_path": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2370&q=80",
    },
    {
        "title": "Great Balls of Fire",
        "artist_id": 2,
        "mp3_path": "/static/great-balls-of-fire.mp3",
        "cover_path": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2128&q=80",
    },
    {
        "title": "I Ain't Worried",
        "artist_id": 3,
        "mp3_path": "/static/i-aint-worried.mp3",
        "cover_path": "https://images.unsplash.com/photo-1563089145-599997674d42?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2370&q=80",
    },
]


def insert_song(cursor, title, artist_id, mp3_path, cover_path):
    query = (
        "INSERT INTO songs (title, artist_id, mp3_path, cover_path) "
        "VALUES (%s, %s, %s, %s)"
    )

    values = (title, artist_id, mp3_path, cover_path)
    try:
        print(f"Inserting song '{title}': ", end="")
        cursor.execute(query, values)
        print("OK")
    except MySQLError as err:
        print(err)


def insert_artist(cursor, name, biography):
    query = "INSERT INTO artists (name, biography) VALUES (%s, %s)"

    values = (name, biography)
    try:
        print(f"Inserting artist '{name}': ", end="")
        cursor.execute(query, values)
        print("OK")
    except MySQLError as err:
        print(err)


def initialize_toplist(cursor):
    query = "INSERT INTO users (username, password) VALUES ('Spotipy', 'supersecretpassword')"
    try:
        print("Creating master admin: ", end="")
        cursor.execute(query)
        print("OK")
    except MySQLError as err:
        if err.errno == errorcode.ER_DUP_ENTRY:
            print("admin already exists")
            return
        print(err)

    user_id = cursor.lastrowid

    # Global Top Songs playlist
    try:
        query = f"INSERT INTO playlists (name, user_id) VALUES ('Global Top Songs', {user_id})"
        print("Creating Global Top Songs playlist: ", end="")
        cursor.execute(query)
        print("OK")
    except MySQLError as err:
        print(err)

    playlist_id = cursor.lastrowid
    # Add songs to playlist
    for song_id in range(1, len(SONGS) + 1):
        try:
            query = f"INSERT INTO playlist_songs (playlist_id, song_id) VALUES ({playlist_id}, {song_id})"
            cursor.execute(query)
        except MySQLError as err:
            print(err)


if __name__ == "__main__":
    cnx = MySQLConnection(**config)
    cursor = cnx.cursor()

    try:
        cursor.execute("USE {}".format(DB_NAME))
    except MySQLError as err:
        print(f"Database {DB_NAME} does not exists. Did you forget to run `setup.py`?")
        exit(1)

    for artist in ARTISTS:
        insert_artist(cursor, **artist)
    for song in SONGS:
        insert_song(cursor, **song)

    playlist_id = initialize_toplist(cursor)

    print("Seeding complete!\n")

    print("Songs:")
    query = "SELECT title, artists.name as artist_name FROM `songs` inner join `artists` on songs.artist_id = artists.id"
    cursor.execute(query)
    for title, artist_name in cursor.fetchall():
        print(f"  {title} by {artist_name}")

    try:
        print("Testing CreateUser('testuser', 'testpassword')..")
        cursor.execute("CALL CreateUser('testuser', 'testpassword')")
        print("Ok")
    except MySQLError as err:
        print(err.msg)

    cnx.commit()
