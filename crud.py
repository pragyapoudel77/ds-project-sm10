import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader

# Function to initialize SQLite database and create table
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 age INTEGER,
                 email TEXT,
                 phone_num TEXT,
                 phone_num10 TEXT,
                 new_column TEXT,
                 yy TEXT,
                 gender TEXT)''')
    conn.commit()
    conn.close()

# Function to insert data into the database
def insert_data(name, age, email, phone_num, phone_num10, new_column, yy, gender):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO users(name, age, email, phone_num, phone_num10, new_column, yy, gender) VALUES(?,?,?,?,?,?,?,?)",
              (name, age, email, phone_num, phone_num10, new_column, yy, gender))
    conn.commit()
    conn.close()

# Function to fetch all data from the database
def fetch_all_data():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    rows = c.fetchall()
    conn.close()
    return rows

# Function to update data in the database
def update_data(id, name, age, email, phone_num, phone_num10, new_column, yy, gender):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    query = "UPDATE users SET name=?, age=?, email=?, phone_num=?, phone_num10=?, new_column=?, yy=?, gender=? WHERE id=?"
    c.execute(query, (name, age, email, phone_num, phone_num10, new_column, yy, gender, id))
    conn.commit()
    conn.close()

# Function to delete data from the database
def delete_data(id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()
    conn.close()

# Function to create a new column in the database
def create_column(column_name, column_type):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("ALTER TABLE users ADD COLUMN {} {}".format(column_name, column_type))
    conn.commit()
    conn.close()

# Function to render HTML template for showing data
def render_index():
    # Fetch data from the database
    rows = fetch_all_data()
    
    # Render HTML template using Jinja2
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('index.html')
    html_output = template.render(rows=rows)
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
            self.wfile.write(b'<li><a href="/create">Create Table</a></li>')
            self.wfile.write(b'<li><a href="/insert">Insert Data</a></li>')
            self.wfile.write(b'<li><a href="/show">Show Table</a></li>')
            self.wfile.write(b'<li><a href="/update">Update Data</a></li>')
            self.wfile.write(b'<li><a href="/delete">Delete Data</a></li>')
            self.wfile.write(b'<li><a href="/create_column">Create New Column</a></li>')
            self.wfile.write(b'</ul></body></html>')

        elif path == '/create':
            init_db()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Table created successfully. <a href="/">Back to Menu</a>')

        elif path == '/insert':
            # Extract query parameters (name, age, email, phone_num, phone_num10, new_column, yy, gender)
            params = parse_qs(parsed_path.query)
            name = params.get('name', [''])[0]
            age = int(params.get('age', ['0'])[0])
            email = params.get('email', [''])[0]
            phone_num = params.get('phone_num', [''])[0]
            phone_num10 = params.get('phone_num10', [''])[0]
            new_column = params.get('new_column', [''])[0]
            yy = params.get('yy', [''])[0]
            gender = params.get('gender', [''])[0]
            
            insert_data(name, age, email, phone_num, phone_num10, new_column, yy, gender)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Data inserted successfully. <a href="/">Back to Menu</a>')

        elif path == '/show':
            html_output = render_index()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_output.encode())

        elif path.startswith('/update'):
            # Extract query parameters (id, name, age, email, phone_num, phone_num10, new_column, yy, gender)
            params = parse_qs(parsed_path.query)
            id = int(params.get('id', ['0'])[0])
            name = params.get('name', [''])[0]
            age = int(params.get('age', ['0'])[0])
            email = params.get('email', [''])[0]
            phone_num = params.get('phone_num', [''])[0]
            phone_num10 = params.get('phone_num10', [''])[0]
            new_column = params.get('new_column', [''])[0]
            yy = params.get('yy', [''])[0]
            gender = params.get('gender', [''])[0]
            
            update_data(id, name, age, email, phone_num, phone_num10, new_column, yy, gender)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Data updated successfully. <a href="/">Back to Menu</a>')

        elif path.startswith('/delete'):
            # Extract query parameter (id)
            params = parse_qs(parsed_path.query)
            id = int(params.get('id', ['0'])[0])
            
            delete_data(id)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Data deleted successfully. <a href="/">Back to Menu</a>')

        elif path.startswith('/create_column'):
            # Extract query parameters (column_name, column_type)
            params = parse_qs(parsed_path.query)
            column_name = params.get('column_name', [''])[0]
            column_type = params.get('column_type', [''])[0]
            
            create_column(column_name, column_type)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Column created successfully. <a href="/">Back to Menu</a>')

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Page not found')

# Main function to run the server
def run():
    server_address = ('', 8001)  # Change port if needed
    httpd = HTTPServer(server_address, RequestHandler)
    print('Starting HTTP server on port 8001...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
