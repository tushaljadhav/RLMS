import tkinter as tk, paramiko, socket, threading, os
from tkinter import ttk, messagebox
from plyer import notification
from tkinter import filedialog
from datetime import datetime
from attendance import *

def open():
     
    # Common_font defined & Common_color
    common_font = ('Times', 14, "bold")
    common_color = bg='misty rose'

    #----------------------------------------------------------------------------------------------
            
    def course_validation():
        department = department_combobox.get()
        year = year_combobox.get()
        semester = semester_combobox.get()
        subjects = subjects_combobox.get()
        batch = batch_combobox.get()
        hours = hours_spinbox.get()
        minutes = minutes_spinbox.get()
        seconds = seconds_spinbox.get()
    
        # Input validation
        if not department or not year or not semester or not subjects or not batch or not hours or not minutes or not seconds:
            messagebox.showerror("Error", "Please fill in all the fields.")
            return False   
        else:
            # Registration successful
            # You can add code here to store the data in a database or file
            messagebox.showinfo(" Course Registration Successful", "Teacher registered successfully!")
            return True
        
    # Create combo boxes for Branch, Semester, Section, and Subject
    year = ["FYIT", "SYIT", "TYIT", "FYCS", "SYCS", "TYCS"]
    semesters = ["1", "2", "3", "4", "5", "6"]
    batches = ["1", "2", "3", "4", "5"]
    subjects = {
        "FYIT": {
            "1": [
                "Imperative Programming",
                "Digital Electronics",
                "Operating Systems",
                "Discrete Mathematics",
                "Communication Skills",
            ],
            "2": [
                "Object Oriented Programming",
                "Microprocessor Architecture",
                "Web Programming",
                "Numerical and Statistical Methods",
                "Green Computing",
            ],
            # Add subjects for other semesters in FYIT
        },
        "SYIT": {
            "3": [
                "Python Programming",
                "Data Structures",
                "Computer Networks",
                "Database Management Systems",
                "Applied Mathematics",
            ],
            "4": [
                "Core Java",
                "Introduction to Embedded Systems",
                "Computer Oriented Statistical Techniques",
                "Software Engineering",
                "Computer Graphics and Animation",
            ],
            # Add subjects for other semesters in SYIT
        },
        "TYIT": {
            "5": [
                "Software Project Management",
                "Internet of Things",
                "Advanced Web Programming",
                "Artificial Intelligence",
                "Linux System Administration",
                "Enterprise Java",
                "Next Generation Technologies",
            ],
            "6": [
                "Software Quality Assurance",
                "Security in Computing",
                "Business Intelligence",
                "Principles of Geographic Information Systems",
                "Enterprise Networking",
                "IT Service Management",
                "Cyber Laws",
            ],
            # Add subjects for other semesters in TYIT
        },
        "FYCS": {
            "1": [
                "Computer Organization and Design",
                "Programming with Python- I",
                "Free and Open Source Software",
                "Database Systems",
                "Discrete Mathematics",
                "Descriptive Statistics and Introduction to Probability",
                "Soft Skills Development",
            ],
            "2": [
                "Programming with C",
                "Programming with Python–II",
                "Linux",
                "Data Structures",
                "Calculus",
                "Statistical Methods and Testing of Hypothesis",
                "Green Technologies",
            ],
            # Add subjects for FYCS
        },
        "SYCS": {
            "3": [
            "Theory of Computation",
            "Core JAVA",
            "Operating System",
            "Database Management Systems",
            "Combinatorics and Graph Theory",
            "Physical Computing and IoT Programming",
            "Web Programming"
            ],
             "4": [
            "Fundamentals of Algorithms",
            "Advanced JAVA",
            "Computer Networks",
            "Software Engineering",
            "Linear Algebra using Python",
            ".NET Technologies",
            "Android Developer Fundamentals"
            ],
            # Add subjects for SYCS
        },
        "TYCS": {
            "5": [
            "Artificial Intelligence",
            "Linux Server Administration",
            "Software Testing and Quality Assurance",
            "Information and Network Security",
            "Architecting of IoT",
            "Web Services",
            "Game Programming"
        ],
           "6": [
            "Wireless Sensor Networks and Mobile Communication",
            "Cloud Computing",
            "Cyber Forensics",
            "Information Retrieval",
            "Digital Image Processing",
            "Data Science",
            "Ethical Hacking"
        ],
            # Add subjects for TYCS
        },
    }
    
    def update_subjects(event):
        selected_year = year_combobox.get()
        selected_semester = semester_combobox.get()
    
        if selected_year in subjects and selected_semester in subjects[selected_year]:
            subjects_combobox['values'] = subjects[selected_year][selected_semester]
            subjects_combobox.set("")  # Clear the selection
        else:
            subjects_combobox['values'] = []

