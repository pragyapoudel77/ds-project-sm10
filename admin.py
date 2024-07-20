import os
import sqlite3

print("============= CHOICES================")
print("1.CREATE TABLE \n")
print("2.INSERT IN TABLE \n")
print("3.SHOW TABLE \n")
print("4.UPDATE TABLE'S COLUMN \n")
print("5.DELETE TABLE'S COLUMN \n")
print("6.CREATE NEW COLUMN \n")
print("7.EXIT \n\n")

while True:

    x=int(input("Enter your choice:"))

    if(x==1):
            def init_db():
                conn = sqlite3.connect('data.db')
                c=conn.cursor()
                c.execute("CREATE TABLE IF NOT EXISTS admins(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, password password,is_admin INTEGER DEFAULT 0)")
                conn.commit()
                conn.close()

            init_db()
    if(x==2):

            conn = sqlite3.connect('data.db')
            c = conn.cursor()

            # Insert an admin user
            c.execute("INSERT INTO admins (name, password, is_admin) VALUES (?, ?, ?)",('admin', 'password', 1))

            conn.commit()
            conn.close()

    if(x==3):
            def is_admin(name, password):
                conn = sqlite3.connect('data.db')
                c = conn.cursor()

                c.execute("SELECT is_admin FROM admins WHERE name = ? AND password = ?", (name, password))
                result = c.fetchone()
                
                conn.close()
                
                if result and result[0] == 1:
                    return True
                return False
            
    
    