import tkinter as tk, socket, os, threading, psutil, plyer
from tkinter import messagebox, filedialog

# Common_font defined & Common_color
common_font = ('Times', 14, "bold")
common_color = bg='misty rose'

# Get the hostname of the system
global hostname
hostname = socket.gethostname()

# ------------------------------------------ Student Shutdown -----------------------------------------------

# Define server address and port
HOST = '192.168.51.162'  # Teacher's IP address
PORT = 65432

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Create a client socket
#client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client_socket.connect(("192.168.212.247", 65432))  # Replace "server_ip_address" with the server's IP

# Function to continuously listen for commands
def listen_for_commands():
    while True:
        try:
            # Receive data from the teacher
            data = client_socket.recv(1024).decode()
            if not data:
                break
            handle_command(data)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

# Function to handle received commands
def handle_command(command):
    if command == 'shutdown':
        print('Received shutdown command from teacher.')
        shutdown_computer()

# Function to gracefully shut down the computer
def shutdown_computer():
    try:
        # Check the operating system and execute the appropriate shutdown command
        if os.name == 'posix':  # Unix-based systems (Linux, macOS)
            os.system('shutdown -h now')
        elif os.name == 'nt':   # Windows
            os.system('shutdown /s /t 1')
        else:
            print('Unsupported operating system.')
    except Exception as e:
        print(f"Error during shutdown: {e}")
    
# ------------------------------------------- Student Shutdown END --------------------------------------------------------

