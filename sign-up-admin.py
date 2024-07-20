import os
import sqlite3

def init_db():
    """Initialize database with a users table and an accounts table."""
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER, email TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS accounts(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, role TEXT, email TEXT)")
    conn.commit()
    conn.close()

def sign_up():
    """Sign up a new user with a role and return the username and password."""
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    username = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role (admin/staff): ").strip().lower()
    email = input("Enter email: ")

    c.execute("INSERT INTO accounts(username, password, role, email) VALUES(?,?,?,?)", (username, password, role, email))
    conn.commit()
    conn.close()
    print("User signed up successfully.")
    return username, password

def authenticate(username=None, password=None):
    """Authenticate a user and return their role."""
    if username is None or password is None:
        username = input("Enter username: ")
        password = input("Enter password: ")

    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute("SELECT role FROM accounts WHERE username = ? AND password = ?", (username, password))
    result = c.fetchone()
    conn.close()

    if result:
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

def delete_column():
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
                print("1. CREATE TABLE")
                print("2. INSERT IN TABLE")
                print("3. SHOW TABLE")
                print("4. UPDATE TABLE'S COLUMN")
                if role == 'admin':
                    print("5. DELETE TABLE'S COLUMN")
                    print("6. CREATE NEW COLUMN")
                print("7. EXIT\n")

                choice = int(input("Enter your choice: "))

                if choice == 1:
                    init_db()
                elif choice == 2:
                    insert_db()
                elif choice == 3:
                    show_table()
                elif choice == 4:
                    update_column()
                elif choice == 5 and role == 'admin':
                    delete_column()
                elif choice == 6 and role == 'admin':
                    create_new_column()
                elif choice == 7:
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice or permission denied. Please choose from the available options.")
            except ValueError:
                print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
