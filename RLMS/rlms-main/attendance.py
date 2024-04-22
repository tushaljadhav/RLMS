import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
#import openpyxl

def open_attendance_window():
   def mark_attendance():
       student_rollno = entry_name.get()
       attendance_status = attendance_var.get()
       current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       # Check if the entry with the same roll number already exists
       existing_item = None
       for item in tree.get_children():
           if tree.item(item, "values")[2] == student_rollno:
               existing_item = item
               break
       if existing_item:
           # Update attendance status
           tree.item(existing_item, values=(tree.item(existing_item, "values")[0], current_date, student_rollno, attendance_status))
           update_csv_file()
           messagebox.showinfo("Success", f"Attendance status for {student_rollno} updated as {attendance_status}")
       else:
           # Add a new entry
           serial_number = len(tree.get_children()) + 1
           sr_no_display = f"{serial_number})"
           tree.insert("", "end", values=(sr_no_display, current_date, student_rollno, attendance_status))
           with open('attendance.csv', mode='a', newline='') as file:
               writer = csv.writer(file)
               writer.writerow([current_date, student_rollno, attendance_status])
           messagebox.showinfo("Success", f"Attendance for {student_rollno} marked as {attendance_status}")
   def update_csv_file():
       # Update the CSV file with the modified data from the Treeview
       with open('attendance.csv', mode='w', newline='') as file:
           writer = csv.writer(file)
           for item in tree.get_children():
               values = tree.item(item, "values")
               writer.writerow([values[1], values[2], values[3]])
   def clear_fields():
       entry_name.delete(0, tk.END)
       attendance_var.set("Present")
   def go_back():
       root.destroy()
   def delete_all_details():
       for item in tree.get_children():
           tree.delete(item)
       # Clear the CSV file
       with open('attendance.csv', mode='w', newline=''):
           pass
   root = tk.Tk()
   root.title("Student Attendance System")
   
   frame = tk.Frame(root, bd=7, relief=tk.GROOVE)
   frame.pack(pady=50, padx=20)
   
   label_name = tk.Label(frame, text=" Roll.No:", font=("Arial Rounded MT Bold", 12))
   entry_name = tk.Entry(frame, font=("Arial Rounded MT Bold", 12))

   label_attendance = tk.Label(frame, text="Attendance Status:", font=("Arial Rounded MT Bold", 12))
   attendance_var = tk.StringVar()
   attendance_var.set("Present")

   radio_present = tk.Radiobutton(frame, text="Present", variable=attendance_var, value="Present", font=("Arial Rounded MT Bold", 12))
   radio_absent = tk.Radiobutton(frame, text="Absent", variable=attendance_var, value="Absent", font=("Arial Rounded MT Bold", 12))

   mark_button = tk.Button(frame, text="Mark Attendance", command=mark_attendance, font=("Arial Rounded MT Bold", 9), bg="green", fg="white")

   clear_button = tk.Button(frame, text="Clear", command=clear_fields, font=("Arial Rounded MT Bold", 9), bg="orange", fg="white")

   tree = ttk.Treeview(frame, columns=("Sr.No", "Date and time", "Roll.No", "Attendance Status"), show="headings", height=10)

   tree.heading("Sr.No", text="Sr.No")
   tree.heading("Date and time", text="Date and time")
   tree.heading("Roll.No", text="Roll.No")
   tree.heading("Attendance Status", text="Attendance Status")

   tree.column("Sr.No", width=10)

   tree_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)

   tree.configure(yscrollcommand=tree_scrollbar.set)

   label_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
   entry_name.grid(row=0, column=1, padx=10, pady=10, sticky="w")
   label_attendance.grid(row=1, column=0, padx=10, pady=10, sticky="e")
   radio_present.grid(row=1, column=1, padx=10, pady=10, sticky="w")
   radio_absent.grid(row=1, column=2, padx=10, pady=10)
   mark_button.grid(row=2, column=0, pady=10, padx=(0, 10))
   clear_button.grid(row=2, column=1, pady=10, padx=(0, 10))
   tree.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")
   tree_scrollbar.grid(row=3, column=3, pady=10, sticky="ns")

   delete_button = tk.Button(frame, text="Delete All", command=delete_all_details, font=("Arial Rounded MT Bold", 9), bg="blue", fg="white")
   back_button = tk.Button(frame, text="Back", command=go_back, font=("Arial Rounded MT Bold", 9), bg="red", fg="white")
   back_button.grid(row=4, column=0, pady=10, padx=(0, 10))
   delete_button.grid(row=4, column=1, pady=10, padx=(0, 10))

   frame.grid_rowconfigure(3, weight=1)
   frame.grid_columnconfigure(0, weight=1)
   
   root.mainloop()
   # Cll the function to open the attendance window
open_attendance_window()