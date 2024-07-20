import os
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader

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

# Function to insert user data into the database
def insert_user(name, age, email, password):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO users(name, age, email, password, role) VALUES(?,?,?,?,?)",
              (name, age, email, password, 'user'))  # Assign 'user' role to regular users
    conn.commit()
    conn.close()

# Function to insert admin data into the database
def insert_admin(name, email, password):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO admins(name, email, password, role) VALUES(?,?,?,?)",
              (name, email, password, 'admin'))
    conn.commit()
    conn.close()

# Function to authenticate user based on username and password
def authenticate_user(email, password):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=? AND role='user'",
              (email, password))
    user = c.fetchone()
    conn.close()
    return user

# Function to authenticate admin based on email and password
def authenticate_admin(email, password):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM admins WHERE email=? AND password=? AND role='admin'",
              (email, password))
    admin = c.fetchone()
    conn.close()
    return admin

# Function to render HTML template
def render_template(template_name, **context):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_name)
    html_output = template.render(context)
    return html_output

# HTTP request handler class
class RequestHandler(BaseHTTPRequestHandler):

    # GET method to handle requests
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h2>Database Operations</h2><ul>')
            self.wfile.write(b'<li><a href="/signup">User Sign Up</a></li>')
            self.wfile.write(b'<li><a href="/admin_signup">Admin Sign Up</a></li>')
            self.wfile.write(b'<li><a href="/signin">User Sign In</a></li>')
            self.wfile.write(b'<li><a href="/admin_signin">Admin Sign In</a></li>')
            self.wfile.write(b'</ul></body></html>')

        elif path == '/signup':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(render_template('signup.html').encode())

        elif path == '/admin_signup':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(render_template('admin_signup.html').encode())

        elif path == '/signin':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(render_template('signin.html').encode())

        elif path == '/admin_signin':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(render_template('admin_signin.html').encode())

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Page not found')

    # POST method to handle form submissions
    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        if path == '/signup':
            params = parse_qs(post_data)
            name = params.get('name', [''])[0]
            age = params.get('age', [''])[0]
            email = params.get('email', [''])[0]
            password = params.get('password', [''])[0]

            insert_user(name, age, email, password)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'User signed up successfully. <a href="/">Back to Menu</a>')

        elif path == '/admin_signup':
            params = parse_qs(post_data)
            name = params.get('name', [''])[0]
            email = params.get('email', [''])[0]
            password = params.get('password', [''])[0]

            insert_admin(name, email, password)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Admin signed up successfully. <a href="/">Back to Menu</a>')

        elif path == '/signin':
            params = parse_qs(post_data)
            email = params.get('email', [''])[0]
            password = params.get('password', [''])[0]

            user = authenticate_user(email, password)
            if user:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Set-Cookie', f'role={user[5]}; Path=/')
                self.end_headers()
                self.wfile.write(b'User signed in successfully. <a href="/">Back to Menu</a>')
            else:
                self.send_response(401)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Authentication failed. <a href="/signin">Try again</a>')

        elif path == '/admin_signin':
            params = parse_qs(post_data)
            email = params.get('email', [''])[0]
            password = params.get('password', [''])[0]

            admin = authenticate_admin(email, password)
            if admin:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Set-Cookie', f'role=admin; Path=/')
                self.end_headers()
                self.wfile.write(b'Admin signed in successfully. <a href="/">Back to Menu</a>')
            else:
                self.send_response(401)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Authentication failed. <a href="/admin_signin">Try again</a>')

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Page not found. <a href="/">Back to Menu</a>')

# Main function to run the server
def run():
    init_db()
    port = 8004
    print(f'Starting server on port {port}...')
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Server running...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
