import tkinter as tk
from tkinter import ttk
import math
import cmath
from datetime import datetime

# Color scheme
BG_GRADIENT = "#1E293B"
BTN_COLOR = "#374151"
BTN_HIGHLIGHT = "#3B82F6"
BTN_TEXT_COLOR = "#F9FAFB"
DISPLAY_COLOR = "#111827"
HISTORY_BG = "#1F2937"
FONT_DISPLAY = ('Segoe UI', 28, 'bold')
FONT_BTN = ('Segoe UI', 14, 'bold')
FONT_HISTORY = ('Segoe UI', 12)

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Scientific Calculator")
        self.root.geometry("500x700")
        self.root.config(bg=BG_GRADIENT)
        self.root.resizable(False, False)

        self.display_var = tk.StringVar()
        self.history = []
        self.mode = tk.StringVar(value="DEG")  # Degree or Radian mode
        self.setup_ui()

    def setup_ui(self):
        # Main frame with gradient effect
        main_frame = tk.Frame(self.root, bg=BG_GRADIENT)
        main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Display
        display = tk.Entry(main_frame, textvariable=self.display_var, bg=DISPLAY_COLOR,
                         fg=BTN_TEXT_COLOR, font=FONT_DISPLAY, bd=0, relief='flat',
                         justify='right')
        display.pack(pady=10, padx=10, fill="x")
        self.display_var.set("")

        # Mode selector
        mode_frame = tk.Frame(main_frame, bg=BG_GRADIENT)
        mode_frame.pack(fill="x", pady=5)
        tk.Radiobutton(mode_frame, text="DEG", variable=self.mode, value="DEG",
                      bg=BG_GRADIENT, fg=BTN_TEXT_COLOR, font=FONT_BTN,
                      selectcolor=BTN_HIGHLIGHT).pack(side="left", padx=5)
        tk.Radiobutton(mode_frame, text="RAD", variable=self.mode, value="RAD",
                      bg=BG_GRADIENT, fg=BTN_TEXT_COLOR, font=FONT_BTN,
                      selectcolor=BTN_HIGHLIGHT).pack(side="left", padx=5)

        # Button frame
        btn_frame = tk.Frame(main_frame, bg=BG_GRADIENT)
        btn_frame.pack(fill="both", expand=True)

        # History display
        self.history_text = tk.Text(main_frame, height=5, bg=HISTORY_BG,
                                  fg=BTN_TEXT_COLOR, font=FONT_HISTORY, bd=0)
        self.history_text.pack(pady=5, padx=10, fill="x")
        self.history_text.config(state="disabled")

        # Button layout with explicit multiplication
        buttons = [
            ("C", "←", "(", ")", "÷", "x²"),
            ("sin", "cos", "tan", "log", "ln", "√"),
            ("7", "8", "9", "π", "e", "*"),  # Multiplication button added here
            ("4", "5", "6", "n!", "1/x", "-"),
            ("1", "2", "3", "abs", "mod", "+"),
            ("0", ".", "±", "exp", "=", "")
        ]

        for i, row in enumerate(buttons):
            for j, char in enumerate(row):
                if char == "":
                    continue
                width = 75 if char != "=" else 160
                btn = tk.Button(btn_frame, text=char, font=FONT_BTN,
                               bg=BTN_COLOR if char not in ("=", "C") else BTN_HIGHLIGHT,
                               fg=BTN_TEXT_COLOR, activebackground=BTN_HIGHLIGHT,
                               bd=0, relief='flat',
                               command=lambda ch=char: self.on_click(ch))
                btn.grid(row=i, column=j, padx=3, pady=3, sticky="nsew")
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#4B5563"))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=BTN_COLOR if b.cget("text") not in ("=", "C") else BTN_HIGHLIGHT))
        
        for i in range(len(buttons)):
            btn_frame.grid_rowconfigure(i, weight=1)
        for j in range(len(buttons[0])):
            btn_frame.grid_columnconfigure(j, weight=1)

    def on_click(self, char):
        current = self.display_var.get()
        
        if char == "C":
            self.display_var.set("")
        elif char == "←":
            self.display_var.set(current[:-1])
        elif char == "=":
            try:
                expr = current.replace('÷', '/').replace('^', '**')
                expr = expr.replace('π', str(math.pi)).replace('e', str(math.e))
                expr = expr.replace('√', 'math.sqrt').replace('ln', 'math.log')
                
                # Handle trigonometric functions based on mode
                mode = self.mode.get()
                for fn in ['sin', 'cos', 'tan']:
                    if mode == "DEG":
                        expr = expr.replace(fn, f"math.{fn}(math.radians")
                    else:
                        expr = expr.replace(fn, f"math.{fn}")
                
                # Handle additional functions
                expr = expr.replace('x²', '**2').replace('xʸ', '**')
                expr = expr.replace('n!', 'math.factorial').replace('abs', 'abs')
                expr = expr.replace('mod', '%').replace('1/x', '1/')
                expr = expr.replace('exp', 'math.exp').replace('log', 'math.log10')
                expr = expr.replace('*', '*')  # Ensure multiplication is handled
                
                result = eval(expr)
                result = str(round(float(result), 10))
                self.display_var.set(result)
                
                # Add to history
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.history.append(f"{timestamp}: {current} = {result}")
                self.update_history()
            except Exception:
                self.display_var.set("Error")
        elif char == "±":
            if current.startswith('-'):
                self.display_var.set(current[1:])
            else:
                self.display_var.set('-' + current)
        else:
            self.display_var.set(current + char)

    def update_history(self):
        self.history_text.config(state="normal")
        self.history_text.delete(1.0, tk.END)
        for entry in self.history[-5:]:  # Show last 5 entries
            self.history_text.insert(tk.END, entry + "\n")
        self.history_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()