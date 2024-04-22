import random, tkinter as tk, paramiko, socket, time, sqlite3
from tkinter import Button, Entry, Label, ttk, messagebox
from plyer import notification
from library import *
import mysql.connector
from mysql.connector import Error
from PIL import Image, ImageTk

def open_teacher():
    # Define a common font
    common_font = ('Times', 12, "bold")
    common_color = bg='misty rose'
    
    # Function to generate a random CAPTCHA text
    def generate_captcha():
        characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        global captcha
        captcha = "".join(random.choice(characters) for _ in range(6))
        captcha_label.config(text=captcha)
    
    # Function to clear the entry fields
    def clear_entries():
        teacher_name_entry_login.delete(0, tk.END)
        teacher_id_entry.delete(0, tk.END)
        mobile_no_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        captcha_entry.delete(0, tk.END)
        
# Function to handle the registration process with input validation

    '''def toggle_password_visibility():
        current_show_value = password_entry.cget("show")
        new_show_value = "" if current_show_value else "*"
        password_entry.config(show=new_show_value)
    
        # Toggle eye icon
        if current_show_value:
            toggle_button.config(image=eye_open_icon)
        else:
            toggle_button.config(image=eye_closed_icon)'''

    def register_teacher():
        # Replace the placeholder values with your MySQL database credentials
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="teachers"
        )
    
        if connection.is_connected():
            cursor = connection.cursor()
    
            # Check if teacher already exists
            teacher_id = teacher_id_entry.get()
            query = "SELECT * FROM teachers WHERE teacher_id = %s"
            cursor.execute(query, (teacher_id,))
            existing_teacher = cursor.fetchone()
    
            # If teacher exists, show error message
            if existing_teacher:
                messagebox.showerror("Error", "Teacher with ID {} already exists.".format(teacher_id))
                return False
    
            # Otherwise, proceed with registration
            teacher_name = teacher_name_entry_login.get()
            mobile_no = mobile_no_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            entered_captcha = captcha_entry.get()
    
            # Input validation
            if not teacher_name or not teacher_id or not mobile_no or not email or not password:
                messagebox.showerror("Error", "Please fill in all the fields.")
                return False
            elif not teacher_id.isdigit() or len(teacher_id) != 7:
                messagebox.showerror("Error", "Teacher ID must be a 7-digit number.")
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
                # Registration successful
                # Store the data in the database
                query = "INSERT INTO teachers (teacher_name, teacher_id, mobile_no, email, password) VALUES (%s, %s, %s, %s, %s)"
                data = (teacher_name, teacher_id, mobile_no, email, password)
                cursor.execute(query, data)
                connection.commit()
                cursor.close()
    
                # Show success message
                messagebox.showinfo("Registration Successful", "Teacher registered successfully!")
                return True  
              
    # Create the main window
    root = tk.Tk()
    root.configure(bg='light yellow')
    root.title("teacher Registration")
    root.state("zoomed")

    # Create a frame to contain all the elements
    main_frame = tk.Frame(root, borderwidth=2, relief="solid", bg='misty rose')
    main_frame.pack(pady=50)  # Add padding to center the frame vertically
    
    # Function to handle "Enter" key press and focus on the next entry
    def focus_next_entry(event, current_entry, next_entry):
        current_entry.focus_set()
        next_entry.focus_set()

    '''# Add an image to the left side
    image_path = "C:/Users/Tushal/Desktop/conexa/Kirti_logo.png"  # Change this to the path of your image
    image = tk.PhotoImage(file=image_path)
    #resized_image = image.subsample(5,5)
    image_label = tk.Label(main_frame, image=image)
    image_label.grid(row=1, column=0, rowspan=9, padx=10, pady=10)'''
    
    registration_label = tk.Label(main_frame, text="Teacher Registration", font=("Times", 30, "bold"), bg=common_color)
    registration_label.grid(row=0, column=3,padx=10, pady=10)

    teacher_name_label_login = tk.Label(main_frame, text="Teacher Name:",font=common_font, bg=common_color)
    teacher_name_label_login.grid(row=1, column=2, padx=10, pady=10)
    teacher_name_entry_login = tk.Entry(main_frame)
    teacher_name_entry_login.grid(row=1, column=3, padx=10, pady=10)
    
    teacher_id_label = tk.Label(main_frame, text="Teacher ID (Roll N):",font=common_font, bg=common_color)
    teacher_id_label.grid(row=2, column=2, padx=10, pady=10)
    teacher_id_entry = tk.Entry(main_frame)
    teacher_id_entry.grid(row=2, column=3, padx=10, pady=10)
    
    mobile_no_label = tk.Label(main_frame, text="Mobile No:",font=common_font, bg=common_color)
    mobile_no_label.grid(row=3, column=2, padx=10, pady=10)
    mobile_no_entry = tk.Entry(main_frame)
    mobile_no_entry.grid(row=3, column=3, padx=10, pady=10)
    
    email_label = tk.Label(main_frame, text="Email:",font=common_font, bg=common_color)
    email_label.grid(row=4, column=2, padx=10, pady=10)
    email_entry = tk.Entry(main_frame)
    email_entry.grid(row=4, column=3, padx=10, pady=10)
    
    password_label = tk.Label(main_frame, text="Password:",font=common_font, bg=common_color)
    password_label.grid(row=5, column=2, padx=10, pady=10)
    password_entry = tk.Entry(main_frame, show="*")  # Mask the password
    password_entry.grid(row=5, column=3, padx=10, pady=10)

    '''    # Load eye icon images
    eye_open_icon_image = Image.open("C:/Users/Tushal/Desktop/conexa/eye.png")  # Replace with the path to your open eye icon image
    eye_closed_icon_image = Image.open("C:/Users/Tushal/Desktop/conexa/hidden.png")  # Replace with the path to your closed eye icon image

    eye_open_icon_image = eye_open_icon_image.resize((20, 20))
    eye_closed_icon_image = eye_closed_icon_image.resize((20, 20))
    
    eye_open_icon = ImageTk.PhotoImage(eye_open_icon_image)
    eye_closed_icon = ImageTk.PhotoImage(eye_closed_icon_image)
    
    # Toggle Button with eye icons
    toggle_button = tk.Button(main_frame, command=toggle_password_visibility, image=eye_closed_icon, compound="right", bg=common_color)
    toggle_button.grid(row=5, column=4, padx=10, pady=10)'''

    # Generate and display CAPTCHA text
    captcha_label = Label(main_frame, text="", font=("Times", 17, "bold"), bg='mintcream', fg='red')
    captcha_label.grid(row=8, column=2, padx=10, pady=10)
    generate_captcha_button = Button(main_frame, text="Generate CAPTCHA", command=generate_captcha,font=common_font, bg='orange')
    generate_captcha_button.grid(row=8, column=3, padx=10, pady=10)
    
    # Label and Entry for user input
    captcha_label_entry = Label(main_frame, text="CAPTCHA:",font=common_font,bg=common_color)
    captcha_label_entry.grid(row=7, column=2, padx=10, pady=10)
    captcha_entry = Entry(main_frame, font=("Times", "16", "bold"), width=10, fg='gray1')
    captcha_entry.grid(row=7, column=3, padx=10, pady=5)
    
    # Bind the "Enter" key for teacher_name_entry_login
    teacher_name_entry_login.bind("<Return>", lambda event, entry=teacher_id_entry: focus_next_entry(event, teacher_name_entry_login, entry))
    
    # Bind the "Enter" key for teacher_id_entry_login
    teacher_id_entry.bind("<Return>", lambda event, entry=mobile_no_entry: focus_next_entry(event, teacher_id_entry, entry))
    
    # Bind the "Enter" key for mobile_no_entry
    mobile_no_entry.bind("<Return>", lambda event, entry=email_entry: focus_next_entry(event, mobile_no_entry, entry))
    
    # Bind the "Enter" key for email_entry
    email_entry.bind("<Return>", lambda event, entry=password_entry: focus_next_entry(event, email_entry, entry))
    
    # Bind the "Enter" key for password_entry
    password_entry.bind("<Return>", lambda event, entry=captcha_entry: focus_next_entry(event, password_entry, entry))
    
    # Bind the "Enter" key for captcha_entry
    captcha_entry.bind("<Return>", )  # Assuming you want to submit the form on pressing Enter in the captcha_entry
    
    def vadidate_open_login():
        # Call course_validation to check if all fields are filled
        registeration_successful = register_teacher()
    
        # If validation is successful, open the teacher interface
        if registeration_successful:
            open_login_window()
    
    # Create buttons
    register_button = tk.Button(main_frame, text="Register", bg='green', fg='black',font=common_font, command=lambda: [vadidate_open_login(), root.destroy()])
    register_button.grid(row=9, column=3, padx=10, pady=10, columnspan=2, sticky="ew")
    # Bind the "Enter" key for password_entry
    
    clear_button = tk.Button(main_frame, text=" Clear", bg='red', fg='black',font=common_font, command=clear_entries)
    clear_button.grid(row=11, column=3, padx=10, pady=10, columnspan=2, sticky="ew")
    
    def open_login():
        # Call course_validation to check if all fields are filled
        login_successful = open_login_window()
    
    # If validation is successful, open the teacher interface
        if login_successful:
            root.destroy()
            open_login_window()
    
    login_button = tk.Button(main_frame, text="Login", bg='blue', fg='black',font=common_font, command=open_login)
    login_button.grid(row=10, column=3, padx=10, pady=10, columnspan=2,sticky="ew")
    
    # Center the frame in the window
    main_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    # Function to open the login window
    def open_login_window():
    
        # Create the login window
        login_root = tk.Tk()
        login_root.title("teacher Login")
        login_root.state("zoomed")
        login_root.configure(bg='light yellow')
    
        def join_class():

                # Replace the placeholder values with your MySQL database credentials
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="12345678",
                database="teachers"
            )
            if connection.is_connected():
                cursor = connection.cursor()

                teacher_name_entry = teacher_name_entry_login.get()  # Use nonlocal
                teacher_id = teacher_id_entry_login.get()
                password = password_entry_login.get()
                entered_captcha = captcha_entry.get()
    
                # Input validation
                if not teacher_name_entry or not teacher_id or not password:
                    messagebox.showerror("Error", "Please fill in all the fields.")
                    return False
                elif not teacher_id.isdigit() or len(teacher_id) != 7:
                    messagebox.showerror("Error", "teacher ID must be a 7-digit number.")
                    return False
                elif entered_captcha != captcha.get():
                    messagebox.showerror("Error", "Incorrect CAPTCHA. Please try again.")
                    generate_captcha()
                    return False
                else:
                    # Check if teacher exists in the database
                    query = "SELECT * FROM teachers WHERE teacher_id = %s AND password = %s"
                    cursor.execute(query, (teacher_id, password))
                    existing_teacher = cursor.fetchone()
    
                    if existing_teacher:
                        messagebox.showinfo("Login Successful", "Teacher login successful!")
                        return True
                    else:
                        messagebox.showerror("Error", "Invalid credentials. Please sign up.")
                        return False
        
        # Create a frame to contain all the elements
        login_frame = tk.Frame(login_root, borderwidth=2, relief="solid", bg=common_color)
        login_frame.pack(pady=50)  # Add padding to center the frame vertically
    
        # Configure the columns and rows to expand and fill any extra space
        login_root.columnconfigure(0, weight=1)
        login_root.rowconfigure(0, weight=1)
    
        # Add your login window components to the frame
        # Create labels and entry widgets
        teacher_login = tk.Label(login_frame, text="Teacher Login", font=("Times", 30, 'bold'), bg=common_color)
        teacher_login.grid(row=0, column=1, padx=10, pady=10)
    
        teacher_name_label_login = tk.Label(login_frame, text="Teacher Name:", font=common_font, bg=common_color)
        teacher_name_label_login.grid(row=1, column=0, padx=10, pady=10)
        teacher_name_entry_login = ttk.Entry(login_frame, font=common_font)
        teacher_name_entry_login.grid(row=1, column=1, padx=10, pady=10)
    
        teacher_id_label_login = tk.Label(login_frame, text="Teacher ID:", font=common_font, bg=common_color)
        teacher_id_label_login.grid(row=2, column=0, padx=10, pady=10)
        teacher_id_entry_login = ttk.Entry(login_frame)
        teacher_id_entry_login.grid(row=2, column=1, padx=10, pady=10)
    
        password_label_login = tk.Label(login_frame, text="Password:", font=common_font, bg=common_color)
        password_label_login.grid(row=3, column=0, padx=10, pady=10)
        password_entry_login = ttk.Entry(login_frame, show="*")  # Mask the password
        password_entry_login.grid(row=3, column=1, padx=10, pady=10)
    
        # Generate and display CAPTCHA text
        captcha_label = Label(login_frame, text="", font=("Times", 17), bg='mintcream', fg='red')
        captcha_label.grid(row=5, column=0, padx=1, pady=1)
    
        # Label and Entry for user input
        captcha_label_entry = Label(login_frame, text="CAPTCHA:", bg=common_color, font= common_font)
        captcha_label_entry.grid(row=4, column=0, padx=10, pady=10)
        captcha_entry = Entry(login_frame, font=("Times", "16"), width=10, fg='gray1')
        captcha_entry.grid(row=4, column=1, padx=10, pady=5)

        # Bind the "Enter" key for teacher_name_entry_login
        teacher_name_entry_login.bind("<Return>", lambda event, entry=teacher_id_entry: focus_next_entry(event, teacher_name_entry_login, entry))
        
        # Bind the "Enter" key for teacher_id_entry_login
        teacher_id_entry.bind("<Return>", lambda event, entry=password_entry: focus_next_entry(event, teacher_id_entry, entry))
        
        # Bind the "Enter" key for password_entry
        password_entry.bind("<Return>", lambda event, entry=captcha_entry: focus_next_entry(event, password_entry, entry))
        
        # Bind the "Enter" key for captcha_entry
        captcha_entry.bind("<Return>", )  # Assuming you want to submit the form on pressing Enter in the captcha_entry
        
        # Center the frame in the window
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
                
        # Function to generate a random CAPTCHA text
        def generate_captcha():
            characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
            global captcha
            captcha = "".join(random.choice(characters) for _ in range(6))
            captcha_label.config(text=captcha)
    
        # Generate captcha button
        generate_captcha_button = Button(login_frame, text="Generate CAPTCHA", command=generate_captcha, bg='orange', fg='black', font=common_font)
        generate_captcha_button.grid(row=5, column=1, padx=10, pady=10)
    
        # Create a back button that brings back to registration
        back_button_login = tk.Button(login_frame, text="Back", bg='red',fg='black',font=common_font, command=login_root.destroy)
        back_button_login.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky='w')
        
        """def command1():
            join_class()
        def command2():
            open()
        def command3():
            command1()
            command2()"""

    
        # Rest of your registration window components
        join_class_button = tk.Button(login_frame, text="Course Registration", bg='green',fg='black',font=common_font, command = open)
        join_class_button.grid(row=6, column=1, padx=10, pady=10 )
    
    if __name__ == "__main__":
     open_login_window()
    
    # Start the Tkinter main loop
    root.mainloop()