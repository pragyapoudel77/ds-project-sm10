import sqlite3
from getpass import getpass

# Initialize SQLite database and create tables for users and admins
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Create users table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 age INTEGER,
                 email TEXT,
                 password TEXT,
                 role TEXT)''')

    # Create admins table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS admins (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 email TEXT,
                 password TEXT,
                 role TEXT)''')

    conn.commit()
    conn.close()
    print('Database initialized with users and admins tables.')

# Function to insert user data into the database
def insert_user(name, age, email, password):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO users(name, age, email, password, role) VALUES(?,?,?,?,?)",
              (name, age, email, password, 'user'))  # Assign 'user' role to regular users
    conn.commit()
    conn.close()
    print(f'Inserted user: {name}, {age}, {email}')

# Function to insert admin data into the database
def insert_admin(name, email, password):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO admins(name, email, password, role) VALUES(?,?,?,?)",
              (name, email, password, 'admin'))
    conn.commit()
    conn.close()
    print(f'Inserted admin: {name}, {email}')

# Function to authenticate user based on username and password
def authenticate_user(email, password):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=? AND role='user'",
              (email, password))
    user = c.fetchone()
    conn.close()
    if user:
        print(f'Authenticated user: {email}')
    else:
        print('Authentication failed for user.')
    return user

# Function to authenticate admin based on email and password
def authenticate_admin(email, password):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM admins WHERE email=? AND password=? AND role='admin'",
              (email, password))
    admin = c.fetchone()
    conn.close()
    if admin:
        print(f'Authenticated admin: {email}')
    else:
        print('Authentication failed for admin.')
    return admin

def signup_user():
    print("User Sign Up")
    name = input("Name: ")
    age = input("Age: ")
    email = input("Email: ")
    password = getpass("Password: ")

    insert_user(name, age, email, password)
    print("User signed up successfully.")

def signup_admin():
    print("Admin Sign Up")
    name = input("Name: ")
    email = input("Email: ")
    password = getpass("Password: ")

    insert_admin(name, email, password)
    print("Admin signed up successfully.")

def signin_user():
    print("User Sign In")
    email = input("Email: ")
    password = getpass("Password: ")

    user = authenticate_user(email, password)
    if user:
        print("User signed in successfully.")
    else:
        print("Sign in failed.")

def signin_admin():
    print("Admin Sign In")
    email = input("Email: ")
    password = getpass("Password: ")

    admin = authenticate_admin(email, password)
    if admin:
        print("Admin signed in successfully.")
    else:
        print("Sign in failed.")

def main():
    init_db()

    while True:
        print("\nDatabase Operations")
        print("1. User Sign Up")
        print("2. Admin Sign Up")
        print("3. User Sign In")
        print("4. Admin Sign In")
        print("5. Exit")
        
        choice = input("Choose an option: ")

        if choice == '1':
            signup_user()
        elif choice == '2':
            signup_admin()
        elif choice == '3':
            signin_user()
        elif choice == '4':
            signin_admin()
        elif choice == '5':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    main()