def open(student_name, student_id):
    # def open_student_interface():
    student_interface = tk.Tk()
    student_interface.title("Student Interface")
    student_interface.geometry("500x500")
    student_interface.state("zoomed")  # Open in a maximized (zoomed) state

    # Set the border width of the window
    student_interface.configure(borderwidth=2, relief="solid")

    # Create the above frame
    above_frame = tk.Frame(student_interface, borderwidth=2, relief="solid",bg=common_color)
    above_frame.pack(side="top", fill="x", expand=False)  # Adjust the height as needed

    # Create left, middle, and right frames within the above frame using grid layout
    left_frame = tk.Frame(above_frame,bg=common_color)
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    middle_frame = tk.Frame(above_frame, relief="solid",bg=common_color)
    middle_frame.grid(row=0, column=1,sticky='e')

    right_frame = tk.Frame(above_frame, relief="solid",bg=common_color)
    right_frame.grid(row=0, column=2, padx=10,pady=10, sticky='en')

    # Configure the grid weights to make the frames expand evenly
    above_frame.grid_rowconfigure(0, weight=1)
    above_frame.grid_columnconfigure(0, weight=1)
    above_frame.grid_columnconfigure(1, weight=1)
    above_frame.grid_columnconfigure(2, weight=1)

    # ------------------------------- Selected Entries Display -----------------------------------------

    # Display the selected options in the student interface
    selected_department_label = tk.Label(left_frame, text=f"Department: Information Teachnology", font=common_font,bg=common_color)
    selected_department_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    student_name_label = tk.Label(left_frame, text=f"Student Name: Pradhnesh Dalvi{student_name}", font=common_font,bg=common_color)
    student_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    student_id_label = tk.Label(left_frame, text=f"Student ID: 2382019{student_id}", font=common_font,bg=common_color)
    student_id_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    selected_semester_label = tk.Label(left_frame, text=f"Semester: Semester 3", font=common_font,bg=common_color)
    selected_semester_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

    selected_year_label = tk.Label(middle_frame, text=f"Class: SYIT", font=common_font,bg=common_color)
    selected_year_label.grid(row=1, column=2, padx=5, pady=5, sticky='e')

    # Add labels or other elements in the middle frame
    label_remote = tk.Label(middle_frame, text="Remote Lab Monitoring System", font=('Times', 30, "bold"),bg=common_color)
    label_remote.grid(row=0, column=2, columnspan=2, sticky='news')

    selected_subjects_label = tk.Label(middle_frame, text=f"Subject: Software Engineering", font=common_font,bg=common_color)
    selected_subjects_label.grid(row=3, column=2, padx=5, pady=5, sticky='e')

    selected_batch_label = tk.Label(middle_frame, text=f"Batch: 1", font=common_font,bg=common_color)
    selected_batch_label.grid(row=2, column=2, padx=5, pady=5, sticky='e')

    selected_timer_label = tk.Label(right_frame, text=f"Class Timer:1 hours,0 minutes,0 seconds", font=common_font,fg='red',bg=common_color)
    selected_timer_label.pack(side="top", fill="both", expand=False, padx=10, pady=5)
    selected_timer_label.grid(row=0, column=0, padx=5, pady=5, sticky='ne')

    def logout():
        # Display a confirmation dialog with "Yes" and "No" buttons
        result = messagebox.askquestion("Confirmation", "Are you sure you want to log out?")
        if result == "yes":
            # Add the code to perform the logout action here
            # For example, you can destroy the student_interface window
            student_interface.destroy()
        else:
            # User canceled the action
            messagebox.showinfo("Log Out Canceled", "Log out operation was canceled.")

    # Create a button to log out
    logout_button = tk.Button(right_frame, text="Log Out", font=common_font, command=logout, bg='red', fg='black')
    logout_button.grid(row=1, column=0, padx=5, pady=5, sticky='ne')

    # ------------------------------ Created Left Right and Middle Frame -----------------------------------------

    # Create the left frame
    left_frame = tk.Frame(student_interface, borderwidth=2, relief="solid",bg=common_color)
    left_frame.pack(side="left", fill="y", expand=False)

    # Create a notification frame
    notification_frame = tk.Frame(left_frame, borderwidth=2, relief="solid",bg=common_color,width=15)
    notification_frame.pack(side="top", fill="both", expand=True)

    # Add notification elements
    notification_label = tk.Label(notification_frame, text="Notifications", font=("Times", 16, "bold"),bg=common_color)
    notification_label.pack(pady=10)

    # Create a Listbox for the chat messages
    notification_text = tk.Listbox(notification_frame, selectmode=tk.SINGLE,bg=common_color,font=common_font)
    notification_text.pack(fill=tk.BOTH, expand=True)

    # Create a vertical scrollbar for the Text widget
    notification_scrollbar = tk.Scrollbar(notification_frame, orient="vertical")
    notification_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    notification_text.config(yscrollcommand=notification_scrollbar.set)

    # Function to clear all notifications in the Listbox
    def clear_notifications():
        notification_text.delete(0, tk.END)

    # Create a button to clear all notifications
    #clear_button = tk.Button(notification_frame, text="Clear Notifications", command=clear_notifications, font=('TImes', 10, 'bold'), bg='sky blue')
    #clear_button.pack(pady=10)

    # Create the center frame
    center_frame = tk.Frame(student_interface, borderwidth=2, relief="solid",bg=common_color)
    center_frame.pack(side="left", fill="both", expand=True)

    # Create a small chatbox frame within the top of the center frame
    chatbox_frame = tk.Frame(center_frame, borderwidth=2, relief="solid",bg=common_color)
    chatbox_frame.pack(side="top", fill="both", expand=True)

    # Add chatbox elements
    chatbox_label = tk.Label(chatbox_frame, text="Chatbox", font=("Times", 16, 'bold'),bg=common_color)
    chatbox_label.pack(pady=10)

    # Create a Listbox for the chat messages
    chat_messages_listbox = tk.Listbox(chatbox_frame, selectmode=tk.SINGLE,bg=common_color,width=8)
    chat_messages_listbox.pack(fill=tk.BOTH, expand=True)

    # Create a scrollbar for the Listbox
    scrollbar = tk.Scrollbar(chatbox_frame, orient=tk.VERTICAL, command=chat_messages_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    chat_messages_listbox.config(yscrollcommand=scrollbar.set)

    # Create a frame for the message entry field and send button at the bottom of the center frame
    message_frame = tk.Frame(center_frame, borderwidth=2, relief="solid",bg=common_color)
    message_frame.pack(side="bottom", fill="x", expand=False)

    # Add a label for the message entry field
    message_label = tk.Label(message_frame, text="Type a message:", font=common_font,bg=common_color)
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
                if data[:9] == "Broadcast":
                    # Extract message content
                    content = data[10:]
                    # Display received message on the GUI
                    notification_text.insert(tk.END, f"Broadcast: {content}\n")
                else:
                    # Display received message as normal
                    chat_messages_listbox.insert(tk.END, f"Teacher: {data}")

            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    # Define function to send messages
    def send_message():
        # Get message from the entry field
        message = message_entry.get()
        # Clear the entry field
        
        # Display sent message in the chatbox
        chat_messages_listbox.insert(tk.END, f"Student: {message}")
        message_entry.delete(0, tk.END)
        # Send message to the teacher
        try:
            client_socket.sendall(message.encode())
        except Exception as e:
            print(f"Error sending message: {e}")

    # Add the "Send" button to the message frame
    send_button = tk.Button(message_frame, text="Send", font=common_font, bg='green', fg='black', command=send_message)
    send_button.pack(side="left", padx=10, pady=10)

    '''# Function to receive files
    def receive_file():
        file_name = client_socket.recv(1024).decode()
        save_path = os.path.join(r"C:/Users/Jeevan/OneDrive/Desktop/aaa", file_name)  # Specify the directory where you want to save the files
    
        with open(save_path, "wb") as file:  # Open the file in binary write mode
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
    
        print(f"File received and saved at: {save_path}")
    
    # Create a directory for received files if it doesn't exist
    if not os.path.exists("received_files"):
        os.mkdir("received_files")

    # Create a thread object and call the start method
    receive_thread = threading.Thread(target=receive_file)
    receive_thread.start()'''

    # Start a thread to listen for commands continuously
    listen_thread = threading.Thread(target=listen_for_commands)
    listen_thread.start()

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    student_interface.mainloop()

    # Close the connection
    client_socket.close()