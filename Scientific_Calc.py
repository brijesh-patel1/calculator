import tkinter as tk
import math
from tkinter import messagebox

# Button Color Themes
style = {
    "num": {"bg": "#3c3f41", "fg": "white"},
    "op": {"bg": "#4e4e4e", "fg": "lightgray"},
    "func": {"bg": "#4e4e4e", "fg": "lightblue"},
    "equal": {"bg": "#4078f2", "fg": "white"},
    "clear": {"bg": "red", "fg": "white"}
}

# Button Layout
buttons = [
    ('C', '', 'DEL', '/'),
    ('7', '8', '9', '*'),
    ('4', '5', '6', '-'),
    ('1', '2', '3', '+'),
    ('0', '.', '(', ')'),
    ('pi', 'e', 'sqrt', 'log'),
    ('exp', '%', 'sin', 'cos'),
    ('tan', '!', 'MC', 'MR'),
    ('M+', 'M-', '=', '')
]

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Scientific Calculator")
        self.window.geometry("420x740")
        self.expression = ""
        self.memory = 0
        self.create_widgets()
        self.bind_keys()

    def create_widgets(self):
        self.display = tk.Entry(self.window, font=("Arial", 24), bd=5, relief=tk.FLAT, justify="right", bg="#1e1e1e", fg="white")
        self.display.pack(expand=True, fill="both")

        button_frame = tk.Frame(self.window, bg="#2b2b2b")
        button_frame.pack(expand=True, fill="both")

        for r, row in enumerate(buttons):
            for c, btn in enumerate(row):
                if not btn:
                    continue
                if btn in "0123456789.":
                    theme = style["num"]
                elif btn in ("+", "-", "*", "/", "(", ")"):
                    theme = style["op"]
                elif btn in ("sqrt", "log", "exp", "sin", "cos", "tan", "pi", "e", "!", "%", "MC", "MR", "M+", "M-"):
                    theme = style["func"]
                elif btn == "=":
                    theme = style["equal"]
                elif btn == "C":
                    theme = style["clear"]
                else:
                    theme = style["op"]

                span = 2 if btn in ("=", "C") else 1
                tk.Button(button_frame, text=btn, font=("Arial", 18),
                          bg=theme["bg"], fg=theme["fg"], border=0,
                          command=lambda x=btn: self.on_button_click(x)
                          ).grid(row=r, column=c, columnspan=span, sticky="nsew", padx=1, pady=1)

        for i in range(len(buttons)):
            button_frame.rowconfigure(i, weight=1)
        for j in range(4):
            button_frame.columnconfigure(j, weight=1)

    def bind_keys(self):
        self.window.bind("<Key>", self.on_key_press)
        self.window.bind("<BackSpace>", self.on_key_press)

    def on_key_press(self, event):
        key = event.char
        if key in "0123456789+-*/.%()":
            self.on_button_click(key)
        elif key == '\r':
            self.on_button_click("=")
        elif key in ('\x08', 'BackSpace'):
            self.on_button_click("DEL")
        elif key in ('c', 'C'):
            self.on_button_click("C")

    def on_button_click(self, btn):
        if btn == "C":
            self.expression = ""
        elif btn == "DEL":
            self.expression = self.expression[:-1]
        elif btn == "=":
            self.evaluate()
        elif btn == "pi":
            self.expression += str(math.pi)
        elif btn == "e":
            self.expression += str(math.e)
        elif btn == "sqrt":
            self.expression += "math.sqrt("
        elif btn == "log":
            self.expression += "math.log10("
        elif btn == "exp":
            self.expression += "math.exp("
        elif btn == "sin":
            self.expression += "math.sin("
        elif btn == "cos":
            self.expression += "math.cos("
        elif btn == "tan":
            self.expression += "math.tan("
        elif btn == "fact" or btn == "!":
            try:
                val = int(eval(self.expression))
                self.expression = str(math.factorial(val))
            except Exception:
                self.expression = "Error"
        elif btn == "MC":
            self.memory = 0
        elif btn == "MR":
            self.expression += str(self.memory)
        elif btn == "M+":
            try:
                self.memory += eval(self.expression)
            except Exception:
                self.memory = 0
        elif btn == "M-":
            try:
                self.memory -= eval(self.expression)
            except Exception:
                self.memory = 0
        elif btn == "%":
            try:
                tokens = self.expression.rstrip('0123456789.')
                last_number = self.expression[len(tokens):]
                if not last_number:
                    return
                if tokens and tokens[-1] in "+-*/":
                    op = tokens[-1]
                    base_expr = tokens[:-1]
                    base_value = eval(base_expr) if base_expr else 0
                    percent_value = base_value * float(last_number) / 100
                    self.expression = base_expr + op + str(percent_value)
                else:
                    self.expression = str(float(last_number) / 100)
            except Exception:
                self.expression = "Error"
        else:
            self.expression += str(btn)

        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expression)

    def evaluate(self):
        try:
            result = eval(self.expression)
            self.expression = str(result)
        except Exception:
            self.expression = "Error"

if __name__ == "__main__":
    calc = Calculator()
    calc.window.mainloop()
