import random, tkinter as tk, paramiko, socket, time, sqlite3, os
from tkinter import * 
from plyer import notification
from threading import Thread
import mysql.connector 
from mysql.connector import Error
from PIL import Image, ImageTk
from student_interface import *

# Define a common font
common_font = ('Times', 14, "bold")
common_color = bg='misty rose'

#------------------------------------------ Student Database Connection -------------------------------------------------

# Function to generate a random CAPTCHA text
def generate_captcha():
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    global captcha
    captcha = "".join(random.choice(characters) for _ in range(6))
    captcha_label.config(text=captcha)

# Function to clear the entry fields
def clear_entries():
    student_name_entry.delete(0, tk.END)
    student_id_entry.delete(0, tk.END)
    mobile_no_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    captcha_entry.delete(0, tk.END)

# Function to save student details to the MySQL database
def save_to_database(student_name, student_id, mobile_no, email, password):
    try:
        if is_student_duplicate(student_id):
            messagebox.showerror("Duplicate Entry", "Student with the same ID already exists. Please log in.")
            return False

        # Replace the placeholder values with your MySQL database credentials
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="students"
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Replace 'students' with the actual table name where you want to store the data
            query = "INSERT INTO students (student_name, student_id, mobile_no, email, password) VALUES (%s, %s, %s, %s, %s)"
            data = (student_name, student_id, mobile_no, email, password)

            cursor.execute(query, data)

            connection.commit()
            cursor.close()

    except Error as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            connection.close()

def toggle_password_visibility():
    current_show_value = password_entry.cget("show")
    new_show_value = "" if current_show_value else "*"
    password_entry.config(show=new_show_value)

    # Toggle eye icon
    if current_show_value:
        toggle_button.config(image=eye_open_icon)
    else:
        toggle_button.config(image=eye_closed_icon)

# Function to handle the registration process with input validation
def register_student():
    student_name = student_name_entry.get()
    student_id = student_id_entry.get()
    mobile_no = mobile_no_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    entered_captcha = captcha_entry.get()

    # Input validation
    if  not student_id or not mobile_no or not email or not password:
        messagebox.showerror("Error", "Please fill in all the fields.")
        return False
    elif not student_id.isdigit() or len(student_id) != 7:
        messagebox.showerror("Error", "Student ID must be a 7-digit number.")
        return False
    elif not mobile_no.isdigit() or len(mobile_no) != 10:
        messagebox.showerror("Error", "Mobile number must be a 10-digit number.")
        return False
    elif "@" not in email or "." not in email or email.count("@") != 1:
        messagebox.showerror("Error", "Invalid email address.")
        return False
    elif entered_captcha != captcha:
        messagebox.showerror("Error", "Incorrect CAPTCHA. Please try again.")
        generate_captcha()
        return False
    else:
        successs = save_to_database(student_name, student_id, mobile_no, email, password)
        # Registration successful
        if successs:
           messagebox.showinfo("Registration Successful", "Student registered successfully!")
        return True

# Function to check if the student already exists in the database
def is_student_duplicate(student_id):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="students"
        )

        if connection.is_connected():
            cursor = connection.cursor()

            query = "SELECT * FROM students WHERE student_id = %s"
            data = (student_id,)

            cursor.execute(query, data)
            result = cursor.fetchall()

            return bool(result)  # Returns True if there are duplicate entries, else False

    except Error as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            connection.close()
    return False

# Create the main window
root = Tk()
root.configure(bg='light yellow')
root.title("Student Registration")
root.state("zoomed")

registration_label = tk.Label(root, text="Student Registration", font=("Times", 30, "bold"), bg='light yellow')
registration_label.pack(padx=10, pady=10)

# Create a frame to contain all the elements
main_frame = tk.Frame(root, borderwidth=2, relief="solid", bg='misty rose')
main_frame.pack(pady=50)  # Add padding to center the frame vertically

def focus_next_entry(event, current_entry, next_entry):
    current_entry.focus_set()
    next_entry.focus_set()

# Add an image to the left side
"""image_path = "C:/Users/Jeevan/OneDrive/Desktop/Student_logo.png"  # Change this to the path of your image
image = tk.PhotoImage(file=image_path)
resized_image = image.subsample(100,100)
image_label = tk.Label(main_frame, image=image, bg=common_color)
image_label.grid(row=3, column=1, rowspan=9, padx=10, pady=10)"""

student_name_label = tk.Label(main_frame, text="Student Name:",font=common_font, bg=common_color)
student_name_label.grid(row=2, column=2, padx=10, pady=10)
student_name_entry = tk.Entry(main_frame)
student_name_entry.grid(row=2, column=3, padx=10, pady=10)

student_id_label = tk.Label(main_frame, text="Roll No:",font=common_font, bg=common_color)
student_id_label.grid(row=3, column=2, padx=10, pady=10)
student_id_entry = tk.Entry(main_frame)
student_id_entry.grid(row=3, column=3, padx=10, pady=10)

