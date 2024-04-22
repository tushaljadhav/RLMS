import tkinter as tk
from tkinter import messagebox
from tushal import *

# Define a common font
common_font = ('Times', 14, "bold")
common_color = bg='misty rose'

def teacher_button_click():
    messagebox.showinfo("Teacher Button Clicked", "Teacher button clicked")

def student_button_click():
    messagebox.showinfo("Student Button Clicked", "Student button clicked")

# Create the main window
interface_root = tk.Tk()
interface_root.configure(bg='light yellow')
interface_root.title("RMLS")
interface_root.geometry("500x500")  # was 500x500
interface_root.state("zoomed")

# Create a frame to contain all the elements
frame = tk.Frame(interface_root, borderwidth=2, relief="solid", height=800, width=1200, bg= common_color)
frame.pack(pady=50)  # Add padding to center the frame vertically

college_label = tk.Label(
    frame,
    text="""""",
    font=("Times", 16, "bold")
)

# Add an image to the left side
image_path = "C:/Users/Jeevan/OneDrive/Desktop/Startup/rlms.png"  # Change this to the path of your image
image = tk.PhotoImage(file=image_path)
resized_image = image.subsample(1, 1)
image_label = tk.Label(frame, image=resized_image, bg=common_color)
image_label.grid(row=1, column=1, rowspan=8, padx=6, pady=6)
college_label.grid(row=0, column=0, padx=10, pady=10)

course_label = tk.Label(frame, text="REMOTE LAB MONITORING", font=("Times", 30, "bold"), bg=common_color)
course_label.grid(row=1, column=2, padx=15, pady=15, sticky='')

# Add buttons for Teacher and Student
teacher_button = tk.Button(frame, text="Teacher", command=open_teacher, bg='red', fg='black', height=3, width=3, font=('Times', 15, 'bold'))
teacher_button.grid(row=2, column=2, padx=10, pady=10, sticky="ew")

student_button = tk.Button(frame, text="Student", command=student_button_click, bg='green', fg='black', height=3, width=3, font=('Times', 15, 'bold'))
student_button.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

# Run the Tkinter event loop
interface_root.mainloop()