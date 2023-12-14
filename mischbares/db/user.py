""" Class for handling the User table in the database. """
from bcrypt import hashpw, gensalt, checkpw

from mischbares.db.database import Database
from mischbares.logger import logger

log = logger.get_logger("db_users")

class Users(Database):
    """class for handling user data."""
    def __init__(self):
        """Initialize the User class
        """
        super().__init__()
        self.user_id = None


    def get_user(self, username):
        """get a user from the database

        Args:
            username (str): The username of the user
        Returns:
            user (tuple): A tuple containing the user's data
        """
        sql = "SELECT * FROM users WHERE username = %s"
        return self.execute(sql, (username,))


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
        if username_exists is not None:
            log.info("User already exists")
            return False

        commit_status = self.commit("INSERT INTO users (user_id, first_name, last_name, email, password, username)\
            VALUES (nextval('user_user_id_seq'::regclass), %s, %s, %s, %s, %s)", \
            (first_name, last_name, email, hashed_password.decode('utf-8'), username))
        if commit_status:
            log.info(f"User {username} registered.")
        return commit_status


    def login_user(self, username, password):
        """login a user

        Args:
            username (str): The username of the user
            password (str): The password of the user
        Returns:
            bool: True if the user was logged in, False if not
        """
        sql = "SELECT * FROM users WHERE username = %s"
        result = self.execute(sql, (username,))
        if not result.empty:
            if checkpw(password.encode('utf-8'), result['password'].values[0].encode('utf-8')):
                log.info(f"Password correct. User {username} logged in.")
                self.user_id = int(result['user_id'].values[0])
                return True
            log.info("Password incorrect.")
            return False
        log.info(f"User {username} does not exist.")
        return False


    def delete_user(self, username):
        """Delete a user from the database

        Args:
            username (str): The username of the user
        Returns:
            bool: True if the user was deleted, False if not
        """
        sql = "DELETE FROM users WHERE username = %s"
        commit_status = self.commit(sql, (username,))
        if commit_status:
            log.info(f"User {username} deleted.")
        return commit_status
