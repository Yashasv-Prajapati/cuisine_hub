import bcrypt
from modules.connect_db import *

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

def check_role(role_required):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if USER["role"] == role_required or USER["role"] == 'admin':
                return func(*args, **kwargs)
            else:
                print(f"Unauthorized. Only {role_required}s and admin are allowed to use this function.")
                return 

        return wrapper
    return decorator


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
