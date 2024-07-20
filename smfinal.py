import sqlite3
import hashlib
import sys
import termios
import tty
from email_validator import validate_email, EmailNotValidError

#mailtrap,tkinter

def init_db():
    """Initialize database with a users table and an accounts table."""
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            email TEXT,
            phone_num TEXT,
            phone_num10 TEXT,
            new_column TEXT,
            yy TEXT,
            gender TEXT,
            u TEXT
        )
    """)
    c.execute("CREATE TABLE IF NOT EXISTS account(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, email TEXT, role TEXT)")
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def get_password(prompt="Enter password: "):
    """Prompt for a password and mask input with asterisks."""
    if sys.stdin.isatty():
        print(prompt, end='', flush=True)
        password = []
        while True:
            char = getch()
            if char in ('\r', '\n'):
                print()
                break
            if char == '\x7f':  # Handle backspace
                if password:
                    password.pop()
                    print('\b \b', end='', flush=True)
            else:
                password.append(char)
                print('*', end='', flush=True)
        return ''.join(password)
    else:
        return input(prompt)

def getch():
    """Get a single character from standard input without echo."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return char

def sign_up():
    """Sign up a new user with a role and return the username and password."""
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    username = input("Enter username: ")
    password = get_password()
    hashed_password = hash_password(password)
    
    while True:
        email = input("Enter email: ")
        try:
            v = validate_email(email)
            email = v["email"]
            break
        except EmailNotValidError as e:
            print(str(e))

    role = input("Enter role (admin/staff): ").strip().lower()

    c.execute("INSERT INTO account(username, password, email, role) VALUES(?,?,?,?)", (username, hashed_password, email, role))
    conn.commit()
    conn.close()
    print("User signed up successfully.")
    return username, password

def authenticate(username=None, password=None):
    """Authenticate a user and return their role."""
    if username is None or password is None:
        username = input("Enter username: ")
        password = get_password()

    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    hashed_password = hash_password(password)
    c.execute("SELECT role FROM account WHERE username = ? AND password = ?", (username, hashed_password))
    result = c.fetchone()
    conn.close()

    if result:
        print(f"Authentication successful. Logged in as {result[0]}.")
        return result[0]
    else:
        print("Authentication failed.")
        return None

def insert_db():
    """Insert records into the users table."""
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    while True:
        name = input("Enter name: ")
        age = input("Enter age: ")
        email = input("Enter email: ")

        c.execute("INSERT INTO users(name, age, email) VALUES(?,?,?)", (name, age, email))
        conn.commit()

        cont = input("Do you want to add another record? (yes/no): ").strip().lower()
        if cont != 'yes':
            break

    conn.close()

def show_table():
    """Show all records in the users table."""
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    rows = c.fetchall()
    for row in rows:
        print(row)
    conn.close()

def update_column():
    """Update a specific column in a user record."""
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    user_id = input("Enter the id of the user you want to update: ")
    choice = input("What do you want to update? (age/name/email): ").lower()

    if choice == 'age':
        new_age = input("Enter the new age: ")
        c.execute("UPDATE users SET age = ? WHERE id = ?", (new_age, user_id))
    elif choice == 'name':
        new_name = input("Enter the new name: ")
        c.execute("UPDATE users SET name = ? WHERE id = ?", (new_name, user_id))
    elif choice == 'email':
        new_email = input("Enter the new email: ")
        c.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    else:
        print("Invalid choice.")

    conn.commit()
    conn.close()

def delete_record():
    """Delete a user record based on id."""
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    user_id = input("Enter the id of the user you want to delete: ")
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))

    conn.commit()
    conn.close()

def create_new_column():
    """Create a new column in the users table."""
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    new_column_name = input("Enter the name of the new column: ")
    c.execute(f"ALTER TABLE users ADD COLUMN {new_column_name} VARCHAR(20)")

    conn.commit()
    conn.close()

def main():
    init_db()

    print("============= CHOICES================")
    print("1. SIGN UP")
    print("2. LOG IN")
    print("3. EXIT\n")

    role = None

    while True:
        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                username, password = sign_up()
                role = authenticate(username, password)
                if role:
                    break
            elif choice == 2:
                role = authenticate()
                if role:
                    break
            elif choice == 3:
                print("Exiting...")
                return
            else:
                print("Invalid choice. Please choose from 1 to 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    if role:
        print(f"Logged in as {role}.")
        while True:
            try:
                print("============= CHOICES================")
                print("1. INSERT INTO TABLE")
                print("2. SHOW TABLE")
                print("3. UPDATE RECORD")
                if role == 'admin':
                    print("4. DELETE RECORD")
                    print("5. CREATE NEW COLUMN")
                print("6. EXIT\n")

                choice = int(input("Enter your choice: "))

                if choice == 1:
                    insert_db()
                elif choice == 2:
                    show_table()
                elif choice == 3:
                    update_column()
                elif choice == 4 and role == 'admin':
                    delete_record()
                elif choice == 5 and role == 'admin':
                    create_new_column()
                elif choice == 6:
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice or permission denied. Please choose from the available options.")
            except ValueError:
                print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
