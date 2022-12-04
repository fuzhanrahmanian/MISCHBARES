import psycopg2

from mischbares.logger import logger

log = logger.get_logger("db_database")

class Database:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        """Connect to the database

        Returns:
            connection (psycopg2.connection): The connection to the database
            cursor (psycopg2.cursor): The cursor to execute SQL statements
        """
        self.connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        try:
            self.cursor = self.connection.cursor()
            log.info("Connected to database")
            return self.connection, self.cursor
        except psycopg2.Error as e:
            log.error(f"Error while connecting to database: {e}")
            return None

    def close(self):
        """Close the connection to the database"""
        self.connection.close()

    def execute(self, sql, params=None):
        """Execute a SQL statement"""
        self.cursor.execute(sql, params)
        result = self.cursor.fetchall()
        return result