import os
import sqlite3
import csv


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
                c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER, email TEXT)")
                conn.commit()
                conn.close()

            init_db()

    elif(x==2):
          
        def insert_db():

                while True:
                    records = []
                    while True:
                        #for-loop and then record gets updated, name set in tuple
                        name33 = input("Enter your name")
                        age10= (input("Enter your age"))
                        email10 = (input("Enter your email"))

                        x = (name33,age10,email10)
                        records.append(x)

                        for record in records:
                                print(record)

                        # Ask if the user wants to add another record
                        cont = input("Do you want to add another record? (yes/no): ").strip().lower()
                        if cont!= 'yes':
                                break

                        print("Final records:")

                        for record in records:
                          print(record)
                        # if name33.isdigit():
                        #         print("Invalid")
                        #         break
                        # else:
                        #   print(f"{name33}")
                        # conn = sqlite3.connect('data.db')
                        # c=conn.cursor()
                        # c.execute("INSERT INTO users(name,age,email) VALUES(?,?,?)",(name33,age10,email10,))
                        # # c.execute("INSERT INTO users(age) VALUES(?)",(age10,))

                        # conn.commit()
                        # conn.close()
                        # break

        insert_db()
            
                 


    elif(x==3):
            # Query updated data
        conn = sqlite3.connect('data.db')
        c=conn.cursor()    
        c.execute("SELECT * FROM users")
        rows = c.fetchall()
        print("After update:")
        for row in rows:
            print(row)
                       
            
    elif(x==4):
            conn = sqlite3.connect('data.db')
            c = conn.cursor()

            id10 = input("Enter the id you want to update:")
            
            choice=(int(input("What do you want to update?:age -->1 , name -->2 or mail -->3")))

            if (choice==1):
                 age = int(input("Enter your age you want to update: "))
                 query = "UPDATE users SET age = ? WHERE id = ?"
                 c.execute(query, (age, id10))
                 conn.commit()
                 conn.close()

            elif (choice==2):
                 name100 = (input("Enter your name you want to update: "))
                 query = "UPDATE users SET name = ? WHERE id = ?"
                 c.execute(query, (name100, id10))
                
                 conn.commit()
                 conn.close()

            elif (choice==3):
                 id100 = (input("Enter your email you want to update: "))
                 query = "UPDATE users SET email = ? WHERE id = ?"
                 c.execute(query, (id100, id10))
                
                 conn.commit()
                 conn.close()


    elif(x == 5):
            def delete_data():
                conn = sqlite3.connect('data.db')
                c=conn.cursor()
                id110 = int(input("Enter the id you want to delete:"))
                query ="DELETE FROM users WHERE id = ?"
                c.execute(query, (id110,))      
                conn.commit()
                conn.close()
            delete_data()

    elif(x == 6):
        def create_column():
                conn = sqlite3.connect('data.db')
                c=conn.cursor()
                new_column=(input("Enter new title name"))
                query = f"ALTER TABLE users ADD {new_column} VARCHAR(20)"
                c.execute(query )
                conn.commit()
                conn.close()
        create_column()

    elif(x==7):
        

            print("Exit")
            print("Invalid Number and go to each number")
            x=int(input("Enter your choice:"))
            print(f"{x}")
            os.system("clear")
            
            
            
    else:
            print("Invalid Number and go to each number")
            os.system("clear")











    
        
    




