import tkinter as tk
from tkinter import messagebox

class LCDArtApp:
    def __init__(self, root):
        self.root = root
        self.root.title("16x2 LCD Character Creator")
        self.root.configure(bg="#2c3e50")
        
        # UI Colors
        self.OFF_COLOR = "#34495e" 
        self.ON_COLOR = "#00d2ff" 
        self.HOVER_COLOR = "#1abc9c"
        self.LCD_BG = "#000000"
        self.CODE_BG = "#1e272e"

        # Logic Data
        self.library = [[[0 for _ in range(5)] for _ in range(8)]]
        self.current_char_idx = 0
        self.buttons = [[None for _ in range(5)] for _ in range(8)]
        self.display_data = [[-1 for _ in range(16)] for _ in range(2)]
        self.display_canvases = [[None for _ in range(16)] for _ in range(2)]
        self.pixel_size = 4 
        
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # ==========================================
        # COLUMN 1: Character Editor & Library
        # ==========================================
        col1 = tk.Frame(main_frame, bg="#2c3e50")
        col1.pack(side=tk.LEFT, padx=(0, 25), anchor="n")
        
        tk.Label(col1, text="1. DESIGN", fg="white", bg="#2c3e50", font=("Courier", 14, "bold")).pack(pady=(0,10))

        nav_frame = tk.Frame(col1, bg="#34495e", pady=5, padx=5)
        nav_frame.pack(fill="x", pady=(0, 10))
        
        tk.Button(nav_frame, text="<", command=lambda: self.nav_library(-1), width=3).pack(side=tk.LEFT)
        self.lib_label = tk.Label(nav_frame, text="Char: 0 / 0", bg="#34495e", fg="white", width=12)
        self.lib_label.pack(side=tk.LEFT)
        tk.Button(nav_frame, text=">", command=lambda: self.nav_library(1), width=3).pack(side=tk.LEFT)
        tk.Button(nav_frame, text="+ NEW", bg="#27ae60", fg="black", command=self.add_new_char, font=("Arial", 8, "bold")).pack(side=tk.RIGHT)

        grid_container = tk.Frame(col1, bg="black", padx=4, pady=4)
        grid_container.pack()

        for r in range(8):
            row_frame = tk.Frame(grid_container, bg="black")
            row_frame.pack()
            for c in range(5):
                btn = tk.Label(row_frame, width=4, height=2, bg=self.OFF_COLOR, relief="raised", bd=1)
                btn.pack(side=tk.LEFT, padx=1, pady=1)
                btn.bind("<Button-1>", lambda e, r=r, c=c: self.toggle_pixel(r, c))
                self.buttons[r][c] = btn

        tk.Button(col1, text="DELETE CURRENT CHAR", bg="#c0392b", fg="black", 
                  command=self.delete_current_char, font=("Arial", 8)).pack(fill="x", pady=10)

        # ==========================================
        # COLUMN 2: 16x2 Display Preview
        # ==========================================
        col2 = tk.Frame(main_frame, bg="#2c3e50")
        col2.pack(side=tk.LEFT, padx=(0, 25), anchor="n")
        
        tk.Label(col2, text="2. PREVIEW", fg="white", bg="#2c3e50", font=("Courier", 14, "bold")).pack(pady=(0,10))
        
        lcd_bezel = tk.Frame(col2, bg=self.LCD_BG, padx=10, pady=10, bd=5, relief="sunken")
        lcd_bezel.pack()

        for r in range(2):
            row_frame = tk.Frame(lcd_bezel, bg=self.LCD_BG)
            row_frame.pack(pady=2) 
            for c in range(16):
                canv = tk.Canvas(row_frame, width=5*self.pixel_size, height=8*self.pixel_size, 
                                 bg=self.OFF_COLOR, highlightthickness=0)
                canv.pack(side=tk.LEFT, padx=2)
                canv.bind("<Button-1>", lambda e, r=r, c=c: self.stamp_character(r, c))
                canv.bind("<Button-3>", lambda e, r=r, c=c: self.erase_character(r, c))
                self.display_canvases[r][c] = canv

        tk.Button(col2, text="CLEAR LCD SCREEN", bg="#7f8c8d", fg="black", 
                  command=self.clear_display, font=("Arial", 8)).pack(pady=10)
        
        instruction = tk.Label(col2, text="Left-Click: Stamp Char\nRight-Click: Erase Cell", 
                               fg="#bdc3c7", bg="#2c3e50", font=("Arial", 8, "italic"))
        instruction.pack()

        # ==========================================
        # COLUMN 3: Generated Code
        # ==========================================
        col3 = tk.Frame(main_frame, bg="#2c3e50")
        col3.pack(side=tk.LEFT, fill="y", anchor="n")
        
        tk.Label(col3, text="3. ARDUINO CODE", fg="white", bg="#2c3e50", font=("Courier", 14, "bold")).pack(pady=(0,10))

        self.code_box = tk.Text(col3, height=25, width=45, bg=self.CODE_BG, 
                               fg="#00d2ff", font=("Consolas", 9), padx=10, pady=10)
        self.code_box.pack(fill="both", expand=True)
        
        copy_btn = tk.Button(col3, text="COPY TO CLIPBOARD", bg="#2980b9", fg="black", 
                             command=self.copy_to_clipboard, font=("Arial", 9, "bold"))
        copy_btn.pack(fill="x", pady=(10, 0))

        self.update_ui_state()

    # --- UI Logic ---
    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.code_box.get("1.0", tk.END))
        messagebox.showinfo("Success", "Code copied to clipboard!")

    def nav_library(self, direction):
        self.current_char_idx = (self.current_char_idx + direction) % len(self.library)
        self.update_ui_state()

    def add_new_char(self):
        self.library.append([[0 for _ in range(5)] for _ in range(8)])
        self.current_char_idx = len(self.library) - 1
        self.update_ui_state()

    def delete_current_char(self):
        if len(self.library) > 1:
            deleted_idx = self.current_char_idx
            self.library.pop(deleted_idx)
            for r in range(2):
                for c in range(16):
                    if self.display_data[r][c] == deleted_idx:
                        self.display_data[r][c] = -1
                    elif self.display_data[r][c] > deleted_idx:
                        self.display_data[r][c] -= 1
            self.current_char_idx = max(0, self.current_char_idx - 1)
            self.update_ui_state()
            self.update_all_canvases()

    def toggle_pixel(self, r, c):
        char_data = self.library[self.current_char_idx]
        char_data[r][c] = 1 - char_data[r][c]
        self.update_ui_state()
        self.update_all_canvases()

    def stamp_character(self, r, c):
        self.display_data[r][c] = self.current_char_idx
        self.draw_char_on_canvas(r, c)
        self.update_code()

    def erase_character(self, r, c):
        self.display_data[r][c] = -1
        self.draw_char_on_canvas(r, c)
        self.update_code()

    def update_ui_state(self):
        self.lib_label.config(text=f"Char: {self.current_char_idx} / {len(self.library)-1}")
        char_data = self.library[self.current_char_idx]
        for r in range(8):
            for c in range(5):
                color = self.ON_COLOR if char_data[r][c] else self.OFF_COLOR
                self.buttons[r][c].config(bg=color)
        self.update_code()

    def draw_char_on_canvas(self, r, c):
        canv = self.display_canvases[r][c]
        canv.delete("all")
        char_idx = self.display_data[r][c]
        if char_idx != -1:
            char_data = self.library[char_idx]
            for pr in range(8):
                for pc in range(5):
                    if char_data[pr][pc] == 1:
                        x1, y1 = pc*self.pixel_size, pr*self.pixel_size
                        canv.create_rectangle(x1, y1, x1+self.pixel_size, y1+self.pixel_size, fill=self.ON_COLOR, outline="")

    def update_all_canvases(self):
        for r in range(2):
            for c in range(16):
                self.draw_char_on_canvas(r, c)

    def clear_display(self):
        self.display_data = [[-1 for _ in range(16)] for _ in range(2)]
        self.update_all_canvases()
        self.update_code()

    def update_code(self):
        used_indices = sorted(list(set(cell for row in self.display_data for cell in row if cell != -1)))
        
        code = "// LCD Custom Graphics Generated Code\n"
        code += "#include <LiquidCrystal.h>\n\n"
        
        if len(used_indices) > 8:
            code += "// !!! WARNING: HARDWARE LIMIT EXCEEDED (MAX 8 UNIQUE CHARS) !!!\n"
            
        char_defs = ""
        setup_logic = "void setup() {\n  // lcd.begin(16, 2);\n"
        
        lib_to_hw = {}
        for hw_idx, lib_idx in enumerate(used_indices):
            if hw_idx < 8:
                lib_to_hw[lib_idx] = hw_idx
                char_defs += f"byte char{hw_idx}[8] = {{\n"
                for row in self.library[lib_idx]:
                    bits = "".join(map(str, row))
                    char_defs += f"  0b{bits},\n"
                char_defs = char_defs[:-2] + "\n};\n\n"
                setup_logic += f"  lcd.createChar({hw_idx}, char{hw_idx});\n"
        
        print_logic = "\n  // Display Layout\n"
        for r in range(2):
            for c in range(16):
                lib_idx = self.display_data[r][c]
                if lib_idx in lib_to_hw:
                    hw_idx = lib_to_hw[lib_idx]
                    print_logic += f"  lcd.setCursor({c}, {r}); lcd.write(byte({hw_idx}));\n"

        final_code = code + char_defs + setup_logic + print_logic + "}"
        self.code_box.delete("1.0", tk.END)
        self.code_box.insert(tk.END, final_code)

if __name__ == "__main__":
    root = tk.Tk()
    app = LCDArtApp(root)
    root.mainloop()