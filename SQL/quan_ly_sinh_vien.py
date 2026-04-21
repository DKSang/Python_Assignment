import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class StudentManagementApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Student Management Software")
        self.master.geometry("950x600")
        
        self.db_file = 'student_list.db'
        self.init_db()
        
        self.build_ui()
        self.load_data()
        self.write_log("Application started successfully.")

    def init_db(self):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS student (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                major TEXT NOT NULL,
                gpa REAL
            )
        ''')
        
        cur.execute("SELECT COUNT(*) FROM student")
        if cur.fetchone()[0] == 0:
            sample_data = [
                ('Tran Van A', 'Information Technology', 3.2),
                ('Le Thi B', 'Data Science', 3.8),
                ('Pham Van C', 'Information Security', 1.5),
                ('Hoang Thi D', 'Information Systems', 4.0)
            ]
            cur.executemany("INSERT INTO student (full_name, major, gpa) VALUES (?, ?, ?)", sample_data)
        conn.commit()
        conn.close()

    def build_ui(self):
        lbl_title = tk.Label(self.master, text="STUDENT MANAGEMENT SOFTWARE", font=("Helvetica", 18, "bold"), fg="#2c3e50")
        lbl_title.pack(pady=10)
        
        main_frame = tk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        left_frame = tk.LabelFrame(main_frame, text=" Student Information ", font=("Helvetica", 11))
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)
        
        tk.Label(left_frame, text="Full Name:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.txt_fullname = ttk.Entry(left_frame, width=25)
        self.txt_fullname.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(left_frame, text="Major:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        self.txt_major = ttk.Entry(left_frame, width=25)
        self.txt_major.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(left_frame, text="GPA Score:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        self.txt_gpa = ttk.Entry(left_frame, width=25)
        self.txt_gpa.grid(row=2, column=1, padx=10, pady=10)
        
        btn_frame = tk.Frame(left_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Add New", command=self.add_student).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="Update GPA", command=self.update_gpa).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(btn_frame, text="Delete (< 2.0)", command=self.delete_weak_students).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="Filter Good", command=self.filter_good_students).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(btn_frame, text="Refresh List", command=self.load_data).grid(row=2, column=0, columnspan=2, pady=5, sticky="we")
        
        tk.Label(left_frame, text="System Log:", font=("Helvetica", 9, "italic")).grid(row=4, column=0, sticky=tk.W, padx=10, pady=(15, 0))
        self.txt_log = tk.Text(left_frame, height=8, width=35, state=tk.DISABLED, bg="#f9f9f9", font=("Consolas", 9))
        self.txt_log.grid(row=5, column=0, columnspan=2, pady=5, padx=10)
        
        right_frame = tk.LabelFrame(main_frame, text=" Student List ", font=("Helvetica", 11))
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("id", "name", "major", "gpa")
        self.student_table = ttk.Treeview(right_frame, columns=columns, show="headings")
        self.student_table.heading("id", text="ID")
        self.student_table.heading("name", text="Full Name")
        self.student_table.heading("major", text="Major")
        self.student_table.heading("gpa", text="GPA")
        
        self.student_table.column("id", width=60, anchor=tk.CENTER)
        self.student_table.column("name", width=160)
        self.student_table.column("major", width=140)
        self.student_table.column("gpa", width=80, anchor=tk.CENTER)
        
        scrollbar_y = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.student_table.yview)
        self.student_table.configure(yscrollcommand=scrollbar_y.set)
        
        self.student_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.student_table.bind("<<TreeviewSelect>>", self.select_student)

    def load_data(self, query="SELECT * FROM student"):
        for row in self.student_table.get_children():
            self.student_table.delete(row)
            
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        for r in rows:
            self.student_table.insert("", tk.END, values=r)
        conn.close()
        
    def add_student(self):
        name = self.txt_fullname.get().strip()
        major = self.txt_major.get().strip()
        gpa_str = self.txt_gpa.get().strip()
        
        if not name or not major or not gpa_str:
            messagebox.showwarning("Missing Info", "Please enter all fields!")
            return
            
        try:
            gpa = float(gpa_str)
            if gpa < 0 or gpa > 4.0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Data Error", "GPA must be between 0 and 4.0!")
            return
            
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute("INSERT INTO student (full_name, major, gpa) VALUES (?, ?, ?)", (name, major, gpa))
        conn.commit()
        conn.close()
        
        self.write_log(f"[Add] {name} - Major {major} - GPA: {gpa}")
        self.clear_form()
        self.load_data()

    def update_gpa(self):
        selected = self.student_table.selection()
        if not selected:
            messagebox.showinfo("Notice", "Please select a student from the list to update GPA!")
            return
            
        try:
            student_id = self.student_table.item(selected[0])['values'][0]
            new_gpa = float(self.txt_gpa.get())
            if new_gpa < 0 or new_gpa > 4.0:
                raise ValueError
                
            conn = sqlite3.connect(self.db_file)
            cur = conn.cursor()
            cur.execute("UPDATE student SET gpa = ? WHERE student_id = ?", (new_gpa, student_id))
            conn.commit()
            conn.close()
            
            self.write_log(f"[Update] Student ID {student_id} changed GPA to {new_gpa}")
            self.load_data()
        except ValueError:
            messagebox.showerror("Data Error", "Please enter a valid GPA (0 - 4.0)!")

    def delete_weak_students(self):
        ans = messagebox.askyesno("Confirm Action", "System will delete ALL students with GPA < 2.0. Are you sure?")
        if ans:
            conn = sqlite3.connect(self.db_file)
            cur = conn.cursor()
            cur.execute("DELETE FROM student WHERE gpa < 2.0")
            deleted_count = cur.rowcount
            conn.commit()
            conn.close()
            
            self.write_log(f"[Delete] Successfully deleted {deleted_count} students.")
            self.load_data()

    def filter_good_students(self):
        self.write_log("[Filter] Displaying Good students list (GPA > 3.0)")
        self.load_data("SELECT * FROM student WHERE gpa > 3.0")

    def select_student(self, event):
        selected = self.student_table.selection()
        if selected:
            item = self.student_table.item(selected[0])['values']
            self.clear_form()
            self.txt_fullname.insert(0, item[1])
            self.txt_major.insert(0, item[2])
            self.txt_gpa.insert(0, item[3])

    def clear_form(self):
        self.txt_fullname.delete(0, tk.END)
        self.txt_major.delete(0, tk.END)
        self.txt_gpa.delete(0, tk.END)

    def write_log(self, msg):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.txt_log.config(state=tk.NORMAL)
        self.txt_log.insert(tk.END, f"[{now}] {msg}\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementApp(root)
    root.mainloop()
