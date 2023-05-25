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

procedures = {}

procedures["CreateUser"] = ( # You can apperantly simply use the three quotes instead btw
    """CREATE PROCEDURE CreateUser(
	    IN inUsername VARCHAR(255),
        IN inPassword VARCHAR(255)
    )
    BEGIN
	    DECLARE userID INT;
    
        INSERT INTO users (username, password) VALUES (inUsername, inPassword);
        SELECT LAST_INSERT_ID() INTO userID;
        INSERT INTO playlists (name, user_id) VALUES ('Liked Songs', userID);
    
    END"""
)

functions = {}

functions['VerifyUser'] = (# Verifies password with user id or username. Returns 1 if pwd is correct
    """CREATE FUNCTION VerifyUser(
        id INT,
        name VARCHAR(255),
        password VARCHAR(255)
    ) 
    RETURNS int
    BEGIN
        DECLARE to_return INT;
        DECLARE table_password VARCHAR(255);

        SET to_return = 0;

        IF id IS NULL THEN
            SELECT users.password INTO table_password FROM users WHERE users.username = name;
        ELSEIF name IS NULL THEN
            SELECT users.password INTO table_password FROM users WHERE users.id = id;
        END IF;

        IF password = table_password THEN
            SET to_return = 1;
        ELSE
            SET to_return = 0;
        END IF;

        RETURN to_return;

    END"""
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

def create_procedure(cursor, name, query):
    try:
        print(f"Creating procedure {name}: ", end="")
        cursor.execute(query)
        print("OK")
    except MySQLError as err:
        if err.errno == errorcode.ER_SP_ALREADY_EXISTS:
            print("already exists.")
        else:
            print(err.msg)

def create_function(cursor, name, query):
    try:
        print(f"Creating function {name}: ", end="")
        cursor.execute(query)
        print("OK")
    except MySQLError as err:
        if err.errno == errorcode.ER_SP_ALREADY_EXISTS:
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

    for proc_name in procedures:
        query = procedures[proc_name]
        create_procedure(cursor, proc_name, query)

    for func_name in functions:
        query = functions[func_name]
        create_function(cursor, func_name, query)

    cnx.commit()
    cursor.close()
    cnx.close()
