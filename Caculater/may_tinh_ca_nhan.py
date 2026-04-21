import tkinter as tk

class CalculatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Personal Calculator")
        self.master.geometry("360x520")
        self.master.resizable(False, False)
        self.master.configure(bg="#e8f4f8") 
        
        self.expression = tk.StringVar(value="")
        
        self.create_display()
        self.create_buttons()

    def create_display(self):
        display_label = tk.Label(
            self.master, 
            textvariable=self.expression, 
            font=("Consolas", 32, "bold"),
            bg="#e8f4f8", 
            fg="#2c3e50", 
            anchor="e", 
            padx=20, 
            pady=30
        )
        display_label.pack(fill="both")

    def handle_click(self, char):
        current = self.expression.get()
        
        if char == "=":
            try:
                result = eval(current)
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                new_string = str(result)
            except Exception:
                new_string = "Error"
        elif char == "AC":
            new_string = ""
        elif char == "Del":
            new_string = current[:-1]
        else:
            if len(current) < 15:
                new_string = current + char
            else:
                new_string = current
                
        self.expression.set(new_string)

    def create_buttons(self):
        button_frame = tk.Frame(self.master, bg="#e8f4f8")
        button_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        button_layout = [
            ["AC", "Del", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]
        
        for row_index, row in enumerate(button_layout):
            row_frame = tk.Frame(button_frame, bg="#e8f4f8")
            row_frame.pack(expand=True, fill="both")
            
            for col_index, btn_text in enumerate(row):
                if btn_text == "=":
                    bg_color = "#2980b9"
                    fg_color = "white"
                    active_bg = "#3498db"
                elif btn_text in ["AC", "Del", "%", "/", "*", "-", "+"]:
                    bg_color = "#bdc3c7"
                    fg_color = "#2c3e50"
                    active_bg = "#95a5a6"
                else:
                    bg_color = "white"
                    fg_color = "#2c3e50"
                    active_bg = "#ecf0f1"

                btn = tk.Button(
                    row_frame, 
                    text=btn_text, 
                    font=("Consolas", 16, "bold"),
                    bg=bg_color, 
                    fg=fg_color, 
                    activebackground=active_bg,
                    activeforeground=fg_color,
                    bd=0, 
                    relief="flat", 
                    cursor="hand2",
                    command=lambda k=btn_text: self.handle_click(k)
                )
                
                btn.pack(side="left", expand=True, fill="both", padx=5, pady=5)

if __name__ == "__main__":
    window = tk.Tk()
    app = CalculatorApp(window)
    window.mainloop()
