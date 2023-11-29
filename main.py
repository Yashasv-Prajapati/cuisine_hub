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
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        print("Password does not match")
        return False

def register(name, email, password, role, address, phone):
    password = hash_password(password)

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
                return None

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
    
    print(recipe_id, quantity)
    # get logged in customer details
    user_name = USER['name']
    user_email = USER['email']
    user_role = USER['role']

    try:
        c.execute('select raw_material_id from ingredient as i where i.recipe_id = %s', [recipe_id])
        ingredients = c.fetchall()

        for ingredient in ingredients:
            ingredient_id = ingredient[0]
            c.callproc('update_raw_materials', [ingredient_id, recipe_id, 0])
            connection.commit()

        
        # calculate amount to pay by customer
        c.execute("call get_recipe_price(%s, @recipe_price)", [recipe_id])
        c.execute("select @recipe_price")
        result = c.fetchone()

        if not result:
            print("Something went wrong, couldn't get price")
            return
        
        price = result[0]
        if price == None:
            print("Something went wrong, couldn't get price")
            return
        
        amount_to_pay = price * (1+profit_margin) * (1+tax)
        print("This is the total amount you have to pay: ", amount_to_pay)
        print("Do you want to continue? (y/n)")


        choice = input()
        if(choice == 'n'):
            return

        # USER HAS TO CONFIRM THE ORDER
        # check if the items are available or not
        c.execute('select raw_material_id from ingredient as i where i.recipe_id = %s', [recipe_id])
        ingredients = c.fetchall()

        for ingredient in ingredients:
            print(ingredient[0])
            ingredient_id = ingredient[0]
            c.callproc('check_raw_material', [ingredient_id, quantity])

        for ingredient in ingredients:
            ingredient_id = ingredient[0]
            c.callproc('update_raw_materials', [ingredient_id, recipe_id, quantity])
            connection.commit()

        # add the order to the buys table
        c.callproc('place_order', [user_name, user_email, user_role, recipe_id, quantity,price, amount_to_pay])
        connection.commit()

        
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    return

@check_role('customer')
def show_menu():
    recipes = []

    try:
        # get all recipes
        c.execute('SELECT id, name, description FROM recipe;')

        recipes = c.fetchall()

        print("id - name - description")
        for recipe in recipes:
            print(f"{recipe[0]} - {recipe[1]} - {recipe[2]}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        
    return recipes


@check_role("admin")
def approve():
    print("Here is the Pending materials\n")
    recipes = []

    try:
        # get all recipes
        c.execute('SELECT user_id, raw_material_id, status FROM sells WHERE status="pending";')

        recipes = c.fetchall()

        print("user_id - raw_material_id - status")
        for recipe in recipes:
            print(f"{recipe[0]} - {recipe[1]} - {recipe[2]}")
        print("Select the user_id you want to approve")
        userID = int(input())
        print("Select the raw_material_id you want to approve")
        RawID =int(input())
        c.callproc('approve_recipe',(userID,RawID))
        connection.commit()


    except mysql.connector.Error as err:
        print(f"Error: {err}")
        
    return 

@check_role("admin")
def add_recipe():
    print("Enter recipe name: ")
    recipe_name = input()
    print("Enter recipe description: ")
    recipe_descr = input()

    # Take input for the number of raw materials
    num_raw_materials = int(input("Enter the number of raw materials: "))

    raw_materials = []  # List to store raw materials and their quantities

    # Take input for each raw material and quantity
    for i in range(num_raw_materials):
        print(f"Enter name of raw material {i+1}: ")
        raw_material_name = input()
        print(f"Enter quantity required for {raw_material_name}: ")
        raw_material_quantity = float(input())
        raw_materials.append((raw_material_name, raw_material_quantity))


    try:
        # Call the add_recipe stored procedure with recipe_name, recipe_price, and raw_materials
        c.callproc('add_recipe', (recipe_name, recipe_descr))

        # Retrieve the recipe_id generated by the stored procedure
        c.execute("SELECT LAST_INSERT_ID();")
        recipe_id = c.fetchone()[0]

        # Add raw materials to the recipe
        print(raw_materials)
        for raw_material in raw_materials:
            print(raw_material[0], raw_material[1])
            c.callproc('add_raw_materials_to_recipe', (recipe_id, raw_material[0], raw_material[1]))
            connection.commit()

        print("Recipe added successfully")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    return



# Replace these values with your MySQL server details
host = "localhost"
user = "root"
password = "Gopal@123"
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

    # place_order(1, 2)
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
                recipe_id = recipes[index][0]

                print("Enter quantity: ")
                quantity = int(input())
                place_order(recipe_id, quantity)
            elif chosen_option == 3:
                add_recipe()
            else:
                break
        if USER['logged_in'] and USER['role'] == 'admin':
            options = ['1. Add recipe', '2. Approve','3.Exit']
            for option in options:
                print(option)

            chosen_option = int(input())
            if chosen_option == 1:
                add_recipe()
            if chosen_option==2:
                approve()
            else:
                break

        print("Done, do you want to do something else? (y/n)")
        if(input() == 'n'):
            break


except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Close the database connection in the finally block
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connection closed")
    else:
        print("Connection not closed")
