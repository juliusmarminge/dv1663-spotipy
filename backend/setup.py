import mysql.connector
from mysql.connector import errorcode

config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "password",
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()


DB_NAME = "spotipy"

TABLES = {}
TABLES["artists"] = (
    "CREATE TABLE `artists` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(255) NOT NULL,"
    "  `biography` varchar(255) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ")"
)

TABLES["songs"] = (
    "CREATE TABLE `songs` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `title` varchar(255) NOT NULL,"
    "  `artist_id` int NOT NULL,"
    "  `mp3_path` varchar(255) NOT NULL,"
    "  `cover_path` varchar(255) NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  FOREIGN KEY (`artist_id`) REFERENCES `artists` (`id`)"
    ")",
)

TABLES["users"] = (
    "CREATE TABLE `users` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `username` varchar(255) NOT NULL,"
    "  `password` varchar(255) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ")"
)

TABLES["playlists"] = (
    "CREATE TABLE `playlists` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(255) NOT NULL,"
    "  `user_id` int NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)"
    ")"
)

TABLES["playlist_songs"] = (
    "CREATE TABLE `playlist_songs` ("
    "  `playlist_id` int NOT NULL,"
    "  `song_id` int NOT NULL,"
    "  PRIMARY KEY (`playlist_id`, `song_id`),"  # don't allow duplicate songs in the same playlist
    "  FOREIGN KEY (`playlist_id`) REFERENCES `playlists` (`id`),"
    "  FOREIGN KEY (`song_id`) REFERENCES `songs` (`id`)"
    ")"
)

TABLES["artists_songs"] = (
    "CREATE TABLE `artists_songs` ("
    "  `artist_id` int NOT NULL,"
    "  `song_id` int NOT NULL,"
    "  PRIMARY KEY (`artist_id`, `song_id`),"  # the same artist doesn't publish the same song twice
    "  FOREIGN KEY (`artist_id`) REFERENCES `artists` (`id`),"
    "  FOREIGN KEY (`song_id`) REFERENCES `songs` (`id`)"
    ")"
)

TABLES["users_playlists"] = (
    "CREATE TABLE `users_playlists` ("
    "  `playlist_id` int NOT NULL,"
    "  `user_id` int NOT NULL,"
    "  PRIMARY KEY (`playlist_id`),"  # one-to-many - a playlist is only created by one user
    "  FOREIGN KEY (`playlist_id`) REFERENCES `playlists` (`id`),"
    "  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)"
    ")"
)


ARTISTS = [
    {"name": "Harold Faltermeyer", "biography": "blah blah blah"},
    {"name": "Miles Teller", "biography": "blah blah blah2"},
    {"name": "One Republic", "biography": "blah blah blah3"},
]

SONGS = [
    {
        "title": "Danger Zone",
        "artist": 1,
        "mp3_path": "/songs/song1.mp3",
        "cover_path": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2370&q=80",
    },
    {
        "title": "Great Balls of Fire",
        "artist": 2,
        "mp3_path": "/songs/song2.mp3",
        "cover_path": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2128&q=80",
    },
    {
        "title": "I Ain't Worried",
        "artist": 3,
        "mp3_path": "/songs/song3.mp3",
        "cover_path": "https://images.unsplash.com/photo-1563089145-599997674d42?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2370&q=80",
    },
]


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME)
        )
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


def insert_song(cursor, title, artist, mp3_path, cover_path):
    query = (
        "INSERT INTO songs (title, artist, mp3_path, cover_path) "
        "VALUES (%s, %s, %s, %s)"
    )

    values = (title, artist, mp3_path, cover_path)
    cursor.execute(query, values)


def insert_artist(cursor, name, biography):
    query = "INSERT INTO artists (name, biography) " "VALUES (%s, %s)"

    values = (name, biography)
    cursor.execute(query, values)


if __name__ == "__main__":
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end="")
            cursor.execute(table_description)
            cnx.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    # for song in SONGS:
    #     insert_song(cursor, **song)

    # for artist in ARTISTS:
    #     insert_artist(cursor, **artist)

    cnx.commit()

    # query = "SELECT title, artist FROM `songs`"
    # cursor.execute(query)

    # for title, artist in cursor:
    #     print("{} - {}".format(title, artist))

    cursor.close()
    cnx.close()
