import tkinter as tk

class LCDArtApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pro LCD Character Designer")
        self.root.configure(bg="#2c3e50")
        
        self.OFF_COLOR = "#34495e" 
        self.ON_COLOR = "#00d2ff" 
        self.HOVER_COLOR = "#1abc9c"

        self.grid_data = [[0 for _ in range(5)] for _ in range(8)]
        self.buttons = [[None for _ in range(5)] for _ in range(8)]
        
        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self.root, text="LCD PIXEL ART", fg="white", bg="#2c3e50", 
                         font=("Courier", 16, "bold"))
        title.pack(pady=15)

        container = tk.Frame(self.root, bg="black", padx=5, pady=5)
        container.pack()

        for r in range(8):
            row_frame = tk.Frame(container, bg="black")
            row_frame.pack()
            for c in range(5):
                btn = tk.Label(row_frame, width=4, height=2, bg=self.OFF_COLOR, 
                               relief="raised", bd=1)
                btn.pack(side=tk.LEFT, padx=1, pady=1)
                
                # Bind events for clicking and hovering
                btn.bind("<Button-1>", lambda e, r=r, c=c: self.toggle(r, c))
                btn.bind("<Enter>", lambda e, btn=btn: self.on_hover(btn))
                btn.bind("<Leave>", lambda e, r=r, c=c: self.on_leave(r, c))
                
                self.buttons[r][c] = btn

        self.code_box = tk.Text(self.root, height=10, width=35, bg="#1e272e", 
                               fg="#00d2ff", font=("Consolas", 10), bd=0)
        self.code_box.pack(pady=20, padx=20)

        clear_btn = tk.Button(self.root, text="RESET GRID", command=self.clear,
                              bg="#e74c3c", fg="white", font=("Arial", 9, "bold"))
        clear_btn.pack(pady=(0, 20))

        self.update_code()

    def toggle(self, r, c):
        self.grid_data[r][c] = 1 - self.grid_data[r][c]
        color = self.ON_COLOR if self.grid_data[r][c] else self.OFF_COLOR
        self.buttons[r][c].config(bg=color)
        self.update_code()

    def on_hover(self, btn):
        if btn["bg"] == self.OFF_COLOR:
            btn.config(bg=self.HOVER_COLOR)

    def on_leave(self, r, c):
        color = self.ON_COLOR if self.grid_data[r][c] else self.OFF_COLOR
        self.buttons[r][c].config(bg=color)

    def clear(self):
        self.grid_data = [[0 for _ in range(5)] for _ in range(8)]
        for r in range(8):
            for c in range(5):
                self.buttons[r][c].config(bg=self.OFF_COLOR)
        self.update_code()

    def update_code(self):
        code = "byte customChar[8] = {\n"
        for row in self.grid_data:
            bits = "".join(map(str, row))
            code += f"  0b{bits},\n"
        code = code[:-2] + "\n};" 
        self.code_box.delete("1.0", tk.END)
        self.code_box.insert(tk.END, code)

if __name__ == "__main__":
    root = tk.Tk()
    app = LCDArtApp(root)
    root.mainloop()