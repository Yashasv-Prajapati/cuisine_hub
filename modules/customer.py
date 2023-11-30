from modules.authorization import check_role
from modules.connect_db import c, connection, USER
import mysql.connector

@check_role('customer')
def place_order(recipe_id, quantity, profit_margin, tax):
    
    print(recipe_id, quantity)
    # get logged in customer details
    user_name = USER['name']
    user_email = USER['email']
    user_role = USER['role']

    try:

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
