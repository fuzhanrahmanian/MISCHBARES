"""Class for database objects and connections."""
import configparser
import psycopg2

import pandas as pd

from mischbares.logger import logger

log = logger.get_logger("db_database")

class Database:
    """ Class for database objects and connections. """
    def __init__(self):
        config  = configparser.ConfigParser()
        config.read("mischbares/db/config.ini")
        self.host = config["database"]["host"]
        self.port = config["database"]["port"]
        self.user = config["database"]["user"]
        self.password = config["database"]["password"]
        self.database = config["database"]["database"]
        self.connection = None
        self.cursor = None
        self.connect()


    def __del__(self):
        """Close the connection to the database"""
        self.close()


    def connect(self):
        """Connect to the database
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

        except psycopg2.Error as e:
            log.error(f"Error while connecting to database: {e}")


    def close(self):
        """Close the connection to the database"""
        self.connection.close()


    def execute(self, sql, params=None):
        """Execute a SQL statement"""
        df = pd.read_sql_query(sql, self.connection, params=params)
        if df.empty:
            return None
        return df
        # self.cursor.execute(sql, params)
        # result = self.cursor.fetchall()
        # #TODO Make a pandas dataframe from the result
        # if result:
        #     cols = [desc[0] for desc in self.cursor.description]
        #     for i in range(len(result)):
        #         result[i] = dict(zip(cols, result[i]))
        #     return result
        #     #return dict(zip(cols, result[0]))
        # return None


    def commit(self, sql, params=None):
        """Commit a SQL statement
        Args:
            sql (str): The SQL statement to execute
            params (tuple): The parameters for the SQL statement
        Returns:
            Bool: True if the commit was successful, False otherwise
        """
        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
            log.info("Changes committed to database")
            return True

        except psycopg2.Error as e:
            log.error(f"Error while executing SQL statement: {e}")
            return False
