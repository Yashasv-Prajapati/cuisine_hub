# Program for managing stock in medical store
import os
import sys
import time
import hashlib
from datetime import date
import bcrypt
import mysql.connector
# from .modules.authentication import *
# from .modules.middleware import *

profit_margin = 0.20  # 20% profit margin
tax = 0.13  # 13% tax

USER = {
    'name' : '',
    'role':'', 
    'email':'', 
    'logged_in':False
}


def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def check_password(password, hashed_password):
    # Check if the provided password matches the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def register(name, email, password, role, address, phone):
    password = hash_password(password)
    print( password.decode('utf-8') )

    try:
        c.callproc('register', (name, email, password, phone, address, role))    
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    c.execute("SELECT * FROM user WHERE user.email = %s", (email,))
    connection.commit()

    user = c.fetchone()

    if user:
        return user
    else:
        return None

def login(email, password, role):
    
    hashed_password = ''
    user_name = ''
    
    try:
        c.execute("select password, name from user where user.email = %s AND user.role=%s", (email,role))
        connection.commit()

        item = c.fetchone()

        if item != None:
            hashed_password = item[0]
            user_name = item[1]
        else:
            print("No user found")
            return
        if(hashed_password == None): 
            print("No user found")
            return 
        
        valid = check_password(password, hashed_password)

        if valid:
            print('Login Successful')
            USER['name'] = user_name
            USER['role'] = role
            USER['email'] = email
            USER['logged_in'] = True
            return
        else:
            print('Login Failed')
            return
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return


def check_role(role_required):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if USER["role"] == role_required or USER["role"] == 'admin':
                return func(*args, **kwargs)
            else:
                print(f"Unauthorized. Only {role_required}s and admin are allowed to use this function.")
                # You can raise an exception or return a specific response if needed.
                return None  # For illustration purposes

        return wrapper
    return decorator



@check_role('seller')
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

@check_role('customer')
def place_order(recipe_id, quantity):
    user_name = USER['name']
    user_email = USER['email']
    user_role = USER['role']

    # get amount to pay
    c.execute("select price from recipe where recipe.id = %s", (recipe_id,))
    price = c.fetchone()[0]
    amount_to_pay = price * quantity

    print("This is the total amount you have to pay: ", amount_to_pay)
    print("Do you want to continue? (y/n)")
    choice = input()
    if(choice == 'n'):
        return

    params = (user_name, user_email, user_role, recipe_id, quantity, amount_to_pay)

    try:
        
        c.callproc('place_order', params)    
        connection.commit()

        print("Order placed successfully")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return

@check_role('customer')
def show_menu():

    try:
        # get all recipes
        # c.callproc('get_recipes')
        c.execute('SELECT id, name, selling_price FROM recipe;')

        recipes = c.fetchall()

        # print('recipes')
        # print(recipes)
        print("id - name - price")
        for recipe in recipes:
            print(f"{recipe[0]} - {recipe[1]} - {recipe[2]}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        
    return

def add_recipe():
    print("Enter recipe name: ")
    recipe_name = input()
    print("Enter recipe price: ")
    recipe_price = input()

    try:
        c.callproc('add_recipe', (recipe_name, recipe_price))    
        connection.commit()

        print("Recipe added successfully")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return

# Replace these values with your MySQL server details
host = "localhost"
user = "root"
password = "admin"
database = "db"

# Establish a connection to the MySQL server
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

        
    # a = register('Yamu Prajapati', 'yamu@gmail.com', '1234', 'customer', 'Kathmandu', '9841234567')

    # a = login('yamu@gmail.com', '1234', 'customer')


    while True:
        if not USER['logged_in'] :
            print("Register or Login(r/l): ")
            choice = input()
        
            if choice == 'r':
                print("Enter name: ")
                name = input()
                print("Enter email in the form (abc@xyz.prq): ")
                email = input()
                print("Enter password(must be longer than 4 characters): ")
                password = input()
                print("Enter role(customer/seller): ")
                role = input()
                print("Enter address: ")
                address = input()
                print("Enter phone(must be longer than 10 characters): ")
                phone = input()
                register(name, email, password, role, address, phone)
            
            elif choice == 'l':
                print("Enter email: ")
                email = input()
                print("Enter password: ")
                password = input()
                print("Enter role(customer/seller): ")
                role = input()
                login(email, password, role)
            
            else:
                print("Invalid choice")
                continue
        
        if USER['logged_in'] and USER['role'] == 'seller':
            options = ['1. Request to sell', '2. Exit']
            for option in options:
                print(option)

            chosen_option = int(input())
            if chosen_option == 1 : 
                print("Name of raw material: ")
                name = input()
                print("Price of raw material: ")
                price = input()
                print("Expiry time of raw material(YYYY-MM-DD HH:MM:SS): ")
                exp_time = input()
                print("Quantity left: ")
                quantity_left = input()
                request_to_sell(name, price, exp_time, quantity_left)
            else:
                break

        if USER['logged_in'] and USER['role'] == 'customer':
            options = ['1. Show Menu', '2. Place Order', '3. Exit']
            for option in options:
                print(option)
    
            chosen_option = int(input())
            if chosen_option == 1:
                show_menu()
            elif chosen_option == 2:
                recipes = show_menu()

                print("Select recipe number: ")
                index = int(input())
                
                if(index < 0 or index >= len(recipes)): # invalid index
                    print("Invalid recipe number")
                    continue
                recipe_id = recipes[index]

                print("Enter quantity: ")
                quantity = input()
                place_order(recipe_id, quantity)
            else:
                break

            print("Done, do you want to do something else? (y/n)")
            if(input() == 'n'):
                break

    # if USER['logged_in']:
    #     request_to_sell('Tomato', 100, '2023-11-02 08:00:00', 100)
    # else:
    #     print("User not logged in")

    # print(a)


# authorize('customer')

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Close the database connection in the finally block
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connection closed")