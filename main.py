"""Main module."""
import requests
import threading

# postgres
import psycopg2

import mischbares.server.autolab_server as server
from mischbares.logger import logger
from mischbares.config.main_config import config
from mischbares.driver.autolab_driver import Autolab

log = logger.setup_applevel_logger(file_name="mischbares.log")

# connect to db postgres
def connect_to_postgres(host = "localhost", port = 5432, user = "postgres", password = "PhD2020",
                        database = "mischbares_test"):
    con = psycopg2.connect(
        host = host,
        database = database,
        user = user,
        password = password,
        port = port)
    return con


def call_autolab_driver():
    log.info("Start Autolab-Driver-Modul")
    Autolab(config["autolabDriver"])

def call_autolab_server():
    host_url = config['servers']['autolabDriver']['host']
    port_url = config['servers']['autolabDriver']['port']
    requests.get(f"http://{host_url}:{port_url}").json()

#call_autolab_server()
# def echem_test(action, params):
#     server = 'autolab'
#     action = action
#     params = params
#     res = requests.get("http://{}:{}/{}/{}".format(
#         config['servers']['autolab']['host'],
#         config['servers']['autolab']['port'],server , action),
#         params= params).json()
#     return res

def start_autolab_server():
    """Start the Autolab server."""
    server.main()


def main():
    """Main function."""
    log.info("Start Autolab-Driver-Modul")
    # Start the server in a thread
    server_thread = threading.Thread(target=start_autolab_server)
    server_thread.start()
    # Check if the server is running
    response = None
    while response != 200:
        try:
            response = requests.get("http://{}:{}/docs".format( \
                config['servers']['autolabDriver']['host'], \
                config['servers']['autolabDriver']['port'])).status_code
        except requests.exceptions.ConnectionError:
            pass
    print("Server was started")
    server_thread.stop()
    print("Server was killed")

# main function
if __name__ == "__main__":
    # call autolab server
    #main()
    connection_to_db = connect_to_postgres()

    # cursor
    cursor_to_db = connection_to_db.cursor()

    # execute query
    cursor_to_db.execute("SELECT procedure FROM public.experiment")

    # fetch all data
    rows = cursor_to_db.fetchall()

    # close the cursor
    cursor_to_db.close()

    # close connection
    connection_to_db.close()
    #start_autolab_server()
