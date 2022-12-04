import psycopg2

from bcrypt import hashpw, gensalt

from mischbares.logger import logger

log = logger.get_logger("db_users")

class Users():
    """class for handling user data. This class inherits from the Database class"""
    def __init__(self, connection, cursor):
        """Initialize the User class

        Args:
            connection (psycopg2.connection): The connection to the database
            cursor (psycopg2.cursor): The cursor to execute SQL statements
        """
        self.connection = connection
        self.cursor = cursor

    def get_user(self, username):
        """get a user from the database

        Args:
            username (str): The username of the user
        Returns:
            user (tuple): A tuple containing the user's data
        """
        sql = "SELECT * FROM users WHERE username = %s"
        self.cursor.execute(sql, (username,))
        result = self.cursor.fetchall()
        cols = [desc[0] for desc in self.cursor.description]
        return dict(zip(cols, result[0]))

    def register_user(self, username, first_name, last_name, email, password):
        """register a user in the database

        Args:
            username (str): The username of the user
            password (str): The password of the user
        Returns:
            bool: True if the user was registered, False if not
        """
        hashed_password = hashpw(password.encode('utf-8'), gensalt())
        # check if the user already exists
        username_exists = self.get_user(username)
        if username_exists:
            log.info("User already exists")
            return False
        self.cursor.execute("INSERT INTO users (username, first_name, last_name, email, password) \
                            VALUES (%s, %s, %s, %s, %s)", (username, first_name, last_name, email, hashed_password))
        try:
            self.connection.commit()
            log.info(f"User {username} registered.")
            return True
        except Exception as e:
            log.error(e)
            return False

    def login_user(self, username, password):
        """login a user

        Args:
            username (str): The username of the user
            password (str): The password of the user
        Returns:
            bool: True if the user was logged in, False if not
        """
        sql = "SELECT * FROM users WHERE username = %s"
        result = self.cursor.execute(sql, (username,))
        if result:
            if hashpw(password.encode('utf-8'), result[0][2]) == result[0][2]:
                log.info(f"Password correct. User {username} logged in.")
                return True
            else:
                log.info("Password incorrect.")
                return False
        else:
            log.info(f"User {username} does not exist.")
            return False

    def delete_user(self, username):
        """Delete a user from the database

        Args:
            username (str): The username of the user
        """
        sql = "DELETE FROM users WHERE username = %s"
        self.cursor.execute(sql, (username,))
        self.connection.commit()
        log.info(f"User {username} deleted.")