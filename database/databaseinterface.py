import sqlite3
import utils.path_utils as PathUtils
from utils.singleton import Singleton


@Singleton
class DatabaseInterface(object):
    def __init__(self):
        self.connection = self.create_connection()
        self.connection.row_factory = sqlite3.Row

        self._is_setup = False

    def create_connection(self):
        db_file_path = PathUtils.get_user_data_file_path("bot_data.db")
        return sqlite3.connect(db_file_path)

    def execute_commands(self, commands: list[str]):
        if not self._is_setup:
            print("WARNING: setup_database() has not been called for this DatabaseInterface")

        try:
            with self.connection:
                for command in commands:
                    self.connection.execute(command)
        except sqlite3.IntegrityError:
            print("Failed to execute SQL commands. Rolling back...")

    def close_connection(self):
        # Other functions will commit their own changes, throw away everything else
        self.connection.rollback()
        self.connection.close()

    def setup_database(self):
        # Create all tables
        self.create_polls_table()
        self.create_poll_options_table()

        self._is_setup = True

    def reset_database(self):
        # WARNING: This will obliterate everything
        # You probably only want to use this in dev

        # 1. Drop poll_options table, as a dependent of polls
        # 2. Drop polls table

        try:
            with self.connection as conn:
                conn.execute("DROP TABLE IF EXISTS polloptions")
                conn.execute("DROP TABLE IF EXISTS polls")
        except sqlite3.DatabaseError:
            print("Failed to drop tables")

    # POLL OPERATIONS
    def create_polls_table(self):
        create_cmd = "CREATE TABLE IF NOT EXISTS polls (" \
                     "poll_id INTEGER PRIMARY KEY," \
                     "title TEXT NOT NULL," \
                     "creator_id INTEGER NOT NULL," \
                     "message_id INTEGER," \
                     "open BOOLEAN DEFAULT TRUE);"

        try:
            with self.connection as conn:
                conn.execute(create_cmd)
        except sqlite3.IntegrityError:
            print("ERROR: Could not create `polls` table")

    def create_poll_options_table(self):
        create_cmd = "CREATE TABLE IF NOT EXISTS polloptions (" \
                     "option_id INTEGER PRIMARY KEY," \
                     "option_emoji TEXT NOT NULL," \
                     "option_text TEXT NOT NULL," \
                     "poll_id INTEGER," \
                     "FOREIGN KEY(poll_id) REFERENCES polls(poll_id) ON UPDATE CASCADE ON DELETE CASCADE);"

        try:
            with self.connection as conn:
                conn.execute(create_cmd)
        except sqlite3.IntegrityError:
            print("ERROR: Could not create `poll_options` table")

    def get_latest_poll(self) -> sqlite3.Row:
        get_latest_cmd = "SELECT * FROM polls ORDER BY poll_id DESC LIMIT 1;"
        result = None

        try:
            with self.connection as conn:
                conn.execute(get_latest_cmd)
                result = conn.cursor().fetchone()
        except sqlite3.DatabaseError:
            print("ERROR: Failed to retrieve latest poll")

        return result

    def get_poll_by_id(self, poll_id) -> sqlite3.Row:
        get_cmd = "SELECT * FROM polls WHERE poll_id = :poll_id"
        data = {"poll_id": poll_id}
        result = None

        try:
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute(get_cmd, data)
                result = cursor.fetchone()
        except sqlite3.DatabaseError:
            print("ERROR: Failed to retrieve poll")

        return result

    def get_poll_title(self, poll_id) -> str:
        get_cmd = "SELECT title FROM polls WHERE poll_id = :poll_id"
        data = {"poll_id": poll_id}
        result = None

        try:
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute(get_cmd, data)
                result = cursor.fetchone()
        except sqlite3.DatabaseError:
            print("ERROR: Failed to retrieve poll")

        return result["title"]

    def get_poll_creator(self, poll_id) -> int:
        get_cmd = "SELECT creator_id FROM polls WHERE poll_id = :poll_id"
        data = {"poll_id": poll_id}
        result = None

        try:
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute(get_cmd, data)
                result = cursor.fetchone()
        except sqlite3.DatabaseError:
            print("ERROR: Failed to retrieve poll")

        return result["creator_id"]

    def get_poll_message_id(self, poll_id) -> int:
        get_cmd = "SELECT message_id FROM polls WHERE poll_id = :poll_id"
        data = {"poll_id": poll_id}
        result = None

        try:
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute(get_cmd, data)
                result = cursor.fetchone()
        except sqlite3.DatabaseError:
            print("ERROR: Failed to retrieve poll")

        return result["message_id"]

    def add_poll(self, title, creator_id, options) -> int:
        insert_poll_cmd = "INSERT INTO polls (title, creator_id)" \
                          "VALUES (:title, :creator_id)"
        data = {"title": title, "creator_id": creator_id}
        cursor = self.connection.cursor()
        poll_id = None

        try:
            with self.connection as conn:
                cursor.execute(insert_poll_cmd, data)
                poll_id = cursor.lastrowid
        except sqlite3.DatabaseError:
            print("ERROR: Failed to create new poll")
            return None

        insert_options_cmd = "INSERT INTO polloptions (option_emoji, option_text, poll_id)" \
                             "VALUES (:emoji, :text, :poll_id);"
        options_data = []

        for i in range(len(options)):
            options_data.append({"emoji": options[i][0], "text": options[i][1], "poll_id": poll_id})

        try:
            with self.connection as conn:
                cursor.executemany(insert_options_cmd, options_data)
        except sqlite3.DatabaseError:
            print("ERROR: Failed to create new poll options")

        return poll_id

    def assign_poll_message_id(self, poll_id, message_id):
        update_message_id_cmd = "UPDATE polls SET message_id = :message_id WHERE poll_id = :poll_id;"
        data = {"message_id": message_id, "poll_id": poll_id}

        try:
            with self.connection as conn:
                conn.execute(update_message_id_cmd, data)
        except sqlite3.DatabaseError:
            print("ERROR: Failed to assign message ID to poll")

    def close_poll(self, poll_id):
        close_poll_cmd = "UPDATE polls SET open = FALSE WHERE poll_id = :poll_id"
        data = {"poll_id": poll_id}

        try:
            with self.connection as conn:
                conn.execute(close_poll_cmd, data)
        except sqlite3.DatabaseError:
            print("ERROR: Failed to close poll")

    def get_option_id(self, poll_id, option_position):
        pass

    def get_poll_options(self, poll_id) -> list[tuple[str, str]]:
        select_options_cmd = "SELECT option_emoji, option_text FROM polloptions WHERE poll_id = :poll_id"
        data = {"poll_id": poll_id}
        result_rows = None
        options = []

        try:
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute(select_options_cmd, data)
                result_rows = cursor.fetchall()
        except sqlite3.DatabaseError:
            print("ERROR: Failed to retrieve poll options")

        for row in result_rows:
            options.append((row["option_emoji"], row["option_text"]))

        return options
