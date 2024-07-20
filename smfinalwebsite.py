import sqlite3
import hashlib
import sys
import termios
import tty
from bottle import route, run, request, redirect

# Function to initialize the database
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            email TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS account(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            email TEXT,
            role TEXT
        )
    """)
    conn.commit()
    conn.close()

# Function to hash a password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to prompt for a password and mask input with asterisks
def get_password(prompt="Enter password: "):
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

# Function to get a single character from standard input without echo
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return char

# Route for the homepage
@route('/')
def home():
    return """
    <html>
    <head><title>Home</title></head>
    <body>
        <h1>Welcome to the Homepage</h1>
        <p><a href='/signup'>Sign Up</a></p>
        <p><a href='/login'>Log In</a></p>
    </body>
    </html>
    """

# Route for signing up a new user
@route('/signup', method='GET')
def show_signup_form():
    return """
    <html>
    <head><title>Sign Up</title></head>
    <body>
        <h1>Sign Up</h1>
        <form action='/signup' method='POST'>
            <label>Username: <input type='text' name='username'></label><br>
            <label>Password: <input type='password' name='password'></label><br>
            <label>Email: <input type='text' name='email'></label><br>
            <input type='submit' value='Sign Up'>
        </form>
        <p><a href='/'>Back to Home</a></p>
    </body>
    </html>
    """

@route('/signup', method='POST')
def do_signup():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    username = request.forms.get('username')
    password = request.forms.get('password')
    email = request.forms.get('email')

    hashed_password = hash_password(password)

    c.execute("INSERT INTO account(username, password, email, role) VALUES(?,?,?,?)", (username, hashed_password, email, 'user'))
    conn.commit()
    conn.close()
    return f"User '{username}' signed up successfully. <br><a href='/'>Back to Home</a>"

# Route for logging in
@route('/login', method='GET')
def show_login_form():
    return """
    <html>
    <head><title>Log In</title></head>
    <body>
        <h1>Log In</h1>
        <form action='/login' method='POST'>
            <label>Username: <input type='text' name='username'></label><br>
            <label>Password: <input type='password' name='password'></label><br>
            <input type='submit' value='Log In'>
        </form>
        <p><a href='/'>Back to Home</a></p>
    </body>
    </html>
    """

@route('/login', method='POST')
def do_login():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    username = request.forms.get('username')
    password = request.forms.get('password')

    hashed_password = hash_password(password)
    c.execute("SELECT role FROM account WHERE username = ? AND password = ?", (username, hashed_password))
    result = c.fetchone()
    conn.close()

    if result:
        redirect(f"/admin/{username}")  # Redirect to admin dashboard
    else:
        return "Authentication failed."

# Route for admin dashboard and CRUD operations
@route('/admin/<username>')
def admin_dashboard(username):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute("SELECT role FROM account WHERE username = ?", (username,))
    role = c.fetchone()[0]
    conn.close()

    if role != 'admin':
        return "Access denied. Only admins can access this page."

    return """
    <html>
    <head><title>Admin Dashboard</title></head>
    <body>
        <h1>Welcome, {username}!</h1>
        <p>Role: Admin</p>
        <h2>CRUD Operations</h2>
        <ul>
            <li><a href='/insert'>Insert Record</a></li>
            <li><a href='/show'>Show Table</a></li>
            <li><a href='/update'>Update Record</a></li>
            <li><a href='/delete'>Delete Record</a></li>
            <li><a href='/create_column'>Create New Column</a></li>
        </ul>
        <p><a href='/'>Back to Home</a></p>
    </body>
    </html>
    """.format(username=username)

# Route for inserting a new record
@route('/insert', method='GET')
def show_insert_form():
    return """
    <html>
    <head><title>Insert Record</title></head>
    <body>
        <h1>Insert Record</h1>
        <form action='/insert' method='POST'>
            <label>Name: <input type='text' name='name'></label><br>
            <label>Age: <input type='number' name='age'></label><br>
            <label>Email: <input type='text' name='email'></label><br>
            <input type='submit' value='Insert'>
        </form>
        <p><a href='/admin/{username}'>Back to Admin Dashboard</a></p>
    </body>
    </html>
    """.format(username=request.params.username)

@route('/insert', method='POST')
def do_insert():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    name = request.forms.get('name')
    age = request.forms.get('age')
    email = request.forms.get('email')

    c.execute("INSERT INTO users(name, age, email) VALUES(?,?,?)", (name, age, email))
    conn.commit()
    conn.close()
    return "Record inserted successfully. <br><a href='/admin/{username}'>Back to Admin Dashboard</a>".format(username=request.params.username)

# Route for displaying all records
@route('/show')
def show_table():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    rows = c.fetchall()

    table = "<html><head><title>Show Table</title></head><body><h1>Show Table</h1><table border='1'><tr><th>ID</th><th>Name</th><th>Age</th><th>Email</th></tr>"
    for row in rows:
        table += "<tr>"
        for column in row:
            table += f"<td>{column}</td>"
        table += "</tr>"
    table += "</table><p><a href='/admin/{username}'>Back to Admin Dashboard</a></p></body></html>".format(username=request.params.username)
    conn.close()
    return table

# Route for updating a record
@route('/update', method='GET')
def show_update_form():
    return """
    <html>
    <head><title>Update Record</title></head>
    <body>
        <h1>Update Record</h1>
        <form action='/update' method='POST'>
            <label>User ID: <input type='number' name='id'></label><br>
            <label>What do you want to update? (name/age/email): <input type='text' name='choice'></label><br>
            <label>New Value: <input type='text' name='new_value'></label><br>
            <input type='submit' value='Update'>
        </form>
        <p><a href='/admin/{username}'>Back to Admin Dashboard</a></p>
    </body>
    </html>
    """.format(username=request.params.username)

@route('/update', method='POST')
def do_update():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    user_id = request.forms.get('id')
    choice = request.forms.get('choice')
    new_value = request.forms.get('new_value')

    if choice == "name":
        c.execute("UPDATE users SET name=? WHERE id=?", (new_value, user_id))
    elif choice == "age":
        c.execute("UPDATE users SET age=? WHERE id=?", (new_value, user_id))
    elif choice == "email":
        c.execute("UPDATE users SET email=? WHERE id=?", (new_value, user_id))
    else:
        return "Invalid choice."

    conn.commit()
    conn.close()
    return "Record updated successfully. <br><a href='/admin/{username}'>Back to Admin Dashboard</a>".format(username=request.params.username)

# Route for deleting a record
@route('/delete', method='GET')
def show_delete_form():
    return """
    <html>
    <head><title>Delete Record</title></head>
    <body>
        <h1>Delete Record</h1>
        <form action='/delete' method='POST'>
            <label>User ID: <input type='number' name='id'></label><br>
            <input type='submit' value='Delete'>
        </form>
        <p><a href='/admin/{username}'>Back to Admin Dashboard</a></p>
    </body>
    </html>
    """.format(username=request.params.username)

@route('/delete', method='POST')
def do_delete():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    user_id = request.forms.get('id')

    c.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    return "Record deleted successfully. <br><a href='/admin/{username}'>Back to Admin Dashboard</a>".format(username=request.params.username)

# Route for creating a new column (not implemented in this basic example)
@route('/create_column', method='GET')
def show_create_column_form():
    return """
    <html>
    <head><title>Create New Column</title></head>
    <body>
        <h1>Create New Column</h1>
        <form action='/create_column' method='POST'>
            <label>Column Name: <input type='text' name='column_name'></label><br>
            <input type='submit' value='Create'>
        </form>
        <p><a href='/admin/{username}'>Back to Admin Dashboard</a></p>
    </body>
    </html>
    """.format(username=request.params.username)

@route('/create_column', method='POST')
def do_create_column():
    column_name = request.forms.get('column_name')

    # Example code to create a new column in SQLite
    # This would require altering the table schema and handling migrations
    # For simplicity, this part is left as an exercise
    
    return "Feature not implemented in this example. <br><a href='/admin/{username}'>Back to Admin Dashboard</a>".format(username=request.params.username)

# Function to run the web server
def main():
    init_db()
    run(host='localhost', port=8087)

if __name__ == "__main__":
    main()
