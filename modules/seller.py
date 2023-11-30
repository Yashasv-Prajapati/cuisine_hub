import mysql.connector
from modules.authorization import check_role
from modules.connect_db import c, connection, USER

# @check_role('seller')
def request_to_sell(rm_name, rm_price, rm_exp_time, rm_quantity_left):
    user_name = USER['name']
    user_email = USER['email']
    user_role = USER['role']

    params = (user_name, user_email, user_role, rm_name, rm_price, rm_exp_time, rm_quantity_left)

    try:
        
        c.callproc('request_to_sell', params)    
        connection.commit()

        print("Request to sell successful")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return
