import json
import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Scrollbar
from tkinter import ttk
from datetime import datetime

# File to store data
DATA_FILE = 'sports_data.json'

# Load existing data or create a new structure
def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save data to JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Add a student to a specific sport and age category
def add_student(sports_data, sport, age_category, student_info):
    if sport not in sports_data:
        sports_data[sport] = {}
    if age_category not in sports_data[sport]:
        sports_data[sport][age_category] = []
    sports_data[sport][age_category].append(student_info)
    save_data(sports_data)

# View students in a specific sport and age category
def view_students(sports_data, sport, age_category, name_filter=None):
    students = sports_data.get(sport, {}).get(age_category, [])
    if name_filter:
        students = [student for student in students if name_filter in student['name']]
    return students

# Edit student info
def edit_student(sports_data, sport, age_category, index, updated_info):
    if sport in sports_data and age_category in sports_data[sport]:
        if 0 <= index < len(sports_data[sport][age_category]):
            sports_data[sport][age_category][index] = updated_info
            save_data(sports_data)

class SportsManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sports System - Amrita Vdyalayam")
        self.sports_data = load_data()

        # Create tab control
        self.tab_control = ttk.Notebook(self.root)

        # Create tabs
        self.add_tab = ttk.Frame(self.tab_control)
        self.view_tab = ttk.Frame(self.tab_control)
        self.edit_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.add_tab, text="Add Student")
        self.tab_control.add(self.view_tab, text="View Students")
        self.tab_control.add(self.edit_tab, text="Edit Student")
        self.tab_control.pack(expand=1, fill='both')

        self.create_add_student_tab()
        self.create_view_students_tab()
        self.create_edit_student_tab()

    def create_add_student_tab(self):
        # Create fields for adding student
        self.sport_entry = self.create_placeholder_entry(self.add_tab, "Enter Sport")
        self.age_entry = self.create_placeholder_entry(self.add_tab, "Enter Age Category")
        self.name_entry = self.create_placeholder_entry(self.add_tab, "Enter Name")
        self.class_entry = self.create_placeholder_entry(self.add_tab, "Enter Class")
        self.sect_entry = self.create_placeholder_entry(self.add_tab, "Enter Section")
        self.birth_entry = self.create_placeholder_entry(self.add_tab, "Enter Birth Date (YYYY-MM-DD)")
        self.father_entry = self.create_placeholder_entry(self.add_tab, "Enter Father's Name")
        self.mother_entry = self.create_placeholder_entry(self.add_tab, "Enter Mother's Name")
        self.phone_entry = self.create_placeholder_entry(self.add_tab, "Enter Phone No")
        self.email_entry = self.create_placeholder_entry(self.add_tab, "Enter Email (optional)")

        add_button = tk.Button(self.add_tab, text="Add Student", command=self.add_student)
        add_button.pack(pady=10)

    def create_placeholder_entry(self, parent, placeholder):
        entry = tk.Entry(parent, width=30)
        entry.pack(pady=5)
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda e: self.on_entry_click(entry, placeholder))
        entry.bind("<FocusOut>", lambda e: self.on_focusout(entry, placeholder))
        return entry

    def on_entry_click(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)  # Clear the placeholder
            entry.config(fg='black')  # Change text color to black

    def on_focusout(self, entry, placeholder):
        if entry.get() == '':
            entry.insert(0, placeholder)  # Restore placeholder
            entry.config(fg='grey')  # Change text color to grey

    def create_view_students_tab(self):
        # Search fields
        self.view_sport_entry = self.create_placeholder_entry(self.view_tab, "Enter Sport")
        self.view_age_entry = self.create_placeholder_entry(self.view_tab, "Enter Age Category")
        self.view_name_entry = self.create_placeholder_entry(self.view_tab, "Enter Name (optional)")

        view_button = tk.Button(self.view_tab, text="View Students", command=self.view_students)
        view_button.pack(pady=5)

        view_all_button = tk.Button(self.view_tab, text="View All Students", command=self.view_all_students)
        view_all_button.pack(pady=5)

        self.view_text_area = tk.Text(self.view_tab, width=60, height=20)
        self.view_text_area.pack(pady=10)

    def create_edit_student_tab(self):
        self.edit_sport_entry = self.create_placeholder_entry(self.edit_tab, "Enter Sport")
        self.edit_age_entry = self.create_placeholder_entry(self.edit_tab, "Enter Age Category")
        self.edit_index_entry = self.create_placeholder_entry(self.edit_tab, "Enter Student Index (0-based)")

        edit_button = tk.Button(self.edit_tab, text="Load Student for Editing", command=self.load_student_for_edit)
        edit_button.pack(pady=10)

        self.edit_name_entry = self.create_placeholder_entry(self.edit_tab, "Edit Name")
        self.edit_class_entry = self.create_placeholder_entry(self.edit_tab, "Edit Class")
        self.edit_sect_entry = self.create_placeholder_entry(self.edit_tab, "Edit Section")
        self.edit_birth_entry = self.create_placeholder_entry(self.edit_tab, "Edit Birth Date (YYYY-MM-DD)")
        self.edit_father_entry = self.create_placeholder_entry(self.edit_tab, "Edit Father's Name")
        self.edit_mother_entry = self.create_placeholder_entry(self.edit_tab, "Edit Mother's Name")
        self.edit_phone_entry = self.create_placeholder_entry(self.edit_tab, "Edit Phone No")
        self.edit_email_entry = self.create_placeholder_entry(self.edit_tab, "Edit Email (optional)")

        update_button = tk.Button(self.edit_tab, text="Update Student", command=self.update_student)
        update_button.pack(pady=10)

    def add_student(self):
        sport = self.sport_entry.get().lower()
        age_category = self.age_entry.get().lower()
        student_info = {
            "name": self.name_entry.get().lower(),
            "class": self.class_entry.get().lower(),
            "sect": self.sect_entry.get().lower(),
            "birth_date": self.birth_entry.get().lower(),
            "current_date": datetime.now().strftime("%Y-%m-%d"),
            "father_name": self.father_entry.get().lower(),
            "mother_name": self.mother_entry.get().lower(),
            "phone_no": self.phone_entry.get().lower(),
            "email": self.email_entry.get().lower()
        }
        add_student(self.sports_data, sport, age_category, student_info)
        index = len(self.sports_data[sport][age_category]) - 1  # Get the index of the newly added student
        messagebox.showinfo("Success", "Student added successfully!")
        self.show_preview_alert(student_info, index)
        self.clear_add_student_fields()

    def clear_add_student_fields(self):
        for entry in [self.sport_entry, self.age_entry, self.name_entry, self.class_entry,
                      self.sect_entry, self.birth_entry, self.father_entry, self.mother_entry,
                      self.phone_entry, self.email_entry]:
            entry.delete(0, tk.END)
            entry.insert(0, entry['placeholder'])
            entry.config(fg='grey')

    def show_preview_alert(self, student_info, index):
        alert_message = f"Student Added (Index {index}):\n\n"
        for key, value in student_info.items():
            alert_message += f"{key.replace('_', ' ').title()}: {value}\n"
        messagebox.showinfo("Student Preview", alert_message)

    def view_students(self):
        sport = self.view_sport_entry.get().lower()
        age_category = self.view_age_entry.get().lower()
        name_filter = self.view_name_entry.get().lower()
        students = view_students(self.sports_data, sport, age_category, name_filter)
        
        self.view_text_area.delete(1.0, tk.END)  # Clear previous content

        if students:
            for idx, student in enumerate(students):
                self.view_text_area.insert(tk.END, f"Student {idx + 1}:\n")  # Show student number
                self.view_text_area.insert(tk.END, f"Name: {student['name']}\n")
                self.view_text_area.insert(tk.END, f"Class: {student['class']}\n")
                self.view_text_area.insert(tk.END, f"Section: {student['sect']}\n")
                self.view_text_area.insert(tk.END, f"Birth Date: {student['birth_date']}\n")
                self.view_text_area.insert(tk.END, f"Current Date: {student['current_date']}\n")
                self.view_text_area.insert(tk.END, f"Father's Name: {student['father_name']}\n")
                self.view_text_area.insert(tk.END, f"Mother's Name: {student['mother_name']}\n")
                self.view_text_area.insert(tk.END, f"Phone No: {student['phone_no']}\n")
                self.view_text_area.insert(tk.END, f"Email: {student['email']}\n\n")
        else:
            self.view_text_area.insert(tk.END, "No students found.")

    def view_all_students(self):
        sport = self.view_sport_entry.get().lower()
        age_category = self.view_age_entry.get().lower()
        students = self.sports_data.get(sport, {}).get(age_category, [])

        if not students:
            messagebox.showinfo("Info", "No students found for the selected sport and age category.")
            return

        self.show_students_in_scrollable_alert(students)

    def show_students_in_scrollable_alert(self, students):
        alert_window = Toplevel(self.root)
        alert_window.title("All Students")
        
        text_area = tk.Text(alert_window, width=80, height=20)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = Scrollbar(alert_window, command=text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_area.config(yscrollcommand=scrollbar.set)

        alert_message = "All Students:\n\n"
        for idx, student in enumerate(students):
            alert_message += f"Index: {idx}\n"
            alert_message += f"Name: {student['name']}\n"
            alert_message += f"Class: {student['class']}\n"
            alert_message += f"Section: {student['sect']}\n"
            alert_message += f"Birth Date: {student['birth_date']}\n"
            alert_message += f"Current Date: {student['current_date']}\n"
            alert_message += f"Father's Name: {student['father_name']}\n"
            alert_message += f"Mother's Name: {student['mother_name']}\n"
            alert_message += f"Phone No: {student['phone_no']}\n"
            alert_message += f"Email: {student['email']}\n"
            alert_message += "-" * 40 + "\n"

        text_area.insert(tk.END, alert_message)

    def load_student_for_edit(self):
        sport = self.edit_sport_entry.get().lower()
        age_category = self.edit_age_entry.get().lower()
        index = simpledialog.askinteger("Input", "Enter the index of the student to edit (0-based):")

        if index is not None:
            students = view_students(self.sports_data, sport, age_category)
            if 0 <= index < len(students):
                student = students[index]
                self.edit_name_entry.delete(0, tk.END)
                self.edit_name_entry.insert(0, student["name"])
                self.edit_class_entry.delete(0, tk.END)
                self.edit_class_entry.insert(0, student["class"])
                self.edit_sect_entry.delete(0, tk.END)
                self.edit_sect_entry.insert(0, student["sect"])
                self.edit_birth_entry.delete(0, tk.END)
                self.edit_birth_entry.insert(0, student["birth_date"])
                self.edit_father_entry.delete(0, tk.END)
                self.edit_father_entry.insert(0, student["father_name"])
                self.edit_mother_entry.delete(0, tk.END)
                self.edit_mother_entry.insert(0, student["mother_name"])
                self.edit_phone_entry.delete(0, tk.END)
                self.edit_phone_entry.insert(0, student["phone_no"])
                self.edit_email_entry.delete(0, tk.END)
                self.edit_email_entry.insert(0, student["email"])
            else:
                messagebox.showerror("Error", "Invalid index.")
        else:
            messagebox.showerror("Error", "Please enter a valid index.")

    def update_student(self):
        sport = self.edit_sport_entry.get().lower()
        age_category = self.edit_age_entry.get().lower()
        index = simpledialog.askinteger("Input", "Enter the index of the student to update (0-based):")
        
        if index is not None:
            updated_info = {
                "name": self.edit_name_entry.get().lower(),
                "class": self.edit_class_entry.get().lower(),
                "sect": self.edit_sect_entry.get().lower(),
                "birth_date": self.edit_birth_entry.get().lower(),
                "current_date": datetime.now().strftime("%Y-%m-%d"),
                "father_name": self.edit_father_entry.get().lower(),
                "mother_name": self.edit_mother_entry.get().lower(),
                "phone_no": self.edit_phone_entry.get().lower(),
                "email": self.edit_email_entry.get().lower()
            }
            edit_student(self.sports_data, sport, age_category, index, updated_info)
            messagebox.showinfo("Success", "Student updated successfully!")
            self.clear_edit_student_fields()
        else:
            messagebox.showerror("Error", "Please enter a valid index.")

    def clear_edit_student_fields(self):
        for entry in [self.edit_name_entry, self.edit_class_entry, self.edit_sect_entry,
                      self.edit_birth_entry, self.edit_father_entry, self.edit_mother_entry,
                      self.edit_phone_entry, self.edit_email_entry]:
            entry.delete(0, tk.END)
            entry.insert(0, entry['placeholder'])
            entry.config(fg='grey')

if __name__ == "__main__":
    root = tk.Tk()
    app = SportsManagementApp(root)
    root.mainloop()
