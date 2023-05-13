from mysql.connector import MySQLConnection, errorcode, Error as MySQLError

config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "password",
}


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
    ")"
)

TABLES["users"] = (
    "CREATE TABLE `users` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `username` varchar(255) NOT NULL,"
    "  `password` varchar(255) NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  UNIQUE KEY `username` (`username`)"
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

TABLES["users_playlists"] = (
    "CREATE TABLE `users_playlists` ("
    "  `playlist_id` int NOT NULL,"
    "  `user_id` int NOT NULL,"
    "  PRIMARY KEY (`playlist_id`),"  # one-to-many - a playlist is only created by one user
    "  FOREIGN KEY (`playlist_id`) REFERENCES `playlists` (`id`),"
    "  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)"
    ")"
)


def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
    except MySQLError as err:
        print(f"Failed creating database: {err}")
        exit(1)


def create_table(cursor, name, query):
    try:
        print(f"Creating table {name}: ", end="")
        cursor.execute(query)
        print("OK")
    except MySQLError as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)


if __name__ == "__main__":
    cnx = MySQLConnection(**config)
    cursor = cnx.cursor()

    try:
        cursor.execute(f"USE {DB_NAME}")
    except MySQLError as err:
        print(f"Database {DB_NAME} does not exists.")
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print(f"Database {DB_NAME} created successfully.")
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    for table_name in TABLES:
        query = TABLES[table_name]
        create_table(cursor, table_name, query)

    cnx.commit()
    cursor.close()
    cnx.close()