mobile_no_label = tk.Label(main_frame, text="Mobile No:",font=common_font, bg=common_color)
mobile_no_label.grid(row=4, column=2, padx=10, pady=10)
mobile_no_entry = tk.Entry(main_frame)
mobile_no_entry.grid(row=4, column=3, padx=10, pady=10)

email_label = tk.Label(main_frame, text="Email:",font=common_font, bg=common_color)
email_label.grid(row=5, column=2, padx=10, pady=10)
email_entry = tk.Entry(main_frame)
email_entry.grid(row=5, column=3, padx=10, pady=10)

password_label = tk.Label(main_frame, text="Password:",font=common_font, bg=common_color)
password_label.grid(row=6, column=2, padx=10, pady=10)
password_entry = tk.Entry(main_frame, show="*")  # Mask the password
password_entry.grid(row=6, column=3, padx=10, pady=10)

# Load eye icon images
eye_open_icon_image = Image.open("C:/Users/Aditya Barai/OneDrive/Desktop/RLMS2/hidden.png")  # Replace with the path to your open eye icon image
eye_closed_icon_image = Image.open("C:/Users/Aditya Barai/OneDrive/Desktop/RLMS2/hidden.png")  # Replace with the path to your closed eye icon image

eye_open_icon_image = eye_open_icon_image.resize((20, 20))
eye_closed_icon_image = eye_closed_icon_image.resize((20, 20))

eye_open_icon = ImageTk.PhotoImage(eye_open_icon_image)
eye_closed_icon = ImageTk.PhotoImage(eye_closed_icon_image)

# Toggle Button with eye icons
toggle_button = tk.Button(main_frame, command=toggle_password_visibility, image=eye_closed_icon, compound="right", bg=common_color)
toggle_button.grid(row=6, column=4, padx=10, pady=10)

# Generate and display CAPTCHA text
captcha_label = Label(main_frame, text="", font=("Times", 17, "bold"), bg=common_color, fg='red')
captcha_label.grid(row=9, column=2, padx=10, pady=10)
generate_captcha_button = Button(main_frame, text="Generate CAPTCHA", command=generate_captcha,font=common_font, bg='SteelBlue1')
generate_captcha_button.grid(row=9, column=3, padx=10, pady=10)

# Label and Entry for user input
captcha_label_entry = Label(main_frame, text="CAPTCHA:",font=common_font, bg=common_color)
captcha_label_entry.grid(row=8, column=2, padx=10, pady=10)
captcha_entry = Entry(main_frame, font=("Times", "16", "bold"), width=10, fg='gray1')
captcha_entry.grid(row=8, column=3, padx=10, pady=5)

# Bind the "Enter" key for student_name_entry
student_name_entry.bind("<Return>", lambda event, entry=student_id_entry: focus_next_entry(event, student_name_entry, entry))

# Bind the "Enter" key for student_id_entry_login
student_id_entry.bind("<Return>", lambda event, entry=mobile_no_entry: focus_next_entry(event, student_id_entry, entry))

# Bind the "Enter" key for mobile_no_entry
mobile_no_entry.bind("<Return>", lambda event, entry=email_entry: focus_next_entry(event, mobile_no_entry, entry))

# Bind the "Enter" key for email_entry
email_entry.bind("<Return>", lambda event, entry=password_entry: focus_next_entry(event, email_entry, entry))

# Bind the "Enter" key for password_entry
password_entry.bind("<Return>", lambda event, entry=captcha_entry: focus_next_entry(event, password_entry, entry))

# Bind the "Enter" key for captcha_entry
captcha_entry.bind("<Return>", )  # Assuming you want to submit the form on pressing Enter in the captcha_entry

def validate_open_login():
    # Call course_validation to check if all fields are filled
    registeration_successful = register_student()

    # If validation is successful, open the student interface
    if registeration_successful:
        open_login_window()

# Create buttons
register_button = tk.Button(main_frame, text="Register", bg='green', fg='black',font=common_font, command=validate_open_login)
register_button.grid(row=10, column=3, padx=10, pady=10, columnspan=2, sticky="ew")
# Bind the "Enter" key for password_entry

clear_button = tk.Button(main_frame, text=" Clear", bg='red', fg='black',font=common_font, command=clear_entries)
clear_button.grid(row=12, column=3, padx=10, pady=10, columnspan=2, sticky="ew")

def command1():
    open_login_window()
def command2():
    root.destroy()
def command3():
    command1()
    command2()

login_button = tk.Button(main_frame, text="Login", bg='gold', fg='black',font=common_font, command = command3)
login_button.grid(row=11, column=3, padx=10, pady=10, columnspan=2,sticky="ew")

