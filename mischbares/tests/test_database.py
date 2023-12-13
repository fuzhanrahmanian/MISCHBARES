""" testfile to test the database module """

import os
import configparser
import pytest

from mischbares.db.database import Database
from mischbares.db.user import Users

config = configparser.ConfigParser()
config.read(os.path.join("mischbares", "db", "config.ini"))

db  = Database()

def test_connect():
    """Test the connection to the database."""

    # Connect to the database
    db.connect()

    # assert that the connection is not None and of type psycopg2.connection
    assert db.connection is not None and type(db.connection).__name__ == "connection"
    assert db.cursor is not None and type(db.cursor).__name__ == "cursor"

    # Close the connection to the database
    db.close()


def test_execute():
    """Test the execution of SQL statements."""

    # Connect to the database
    db.connect()

    # Execute a SQL statement
    sql = "SELECT * FROM users"
    result = db.execute(sql)

    # assert that the result is not None and a pandas dataframe
    assert result is not None and type(result).__name__ == "DataFrame"

    # Close the connection to the database
    db.close()


def test_get_user():
    """Test the get_user method."""

    users = Users()
    user = users.get_user("frahmanian")

    # Check that the user is not None and of type tuple and has username "frahmanian"
    assert user is not None and type(user).__name__ == "DataFrame" and user["username"].values[0] == "frahmanian"
    # close the connection to the database
    db.close()


@pytest.mark.dependency()
def test_register_user():
    """Test the register_user method."""

    users = Users()
    assert users.register_user("test_username", "test_fisrt_name", "test_last_name", "test_email",
                        "test_password") is True

    # Check that the user is not None and of type tuple and has username "test_username"
    test_user = users.get_user("test_username")
    assert test_user is not None and type(test_user).__name__ == "DataFrame" and test_user["username"].values[0] == "test_username"

    users.close()

@pytest.mark.dependency(depends=["test_register_user"])
def test_login_user():
    """Test the login_user method."""

    users = Users()
    assert users.login_user("test_username", "test_password") is True
    assert users.login_user("test_username", "wrong_password") is False

    users.close()

@pytest.mark.dependency(depends=["test_register_user"])
def test_delete_user():
    """Test the delete_user method."""

    users = Users()
    assert users.delete_user("test_username") is True

    # Check that the user is None
    test_user = users.get_user("test_username")
    assert test_user is None

    users.close()
