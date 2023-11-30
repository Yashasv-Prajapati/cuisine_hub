import mysql.connector
from modules.seller import request_to_sell
from modules.customer import place_order, show_menu
from modules.admin import add_recipe, approve
from modules.authorization import register, login
from modules.connect_db import connection, USER


profit_margin = 0.20  # 20% profit margin
tax = 0.13  # 13% tax


if __name__ == "__main__":

    # Establish a connection to the MySQL server
    try:
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
                    place_order(recipe_id, quantity, profit_margin, tax)
                elif chosen_option == 3:
                    break
                else:
                    print("Invalid option")
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