# Center the frame in the window
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# Function to open the login window
def open_login_window():
    # Create the login window
    login_root = tk.Tk()
    login_root.title("Student Login")
    login_root.state("zoomed")
    login_root.configure(bg='light yellow')

    # Create a frame to contain all the elements
    login_frame = tk.Frame(login_root, borderwidth=2, relief="solid", bg=common_color)
    login_frame.pack(pady=50)  # Add padding to center the frame vertically

    def join_class(student_name, student_id):

        if check_feilds_filled():
            student_name = student_name_entry_login.get()  # Use nonlocal
            student_id = student_id_entry_login.get()
            password = password_entry_login.get()
            entered_captcha = captcha_entry.get()
            
            # Input validation
            if not student_name or not student_id or not password:
                messagebox.showerror("Error", "Please fill in all the fields.")
                return False
            elif not student_id.isdigit() or len(student_id) != 7:
                messagebox.showerror("Error", "Student ID must be a 7-digit number.")
                return False
            elif entered_captcha != captcha.get():
                messagebox.showerror("Error", "Incorrect CAPTCHA. Please try again.")
                generate_captcha()
                return False
            else:
                # Registration successful
                messagebox.showinfo("Join Class", "Successfully joined the class!")
                return True
            # Function to check login credentials
    def check_login(student_name, student_id, password):
        try:
            # Replace the placeholder values with your MySQL database credentials
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="12345678",
                database="students"
            )

            if connection.is_connected():
                cursor = connection.cursor()
    
                query = "SELECT * FROM students WHERE student_name = %s AND student_id = %s AND password = %s"
                data = (student_name, student_id, password)
    
                cursor.execute(query, data)
                result = cursor.fetchone()
                
                if result:
                    messagebox.showinfo("Login Successful", "Login successful!")
                else:
                    messagebox.showerror("Login Failed", "Invalid login credentials. Please register first ! ")
    
                cursor.close()
        except Error as e:
            print("Error:", e)
        finally:
            if connection.is_connected():
                connection.close()

    # Create labels and entry widgets
    student_login = tk.Label(login_frame, text="Student Login", font=("Times", 30, "bold"),bg=common_color)
    student_login.grid(row=0, column=1, padx=10, pady=10)

    student_name_label_login = tk.Label(login_frame, text="Student Name:", font=common_font, bg=common_color)
    student_name_label_login.grid(row=1, column=0, padx=10, pady=10)
    student_name_entry_login = tk.Entry(login_frame)
    student_name_entry_login.grid(row=1, column=1, padx=10, pady=10)

    student_id_label_login = tk.Label(login_frame, text="Student ID (7 digits):", font=common_font, bg=common_color)
    student_id_label_login.grid(row=2, column=0, padx=10, pady=10)
    student_id_entry_login = tk.Entry(login_frame)
    student_id_entry_login.grid(row=2, column=1, padx=10, pady=10)

    password_label_login = tk.Label(login_frame, text="Password:", font=common_font, bg=common_color)
    password_label_login.grid(row=3, column=0, padx=10, pady=10)
    password_entry_login = tk.Entry(login_frame, show="*")  # Mask the password
    password_entry_login.grid(row=3, column=1, padx=10, pady=10)

    # Generate and display CAPTCHA text
    captcha_label = Label(login_frame, text="", font=("Times", 17), fg='red', bg=common_color)
    captcha_label.grid(row=5, column=1, padx=10, pady=10)

    # Label and Entry for user input
    captcha_label_entry = Label(login_frame, text="CAPTCHA:", font=common_font, bg=common_color)
    captcha_label_entry.grid(row=4, column=0, padx=10, pady=10)
    captcha_entry = Entry(login_frame, font=("Times", "16"), width=10, fg='gray1')
    captcha_entry.grid(row=4, column=1, padx=10, pady=5)

    # Bind the "Enter" key for student_name_entry_login
    student_name_entry_login.bind("<Return>", lambda event, entry=student_id_entry_login: focus_next_entry(event, student_name_entry_login, entry))
    
    # Bind the "Enter" key for student_id_entry_login
    student_id_entry_login.bind("<Return>", lambda event, entry=password_entry_login: focus_next_entry(event, student_id_entry_login, entry))
    
    # Bind the "Enter" key for password_entry
    password_entry_login.bind("<Return>", lambda event, entry=captcha_entry: focus_next_entry(event, password_entry_login, entry))
        
    # Function to generate a random CAPTCHA text
    def generate_captcha():
        characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        global captcha
        captcha = "".join(random.choice(characters) for _ in range(6))
        captcha_label.config(text=captcha)

    # Generate captcha button
    generate_captcha_button = Button(login_frame, text="Generate CAPTCHA", command=generate_captcha,font=common_font, bg='SteelBlue1')
    generate_captcha_button.grid(row=6, column=1,columnspan=2, padx=10, pady=10)

    # Create a back button that brings back to registration
    back_button_login = tk.Button(login_frame, text="Back", bg='red',fg='black',font=common_font, command=login_root.destroy)
    back_button_login.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky='w')
  
    # Rest of your registration window components
    join_class_button = tk.Button(login_frame, text="Join Class", bg='green2', fg='black', font=common_font, command=lambda: (open(student_name_entry_login.get(), student_id_entry_login.get()),(check_login(student_name_entry_login.get(), student_id_entry_login.get(), password_entry_login.get(), command_r3))))
    join_class_button.grid(row=6, column=2,columnspan=2, padx=10, pady=10)
    
    # Center the frame in the window
    login_frame.place(relx=0.5, rely=0.5, anchor="center")

    login_root.mainloop()

# Start the Tkinter main loop                                     
root.mainloop()
