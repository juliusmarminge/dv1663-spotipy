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
    "  `played_times` int DEFAULT 0,"
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
    "  FOREIGN KEY (`playlist_id`) REFERENCES `playlists` (`id`) ON DELETE CASCADE,"
    "  FOREIGN KEY (`song_id`) REFERENCES `songs` (`id`)"
    ")"
)

views = {}

views['global_with_played'] = ( # shows the global playlist songs along with the their played_times
    """CREATE OR REPLACE VIEW global_with_played AS
	    SELECT playlist_songs.playlist_id, playlist_songs.song_id, songs.played_times
		    FROM playlist_songs
		    INNER JOIN songs ON playlist_songs.song_id = songs.id
		    WHERE playlist_songs.playlist_id = 1;"""
)

procedures = {}

procedures[
    "CreateUser"
] = """CREATE PROCEDURE CreateUser(
	    IN inUsername VARCHAR(255),
        IN inPassword VARCHAR(255)
    )
    BEGIN
	    DECLARE userID INT;
    
        INSERT INTO users (username, password) VALUES (inUsername, inPassword);
        SELECT LAST_INSERT_ID() INTO userID;
        INSERT INTO playlists (name, user_id) VALUES ('Liked Songs', userID);
    
    END"""  # You can apperantly simply use the three quotes instead btw

functions = {}

functions[
    "VerifyUser"
] = """CREATE FUNCTION VerifyUser(
        id INT,
        name VARCHAR(255),
        password VARCHAR(255)
    ) 
    RETURNS int
    READS SQL DATA
    BEGIN
        DECLARE table_password VARCHAR(255);

        IF id IS NULL THEN
            SELECT users.password INTO table_password FROM users WHERE users.username = name;
        ELSEIF name IS NULL THEN
            SELECT users.password INTO table_password FROM users WHERE users.id = id;
        END IF;

        IF password = table_password THEN
            RETURN 1;
        END IF;
        RETURN 0;

    END"""  # Verifies password with user id or username. Returns 1 if pwd is correct

triggers = {}

triggers['after_playlist_insert'] = ( #adds newly inserted song to global playlist if it has less than 10 songs.
    """CREATE TRIGGER after_insert_song
	AFTER INSERT ON songs
    FOR EACH ROW
    BEGIN
        DECLARE nr_of_songs INT;
        SELECT COUNT(playlist_songs.song_id)
            INTO nr_of_songs FROM playlist_songs 
            WHERE playlist_songs.playlist_id = 1;
        
        IF nr_of_songs < 10 THEN
            INSERT INTO playlist_songs(playlist_id, song_id)
            VALUES (1, NEW.id);
        END IF;
    END;"""

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

def create_view(cursor, name, query):
    try:
        print(f"Creating view {name}: ", end="")
        cursor.execute(query)
        print("OK")
    except MySQLError as err:
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


def create_trigger(cursor, name, query):
    try:
        print(f"Creating trigger {name}: ", end="")
        cursor.execute(query)
        print("OK")
    except MySQLError as err:
        if err.errno == errorcode.ER_TRG_ALREADY_EXISTS:
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

    for view_name in views:
        query = views[view_name]
        create_view(cursor, view_name, query)

    for proc_name in procedures:
        query = procedures[proc_name]
        create_procedure(cursor, proc_name, query)

    for func_name in functions:
        query = functions[func_name]
        create_function(cursor, func_name, query)

    for trig_name in triggers:
        query = triggers[trig_name]
        create_trigger(cursor, trig_name, query)

    cnx.commit()
    cursor.close()
    cnx.close()
