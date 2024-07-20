# from http.server import SimpleHTTPRequestHandler, HTTPServer
# import sqlite3
# import hashlib
# import urllib.parse
# import os

# DATABASE = 'data.db'

# # Hardcoded admin credentials for simxplicity
# ADMIN_USERNAME = 'admin'
# ADMIN_PASSWORD = hashlib.sha256('adminpassword'.encode()).hexdigest()

# def init_db():
#     conn = sqlite3.connect(DATABASE)
#     c = conn.cursor()
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS users(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT UNIQUE,
#             password TEXT,
#             email TEXT
#         )
#     """)
#     conn.commit()
#     conn.close()

# class MyHandler(SimpleHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == '/':
#             self.path = 'templates/index.html'
#         elif self.path == '/login':
#             self.path = 'templates/login.html'
#         elif self.path == '/signup':
#             self.path = 'templates/signup.html'
#         elif self.path == '/admin':
#             self.path = 'templates/admin.html'
#         elif self.path == '/insert':
#             self.path = 'templates/insert.html'
#         elif self.path == '/update':
#             self.path = 'templates/update.html'
#         elif self.path == '/delete':
#             self.path = 'templates/delete.html'
#         elif self.path == '/show':
#             conn = sqlite3.connect(DATABASE)
#             c = conn.cursor()
#             c.execute("SELECT * FROM users")
#             users = c.fetchall()
#             conn.close()

#             users_list = ''.join([f"<li>ID: {user[0]}, Username: {user[1]}, Email: {user[3]}</li>" for user in users])
#             with open('templates/show.html', 'r') as file:
#                 template = file.read()
#             response = template.replace('<!-- The users list will be dynamically inserted here -->', users_list)

#             self.send_response(200)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             self.wfile.write(response.encode())
#             return
#         else:
#             self.send_error(404, "File not found")
#             return

#         return SimpleHTTPRequestHandler.do_GET(self)

#     def do_POST(self):
#         content_length = int(self.headers['Content-Length'])
#         post_data = self.rfile.read(content_length)
#         post_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

#         if self.path == '/signup':
#             username = post_data['username'][0]
#             password = post_data['password'][0]
#             email = post_data['email'][0]
#             hashed_password = hashlib.sha256(password.encode()).hexdigest()

#             conn = sqlite3.connect(DATABASE)
#             c = conn.cursor()
#             try:
#                 c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, hashed_password, email))
#                 conn.commit()
#                 self.send_response(302)
#                 self.send_header('Location', '/login')
#                 self.end_headers()
#             except sqlite3.IntegrityError:
#                 self.send_response(302)
#                 self.send_header('Location', '/signup?error=User already exists')
#                 self.end_headers()
#             finally:
#                 conn.close()

#         elif self.path == '/login':
#             username = post_data['username'][0]
#             password = post_data['password'][0]
#             hashed_password = hashlib.sha256(password.encode()).hexdigest()

#             if username == ADMIN_USERNAME and hashed_password == ADMIN_PASSWORD:
#                 self.send_response(302)
#                 self.send_header('Set-Cookie', 'admin=true')
#                 self.send_header('Location', '/admin')
#                 self.end_headers()
#             else:
#                 conn = sqlite3.connect(DATABASE)
#                 c = conn.cursor()
#                 c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
#                 user = c.fetchone()
#                 conn.close()

#                 if user:
#                     self.send_response(302)
#                     self.send_header('Location', '/')
#                     self.end_headers()
#                 else:
#                     self.send_response(302)
#                     self.send_header('Location', '/login?error=Invalid credentials')
#                     self.end_headers()

#         elif self.path in ['/insert', '/update', '/delete']:
#             # Check if the user is an admin
#             cookies = self.headers.get('Cookie')
#             if cookies and 'admin=true' in cookies:
#                 if self.path == '/insert':
#                     username = post_data['username'][0]
#                     password = post_data['password'][0]
#                     email = post_data['email'][0]
#                     hashed_password = hashlib.sha256(password.encode()).hexdigest()

#                     conn = sqlite3.connect(DATABASE)
#                     c = conn.cursor()
#                     c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, hashed_password, email))
#                     conn.commit()
#                     conn.close()

#                     self.send_response(302)
#                     self.send_header('Location', '/show')
#                     self.end_headers()

#                 elif self.path == '/update':
#                     user_id = post_data['id'][0]
#                     username = post_data['username'][0]
#                     email = post_data['email'][0]

#                     conn = sqlite3.connect(DATABASE)
#                     c = conn.cursor()
#                     c.execute("UPDATE users SET username = ?, email = ? WHERE id = ?", (username, email, user_id))
#                     conn.commit()
#                     conn.close()

#                     self.send_response(302)
#                     self.send_header('Location', '/show')
#                     self.end_headers()

#                 elif self.path == '/delete':
#                     user_id = post_data['id'][0]

#                     conn = sqlite3.connect(DATABASE)
#                     c = conn.cursor()
#                     c.execute("DELETE FROM users WHERE id = ?", (user_id,))
#                     conn.commit()
#                     conn.close()

#                     self.send_response(302)
#                     self.send_header('Location', '/show')
#                     self.end_headers()
#             else:
#                 self.send_response(403)
#                 self.send_header('Content-type', 'text/html')
#                 self.end_headers()
#                 self.wfile.write(b'403 Forbidden: Admin access required')
#         else:
#             self.send_response(404)
#             self.end_headers()

# if __name__ == "__main__":
#     init_db()
#     PORT = 8095
#     server_address = ('', PORT)
#     httpd = HTTPServer(server_address, MyHandler)
#     print(f"Serving on port {PORT}")
#     httpd.serve_forever()


from http.server import SimpleHTTPRequestHandler, HTTPServer
import sqlite3
import hashlib
import urllib.parse
import os

DATABASE = 'data.db'

# Hardcoded admin credentials for simplicity
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = hashlib.sha256('adminpassword'.encode()).hexdigest()

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'templates/index.html'
        elif self.path == '/login':
            self.path = 'templates/login.html'
        elif self.path == '/signup':
            self.path = 'templates/signup.html'
        elif self.path == '/admin':
            self.path = 'templates/admin.html'
        elif self.path == '/insert':
            self.path = 'templates/insert.html'
        elif self.path == '/update':
            self.path = 'templates/update.html'
        elif self.path == '/delete':
            self.path = 'templates/delete.html'
        elif self.path == '/show':
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("SELECT * FROM users")
            users = c.fetchall()
            conn.close()

            users_list = ''.join([f"<li>ID: {user[0]}, Username: {user[1]}, Email: {user[3]}</li>" for user in users])
            with open('templates/show.html', 'r') as file:
                template = file.read()
            response = template.replace('<!-- The users list will be dynamically inserted here -->', users_list)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(response.encode())
            return
        else:
            self.send_error(404, "File not found")
            return

        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

        if self.path == '/signup':
            username = post_data['username'][0]
            password = post_data['password'][0]
            email = post_data['email'][0]
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, hashed_password, email))
                conn.commit()
                self.send_response(302)
                self.send_header('Location', '/login')
                self.end_headers()
            except sqlite3.IntegrityError:
                self.send_response(302)
                self.send_header('Location', '/signup?error=User already exists')
                self.end_headers()
            finally:
                conn.close()

        elif self.path == '/login':
            username = post_data['username'][0]
            password = post_data['password'][0]
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            if username == ADMIN_USERNAME and hashed_password == ADMIN_PASSWORD:
                self.send_response(302)
                self.send_header('Set-Cookie', 'admin=true')
                self.send_header('Location', '/admin')
                self.end_headers()
            else:
                conn = sqlite3.connect(DATABASE)
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
                user = c.fetchone()
                conn.close()

                if user:
                    self.send_response(302)
                    self.send_header('Location', '/')
                    self.end_headers()
                else:
                    self.send_response(302)
                    self.send_header('Location', '/login?error=Invalid credentials')
                    self.end_headers()

        elif self.path in ['/insert', '/update', '/delete']:
            # Check if the user is an admin
            cookies = self.headers.get('Cookie')
            if cookies and 'admin=true' in cookies:
                if self.path == '/insert':
                    username = post_data['username'][0]
                    password = post_data['password'][0]
                    email = post_data['email'][0]
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()

                    conn = sqlite3.connect(DATABASE)
                    c = conn.cursor()
                    try:
                        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, hashed_password, email))
                        conn.commit()
                        self.send_response(302)
                        self.send_header('Location', '/show')
                        self.end_headers()
                    except sqlite3.IntegrityError:
                        self.send_response(302)
                        self.send_header('Location', '/insert?error=User already exists')
                        self.end_headers()
                    finally:
                        conn.close()

                elif self.path == '/update':
                    user_id = post_data['id'][0]
                    username = post_data['username'][0]
                    email = post_data['email'][0]

                    conn = sqlite3.connect(DATABASE)
                    c = conn.cursor()
                    c.execute("UPDATE users SET username = ?, email = ? WHERE id = ?", (username, email, user_id))
                    conn.commit()
                    conn.close()

                    self.send_response(302)
                    self.send_header('Location', '/show')
                    self.end_headers()

                elif self.path == '/delete':
                    user_id = post_data['id'][0]

                    conn = sqlite3.connect(DATABASE)
                    c = conn.cursor()
                    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
                    conn.commit()
                    conn.close()

                    self.send_response(302)
                    self.send_header('Location', '/show')
                    self.end_headers()
            else:
                self.send_response(403)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'403 Forbidden: Admin access required')
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    init_db()
    PORT = 8134
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, MyHandler)
    print(f"Serving on port {PORT}")
    httpd.serve_forever()

