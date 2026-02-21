import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Window:
window = tk.Tk()
window.title("University Lab - Vulnerable Login")
window.geometry('600x400')
window.configure(bg="#f0f0f0")

title_label = tk.Label(window, text="Insecure Login Page", font=("Arial", 20, "bold"), bg='#f0f0f0')
title_label.pack(pady=(20, 15))


input_frame = tk.Frame(window, bg='#f0f0f0')
input_frame.pack(pady=10)

# Username:
tk.Label(input_frame, text="Username:", font=("Arial", 12), bg='#f0f0f0').grid(row=0, column=0, padx=5, pady=5, sticky='w')
username_entry = tk.Entry(input_frame, width=30, font=("Arial", 12))
username_entry.grid(row=0, column=1, padx=5, pady=5)

# Password:
tk.Label(input_frame, text="Password:", font=("Arial", 12), bg='#f0f0f0').grid(row=1, column=0, padx=5, pady=5, sticky='w')
password_entry = tk.Entry(input_frame, width=30, show='*', font=("Arial", 12))
password_entry.grid(row=1, column=1, padx=5, pady=5)

# Login:
def handle_login():
    """
    This function handles the login attempt.
    It contains a critical SQL injection vulnerability.
    """
    username = username_entry.get()
    password = password_entry.get()

    db = None 
    try:
        # database connection:
        db = mysql.connector.connect(
            host="localhost",
            user="admin",
      
            password="root",
            database="injection"
        )
        cursor = db.cursor()

    
        # VULNERABILITY  CODE:
        query = f"SELECT Username FROM login WHERE Username='{username}' AND Password='{password}'"
        
        # print the query to the terminal:
        print(f"Executing Vulnerable Query: {query}")

        #exute the query
        cursor.execute(query)

        #take the first colomn 
        result = cursor.fetchone()

        #save the changes after the injection attack
        db.commit()
        
        if result:
            # there is a result?
            messagebox.showinfo("Login Status", f"Welcome, {result[0]}! Login Successful.")
        else:
            # there is no result?
            messagebox.showerror("Login Status", "Login Failed: Invalid username or password.")
    #catch   database errors
    except mysql.connector.Error as err:
       
        messagebox.showerror("Database Error", f"An error occurred: {err}")
    finally:
        # close the connection
        if db and db.is_connected():
            cursor.close()
            db.close()
            print("Database connection closed.")


# button for the login
login_button = tk.Button(window, text="Login", command=handle_login, font=("Arial", 14, "bold"), bg='#4CAF50', fg='white', padx=20, pady=10)
login_button.pack(pady=20)


# start the aprogram
window.mainloop()
