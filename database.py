import mysql.connector
import inspect
import sys

USER = {
    'name' : '',
    'role':'', 
    'email':'', 
    'logged_in':False
}

host = "localhost"
user = "root"
password = "admin"
database = "db"

def establish_connection_to_db():
    # print("Current file name:", __file__)
    # frame_info = inspect.stack()[1]
    # print("__file__ in module:", frame_info[1])

    print("sys.argv[0] in module:", sys.argv[0])

    connection = None
    c = None

    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print("Connected to MySQL database")

        # Perform database operations here

        c = connection.cursor(buffered=True)

    except mysql.connector.Error as err:
        raise err
    
    return connection, c