#-------------------------------------------------------------------------------------------------------------------------------------
    
    remaining_time = 0
    warning_message = False
    
    def start_countdown():
        global remaining_time, warning_message
        total_seconds = int(hours_spinbox.get()) * 3600 + int(minutes_spinbox.get()) * 60 + int(seconds_spinbox.get())
        remaining_time = total_seconds
        update_timer()
    
    def update_timer():
        global remaining_time, warning_message
        if remaining_time > 0:
            hours, remainder = divmod(remaining_time, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Update timer label in teacher interface
            selected_timer_label.config(text=f"Class Timer: {hours:02d} hours, {minutes:02d} minutes, {seconds:02d} seconds")
    
            # Check if 5 minutes remaining and show warning message if not shown yet
            if remaining_time == 300 and not warning_shown:
                warning_shown = True
                tk.messagebox.showwarning(title="Time Warning!", message="5 minutes remaining in the class.")
    
            remaining_time -= 1
            interface_root.after(1000, update_timer)
        else:
            selected_timer_label.config(text="Class Timer: 00 hours, 00 minutes, 00 seconds")

    # Define server address and port
    HOST = '192.168.51.162'
    PORT = 65432

    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen()

    # Accept a connection from a client
    client_socket, _ = server_socket.accept()    

    # Function to send shutdown command to student
    def shutdown_student():
        client_socket.sendall(b'shutdown')
        #result_label.config(text="Shutdown command sent to student.")
    
    def open_teacher_interface(department, year, semester, subjects, batch, hours, minutes, seconds):
        teacher_interface = tk.Tk()
        teacher_interface.title("Teacher Interface")
        teacher_interface.geometry("500x500")
        teacher_interface.state("zoomed")  # Open in a maximized (zoomed) state
    
        # Set the border width of the window
        teacher_interface.configure(borderwidth=5, relief="solid")
    
        # Create the above frame
        above_frame = tk.Frame(teacher_interface, borderwidth=2, relief="solid", bg=common_color)
        above_frame.pack(side="top", fill="x", expand=False)  # Adjust the height as needed
    
        # Create left, middle, and right frames within the above frame using grid layout
        left_frame = tk.Frame(above_frame, relief="solid", bg=common_color)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    
        middle_frame = tk.Frame(above_frame, relief="solid", bg=common_color)
        middle_frame.grid(row=0, column=1, sticky="e")
    
        right_frame = tk.Frame(above_frame, relief="solid", bg=common_color)
        right_frame.grid(row=0, column=2, padx=10, pady=10, sticky="en")
    
        # Configure the grid weights to make the frames expand evenly
        above_frame.grid_rowconfigure(0, weight=1)
        above_frame.grid_columnconfigure(0, weight=1)
        above_frame.grid_columnconfigure(1, weight=1)
        above_frame.grid_columnconfigure(2, weight=1)
    
        #------------------------------------------------------ Selected Entries Display --------------------------------------------------------------------------------
    
        # Display the selected options in the teacher interface
        selected_department_label = tk.Label(left_frame, text=f"Department: {department}", font=common_font, bg=common_color)
        selected_department_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    
        teacher_name_label = tk.Label(left_frame, text="Faculty Name: Apurva Yadav", font=common_font, bg=common_color)
        teacher_name_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
    
        teacher_id_label = tk.Label(left_frame, text="Faculty ID: 233893", font=common_font, bg=common_color)
        teacher_id_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
    
        selected_semester_label = tk.Label(left_frame, text=f"Semester: {semester}", font=common_font, bg=common_color)
        selected_semester_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
    
        # Add labels or other elements in the middle frame
        label_remote = tk.Label(middle_frame, text="Remote Lab Monitoring System", font=('Times', 30, 'bold'), bg=common_color)
        label_remote.grid(row=0, column=2, columnspan=2, sticky='news')
    
        selected_year_label = tk.Label(middle_frame, text=f"Class: {year}", font=common_font, bg=common_color)
        selected_year_label.grid(row=1, column=2, padx=5, pady=5, sticky='e')

        selected_batch_label = tk.Label(middle_frame, text=f"Batch: {batch}", font=common_font, bg=common_color)
        selected_batch_label.grid(row=2, column=2, padx=5, pady=5, sticky='e')

        selected_subjects_label = tk.Label(middle_frame, text=f"Subject: {subjects}", font=common_font, bg=common_color)
        selected_subjects_label.grid(row=3, column=2, padx=10, pady=5, sticky='e')
    
        global selected_timer_label
        selected_timer_label = tk.Label(right_frame, text=f"Class Timer: {hours} hours, {minutes} minutes, {seconds} seconds", font=common_font, fg="red", bg=common_color)
        selected_timer_label.grid(row=0, column=3, padx=10, pady=5, sticky='ne')
    
        # Create the left frame
        left_frame = tk.Frame(teacher_interface, borderwidth=2, relief="solid", bg=common_color)
        left_frame.pack(side="left", fill="both", expand=True)
    
        # Create a small dashboard frame within the left frame
        dashboard_frame = tk.Frame(left_frame, borderwidth=2, relief="solid", bg=common_color)
        dashboard_frame.pack(side="top", fill="both", expand=False)
    
        # Add dashboard elements
        dashboard_label = tk.Label(dashboard_frame, text="Dashboard", font=("Times", 16, 'bold'), bg=common_color)
        dashboard_label.pack(pady=10)
    
        # Add a "Save Attendance" button in the left frame
        save_attendance_button = tk.Button(left_frame, text="Save Attendance", font=("Times", 14, 'bold'), bg='lime green', fg='black',command=open_attendance_window)
        save_attendance_button.pack(side="top", fill="x", padx=10, pady=10)
    
        # Create a button to shut down all PCs
        shutdown_button = tk.Button(left_frame, text="Shutdown Computers", font=("Times", 14, 'bold'),bg='red2',fg='black', command=shutdown_student)
        shutdown_button.pack(side="top", fill="x", padx=10, pady=10)
    
        def logout():
        # Display a confirmation dialog with "Yes" and "No" buttons
            result = messagebox.askquestion("Confirmation", "Are you sure you want to log out?")
            if result == "yes":
            # Add the code to perform the logout action here
            # For example, you can destroy the teacher_interface window
                teacher_interface.destroy()
            else:
              # User canceled the action
                messagebox.showinfo("Log Out Canceled", "Log out operation was canceled.")
    
        # Create a button to log out
        logout_button = tk.Button(left_frame, text="Log Out", font=("Times", 14, 'bold'),bg='firebrick1',fg='black', command=logout)
        logout_button.pack(side="top", fill="x", padx=10, pady=10)
    
        # Function to send a file
        def send_file():
            file_path = filedialog.askopenfilename()
            if file_path:
                file_name = os.path.basename(file_path)
                client_socket.send(file_name.encode())
                with open(file_path, "rb") as file:
                    while True:
                        data = file.read(1024)
                        if not data:
                            break
                        client_socket.send(data)
        
                print(f"File sent: {file_name}")
    
        # Create a button to trigger file sharing
        share_button = tk.Button(left_frame, text="Share File", command=send_file, font=common_font, bg='deep sky blue',fg='black')
        share_button.pack(side="top", fill="x", padx=10, pady=10)
    
        # Create a notification frame 
        notification_frame = tk.Frame(left_frame, borderwidth=2, relief="solid", bg=common_color)
        notification_frame.pack(side="top", fill="both", expand=True)
    
        # Add notification elements
        notification_label = tk.Label(notification_frame, text="Notifications", font=("Times", 16, 'bold'), bg=common_color)
        notification_label.pack(pady=10)
    
        # Create a Text widget for displaying notifications
        notification_text = tk.Listbox(notification_frame, selectmode=tk.SINGLE, bg=common_color)
        notification_text.pack(fill=tk.BOTH, expand=True)

        def broadcast_message():
            selected_index = predefined_messages_listbox.curselection()
            if selected_index:
                selected_message = predefined_messages_listbox.get(selected_index)
                client_socket.sendall(selected_message.encode())
        
                # Display sent message in notification box
                notification_text.insert(tk.END, f" {selected_message}\n")
            else:
                messagebox.showerror("Error", "Please Select A Predefined Message.")
    
        # Create a vertical scrollbar for the Text widget
        notification_scrollbar = tk.Scrollbar(notification_frame, orient='vertical', command=notification_text.yview)
        notification_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        notification_text.config(yscrollcommand=notification_scrollbar.set)
    
        # Function to clear all notifications in the Listbox
        def clear_notifications():
            notification_text.delete(0, tk.END)
    
        # Create a button to clear all notifications
        clear_button = tk.Button(notification_frame, text="Clear Notifications", command=clear_notifications, bg='sky blue')
        clear_button.pack(pady=10)

        # Create the center frame
        center_frame = tk.Frame(teacher_interface, borderwidth=2, relief="solid")
        center_frame.pack(side="left", fill="both", expand=True)

        # Create a small "Active Users" frame within the right frame
        active_teachers_frame = tk.Frame(center_frame, borderwidth=2, relief="solid", bg=common_color)
        active_teachers_frame.pack(side="top", fill="both", expand=True)
    
        # Add active user elements
        active_users_label = tk.Label(active_teachers_frame, text="ChatBox", font=("Times", 16, 'bold'), bg=common_color)
        active_users_label.pack(pady=10)
    
        # Create a Listbox for active teachers
        active_teachers_listbox = tk.Listbox(active_teachers_frame, selectmode=tk.MULTIPLE, bg=common_color)
        active_teachers_listbox.pack(fill=tk.BOTH, expand=True)

    
        # Create a scrollbar for the Listbox
        scrollbar = tk.Scrollbar(active_teachers_frame, orient=tk.VERTICAL, command=active_teachers_listbox.yview, bg=common_color)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        active_teachers_listbox.config(yscrollcommand=scrollbar.set)
    
        # Create a frame for the message entry field and send button at the bottom of the center frame
        message_frame = tk.Frame(center_frame, borderwidth=2, relief="solid", bg=common_color)
        message_frame.pack(side="bottom", fill="x", expand=False)
    
        # Add a label for the message entry field
        message_label = tk.Label(message_frame, text="Type a message:", font=common_font, bg=common_color)
        message_label.pack(side="left", fill="x", pady=10)
    
        # Add the message entry field to the message frame
        message_entry = tk.Entry(message_frame)
        message_entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)
    
        # Define function to receive messages
        def receive_messages():
            while True:
                try:
                    # Receive data from the teacher
                    data = client_socket.recv(1024).decode()
                    if not data:
                        break
                    # Display received message on the GUI
                    active_teachers_listbox.insert(tk.END, f"Student: {data}")
                
                except Exception as e:
                    print(f"Error receiving message: {e}")
                    break
        
        # Define function to send messages
        def send_message():
            # Get message from the entry field
            message = message_entry.get()
            # Clear the entry field

            # Display sent message in the chatbox
            active_teachers_listbox.insert(tk.END, f"Teacher: {message}")
            message_entry.delete(0, tk.END)
            # Send message to the teacher
            try:
                client_socket.sendall(message.encode())
            except Exception as e:
                print(f"Error sending message: {e}")

        # Add the "Send" button to the message frame
        send_button = tk.Button(message_frame, text="Send", font=common_font, bg='green3', fg='black', command=send_message)
        send_button.pack(side="left", padx=10, pady=10)

        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.start()

        # Create the right frame
        right_frame = tk.Frame(teacher_interface, borderwidth=2, relief="solid", bg=common_color)
        right_frame.pack(side="left", fill="both", expand=True)

        # List of client hostnames to monitor
        client_hostnames = ["DESKTOP-H5J0MTC"]
        
        # Create a small "Active Users" frame within the right frame
        active_students_frame = tk.Frame(right_frame, borderwidth=2, relief="solid", bg=common_color)
        active_students_frame.pack(side="top", fill="both", expand=True)
    
        # Add active user elements
        active_users_label = tk.Label(active_students_frame, text="Active Students", font=("Times", 16, 'bold'), bg=common_color)
        active_users_label.pack(pady=10)
    
        # Create a Listbox for active teachers
        active_students_listbox = tk.Listbox(active_students_frame, selectmode=tk.MULTIPLE, bg=common_color)
        active_students_listbox.pack(fill=tk.BOTH, expand=True)
        active_students_listbox.insert(tk.END, "LAPTOP-FAGHMIH9")
        
    
        def check_online_status(hostname):
            try:
                # Resolve the hostname to an IP address
                client_ip = socket.gethostbyname(hostname)
        
                # Attempt to create a socket connection to the client
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((client_ip, 80))
                s.close()
        
                # If the connection is successful, the client is online
                return True, f"{hostname} ({client_ip})"
            except (ConnectionRefusedError, socket.timeout, socket.gaierror):
                return False, f"{hostname} (Offline)"
        
        def update_active_students_list():
            # Clear the current list in the Listbox
            active_students_listbox.delete(0, tk.END)
        
            # Insert only the active students (online) into the Listbox
            for client_hostname in client_hostnames:
                is_online, message = check_online_status(client_hostname)
                if is_online:
                    # Insert the student with a green background for active status
                    active_students_listbox.insert(tk.END, message)
                    active_students_listbox.itemconfig(tk.END, {'bg': 'lightgreen'})
        
            # Center the active student in the frame
            active_students_listbox.pack_propagate(0)
            active_students_listbox.pack(anchor=tk.CENTER)
        
            # Schedule the function to be called again after a period (e.g., every 30 seconds)
            teacher_interface.after(1000, update_active_students_list)
        
        def start_thread():
            # Start a thread for the periodic update of the active students list
            thread = threading.Thread(target=update_active_students_list)
            thread.daemon = True
            thread.start()

        # Create a scrollbar for the Listbox
        scrollbar = tk.Scrollbar(active_students_frame, orient=tk.VERTICAL, command=active_teachers_listbox.yview, bg=common_color)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        active_teachers_listbox.config(yscrollcommand=scrollbar.set)
    
        # Start the thread for periodic updates
        start_thread()

        # Add your predefined messages frame below the active teachers frame
        predefined_messages_frame = tk.Frame(right_frame, borderwidth=2, relief="solid", bg=common_color)
        predefined_messages_frame.pack(side="top", fill="both", expand=True)
    
        # Create a label for the "Predefined Messages" title and place it in the center of the frame
        predefined_messages_title = tk.Label(predefined_messages_frame, text="Predefined Messages", font=("Times", 16,'bold'), bg=common_color)
        predefined_messages_title.place(relx=0.5, rely=0.5, anchor="center")
    
        # Create a Listbox for predefined messages
        predefined_messages_listbox = tk.Listbox(right_frame, selectmode=tk.SINGLE, bg=common_color)
        predefined_messages_listbox.pack(fill=tk.BOTH, expand=True)
                
        # Add predefined messages
        predefined_messages = ["Broadcast: Last 10 minutes remaining for the exam.",
                               "Broadcast: Last 20 minutes remaining for the exam.",
                               "Broadcast: Exam is over."]
    
        for message in predefined_messages:
            predefined_messages_listbox.insert(tk.END, message)

        # Add a broadcast button in the right frame's bottom area
        broadcast_button = tk.Button(right_frame, text="Broadcast", font=common_font,bg='cyan2', fg='black', command=broadcast_message)
        broadcast_button.pack(side="bottom", fill="x", expand=False, padx=10, pady=10)
    
        # Add a line to destroy the course registration window when the teacher interface is opened
        #interface_root.destroy()
    
        teacher_interface.mainloop()
        
    #def open_interface_window():
    def backward():
            # Define what happens when the "Back" button is clicked
            # For example, you can go back to a previous screen or close the window
            interface_root.destroy()  # Close the current window
    
    interface_root = tk.Tk()
    interface_root.title("Course Registeration")
    interface_root.geometry("500x500")
    interface_root.state("zoomed")
    interface_root.configure(bg='light yellow')

    # Create a frame to contain all the elements
    frame = tk.Frame(interface_root, borderwidth=2, relief="solid",bg=common_color)
    frame.pack(pady=50)  # Add padding to center the frame vertically
    
    course_label = tk.Label(frame, text="Course Registration", font=("Times", 30, "bold"), bg=common_color)
    course_label.grid(row=0, column=2, padx=10, pady=10) 
    
    # Create labels and entry widgets
    department_label = tk.Label(frame, text="Department:",font=common_font,bg=common_color)
    department_label.grid(row=1, column=1)
    
    # Create a ComboBox for selecting the department
    departments = ["", "Computer Science", "Information Technology",]
    department_combobox = ttk.Combobox(frame, values=departments)
    department_combobox.grid(row=1, column=2, padx=10, pady=10)
    
    year_label = tk.Label(frame, text="Class:", font=common_font,bg=common_color)
    year_label.grid(row=2, column=1, padx=10, pady=10)
    year_combobox = ttk.Combobox(frame, values=year)
    year_combobox.grid(row=2, column=2, padx=10, pady=10)
    
    semester_label = tk.Label(frame, text="Semester:", font=common_font,bg=common_color)
    semester_label.grid(row=3, column=1, padx=10, pady=10)
    semester_combobox = ttk.Combobox(frame, values=semesters)
    semester_combobox.grid(row=3, column=2, padx=10, pady=10)
    
    subjects_label = tk.Label(frame, text="Subject:", font=common_font,bg=common_color)
    subjects_label.grid(row=4, column=1, padx=10, pady=10)
    subjects_combobox = ttk.Combobox(frame, values=[])
    subjects_combobox.grid(row=4, column=2, padx=10, pady=10)
    
    batch_label = tk.Label(frame, text="Batch:", font=common_font,bg=common_color)
    batch_label.grid(row=5, column=1, padx=10, pady=10)
    batch_combobox = ttk.Combobox(frame, values=batches)
    batch_combobox.grid(row=5, column=2, padx=10, pady=10)
    
    # Add label for class timer
    selected_timer_label = tk.Label(frame, text="Class Timer", font=common_font,bg=common_color)
    selected_timer_label.grid(row=6, column=2, padx=10, pady=10)
    
    # Add Labels and Spin boxes for hours, minutes, and seconds
    hours_label = tk.Label(frame, text="Hours", font=common_font,bg=common_color)
    hours_label.grid(row=7, column=1, padx=10, pady=10)
    hours_spinbox = ttk.Spinbox(frame, from_=0, to=23, width=2)
    hours_spinbox.grid(row=8, column=1, padx=10, pady=10)
    
    minutes_label = tk.Label(frame, text="Minutes", font=common_font,bg=common_color)
    minutes_label.grid(row=7, column=2, padx=10, pady=10)
    minutes_spinbox = ttk.Spinbox(frame, from_=0, to=59, width=2)
    minutes_spinbox.grid(row=8, column=2, padx=10, pady=10)
    
    seconds_label = tk.Label(frame, text="Seconds", font=common_font,bg=common_color)
    seconds_label.grid(row=7, column=3, padx=10, pady=10)
    seconds_spinbox = ttk.Spinbox(frame, from_=0, to=59, width=2)
    seconds_spinbox.grid(row=8, column=3, padx=10, pady=10)

    def next_field(event):
        if event.keycode == 13:
            next_widget = event.widget.tk_focusNext().focus()

    # Bind the next_field function to the <Return> key press event for all widgets in the frame
    for widget in frame.winfo_children():
        if isinstance(widget, (ttk.Entry, ttk.Spinbox, ttk.Combobox)):
            widget.bind('<Return>', next_field)
    
    # Add a "Back" button
    back_button_login = tk.Button(frame, text="Back", font=common_font, bg='red', fg='black', borderwidth=2,relief="solid", command=backward)
    back_button_login.grid(row=10, column=1, padx=10, pady=10, columnspan=2, sticky="ew")
        
    def start_class():
        # Call course_validation to check if all fields are filled
        validation_result = course_validation()
        
        # If validation is successful, open the student interface
        if validation_result:
            start_countdown()
            open_teacher_interface(department_combobox.get(), year_combobox.get(), semester_combobox.get(),
                                   subjects_combobox.get(), batch_combobox.get(), hours_spinbox.get(),
                                   minutes_spinbox.get(), seconds_spinbox.get())
        
    # Modify the "Start Class" button to pass the selected options to the open_teacher_interface function
    start_class_button = tk.Button(frame, text="Start Class",font=common_font, borderwidth=2,relief="solid", command=start_class, bg='green', fg='black')
    start_class_button.grid(row=9, column=1, padx=10, pady=10, columnspan=2, sticky="ew")
    start_class_button.bind('<Return>', lambda event: start_class())

    
    # Center the frame in the window
    frame.place(relx=0.5, rely=0.5, anchor="center")
    
    # Bind the update_subjects function to changes in year and semester Comboboxes
    year_combobox.bind("<<ComboboxSelected>>", update_subjects)
    semester_combobox.bind("<<ComboboxSelected>>", update_subjects)
    
    interface_root.mainloop()

    # Close the server socket
    server_socket.close()