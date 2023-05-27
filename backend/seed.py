from mysql.connector import MySQLConnection, Error as MySQLError, errorcode
from setup import config, DB_NAME

ARTISTS = [
    {"name": "Coldplay", "biography": "British rock band formed in 1996"},
    {
        "name": "Miles Teller",
        "biography": "American actor famous for his role in Top Gun Maverick.",
    },
    {"name": "One Republic", "biography": "American pop rock band formed in 2002"},
    {"name": "ADAAM", "biography": "Swedish rapper"},
    {
        "name": "Post Malone",
        "biography": "Post Malone is an American rapper, singer, and songwriter",
    },
    {"name": "Käärijä", "biography": "blah blah blah6"},
    {"name": "Jonas Blue", "biography": "English DJ, record producer and songwriter"},
    {"name": "Bolaget", "biography": "Swedish pop group formed in 2015"},
    {"name": "Jonas Brothers", "biography": "American pop rock band formed in 2005."},
    {
        "name": "Loreen",
        "biography": "Swedish pop singer and songwriter known for winning the Eurovision Song Contest in 2012 with her song Euphoria.",
    },
    {
        "name": "Charlie Puth",
        "biography": "Charlie Puth is an American singer, songwriter, and record producer",
    },
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
    {
        "title": "17",
        "artist_id": 4,
        "mp3_path": "/static/17.mp3",
        "cover_path": "https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=987&q=80",
    },
    {
        "title": "Candy Paint",
        "artist_id": 5,
        "mp3_path": "/static/candy-paint.mp3",
        "cover_path": "https://images.unsplash.com/photo-1604079628040-94301bb21b91?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80",
    },
    {
        "title": "Cha Cha Cha",
        "artist_id": 6,
        "mp3_path": "/static/cha-cha-cha.mp3",
        "cover_path": "https://images.unsplash.com/photo-1604076913837-52ab5629fba9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80",
    },
    {
        "title": "Fast Car",
        "artist_id": 7,
        "mp3_path": "/static/fast-car.mp3",
        "cover_path": "https://images.unsplash.com/photo-1557672172-298e090bd0f1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80",
    },
    {
        "title": "Ikväll igen",
        "artist_id": 8,
        "mp3_path": "/static/ikvall-igen.mp3",
        "cover_path": "https://images.unsplash.com/photo-1506259091721-347e791bab0f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80",
    },
    {
        "title": "Mourning",
        "artist_id": 5,
        "mp3_path": "/static/mourning.mp3",
        "cover_path": "https://images.unsplash.com/photo-1618005198919-d3d4b5a92ead?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1074&q=80",
    },
    {
        "title": "Waffle House",
        "artist_id": 9,
        "mp3_path": "/static/waffle-house.mp3",
        "cover_path": "https://images.unsplash.com/photo-1552083974-186346191183?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80",
    },
    {
        "title": "Summer Baby",
        "artist_id": 9,
        "mp3_path": "/static/summer-baby.mp3",
        "cover_path": "https://images.unsplash.com/photo-1561212044-bac5ef688a07?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80",
    },
    {
        "title": "Tattoo",
        "artist_id": 10,
        "mp3_path": "/static/tattoo.mp3",
        "cover_path": "https://images.unsplash.com/photo-1513346940221-6f673d962e97?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80",
    },
    {
        "title": "That's not how this works",
        "artist_id": 11,
        "mp3_path": "/static/thats-not-how-this-works.mp3",
        "cover_path": "https://images.unsplash.com/photo-1515405295579-ba7b45403062?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1160&q=80",
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


if __name__ == "__main__":
    cnx = MySQLConnection(**config)
    cursor = cnx.cursor()

    try:
        cursor.execute("USE {}".format(DB_NAME))
    except MySQLError as err:
        print(f"Database {DB_NAME} does not exists. Did you forget to run `setup.py`?")
        exit(1)

    print("Seeding complete!\n")

    initialize_toplist(cursor)

    for artist in ARTISTS:
        insert_artist(cursor, **artist)
    for song in SONGS:
        insert_song(cursor, **song)

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
