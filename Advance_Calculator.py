import tkinter as tk
from math import *
import re

memory = 0

def safe_eval(expr):
    expr = expr.replace('%', '/100')
    expr = re.sub(r'(\d+)!', r'factorial(\1)', expr)
    return eval(expr)

def evaluate_expression(event=None):
    try:
        expression = entry.get()
        result = safe_eval(expression)
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

def insert_character(char):
    entry.insert(tk.END, char)

def clear_entry():
    entry.delete(0, tk.END)

def backspace():
    entry.delete(len(entry.get()) - 1, tk.END)

def memory_clear():
    global memory
    memory = 0

def memory_recall():
    entry.insert(tk.END, str(memory))

def memory_add():
    global memory
    try:
        memory += float(entry.get())
    except:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

def memory_subtract():
    global memory
    try:
        memory -= float(entry.get())
    except:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

# GUI Setup
root = tk.Tk()
root.title("Scientific Calculator")
root.configure(bg="#2b2b2b")
btn_font = ('Arial', 13)

entry = tk.Entry(root, font=('Arial', 20), width=24, borderwidth=4,
                 relief=tk.FLAT, justify='right', bg="#1e1e1e", fg="white", insertbackground="white")
entry.grid(row=0, column=0, columnspan=4, padx=8, pady=8, sticky='nsew')
entry.focus_set()

# Define color themes
style = {
    "num": {"bg": "#3c3f41", "fg": "white"},
    "op": {"bg": "#4e4e4e", "fg": "lightgray"},
    "func": {"bg": "#4e4e4e", "fg": "lightblue"},
    "act": {"bg": "#d9534f", "fg": "white"},
    "equal": {"bg": "#4078f2", "fg": "white"},
}

# Button layout
buttons = [
    ('C', 'C', 'DEL', '%'),                 
    ('7', '8', '9', '/'),
    ('4', '5', '6', '*'),
    ('1', '2', '3', '-'),
    ('0', '.', '(', ')'),
    ('pi', 'e', 'sqrt', 'log'),
    ('exp', 'fact', 'sin', 'cos'),
    ('tan', '!', 'MC', 'MR'),
    ('M+', 'M-', '=', '')                   
]

# Button creation
for i, row in enumerate(buttons):
    skip = False
    for j, char in enumerate(row):
        if skip:
            skip = False
            continue
        if char == '':
            continue
        if char == '=':
            btn = tk.Button(root, text=char, width=12, height=2, font=btn_font,
                            bg=style["equal"]["bg"], fg=style["equal"]["fg"], command=evaluate_expression)
            btn.grid(row=i + 1, column=j, columnspan=2, padx=2, pady=2, sticky="nsew")
            skip = True
            continue
        elif char == 'C' and j < len(row) - 1 and row[j + 1] == 'C':
            btn = tk.Button(root, text='C', width=12, height=2, font=btn_font,
                            bg=style["act"]["bg"], fg=style["act"]["fg"], command=clear_entry)
            btn.grid(row=i + 1, column=j, columnspan=2, padx=2, pady=2, sticky="nsew")
            skip = True
            continue
        elif char == 'DEL':
            cmd = backspace
        elif char == 'MC':
            cmd = memory_clear
        elif char == 'MR':
            cmd = memory_recall
        elif char == 'M+':
            cmd = memory_add
        elif char == 'M-':
            cmd = memory_subtract
        elif char == 'pi':
            cmd = lambda ch=pi: insert_character(str(ch))
        elif char == 'e':
            cmd = lambda ch=e: insert_character(str(ch))
        elif char in ['fact', '!']:
            cmd = lambda: insert_character('!')
        elif char == '%':
            cmd = lambda: insert_character('%')
        else:
            cmd = lambda ch=char: insert_character(ch)

        # Color style
        if char in '0123456789.()':
            bg, fg = style["num"]["bg"], style["num"]["fg"]
        elif char in ['+', '-', '*', '/', '%']:
            bg, fg = style["op"]["bg"], style["op"]["fg"]
        elif char in ['DEL']:
            bg, fg = style["act"]["bg"], style["act"]["fg"]
        else:
            bg, fg = style["func"]["bg"], style["func"]["fg"]

        tk.Button(root, text=char, width=5, height=2, font=btn_font,
                  command=cmd, bg=bg, fg=fg).grid(row=i + 1, column=j, padx=2, pady=2, sticky="nsew")

def keypress_operator(event):
    insert_character(event.char)
    return "break"

for key in ['+', '-', '*', '/', '%', '!', '.', '(', ')']:
    root.bind(f"<KeyPress-{key}>", keypress_operator)


for key in range(10):
    root.bind(f"<KeyPress-{key}>", lambda e, ch=str(key): insert_character(ch), "break"[1])

root.bind("<Return>", evaluate_expression)
root.bind("<BackSpace>", lambda e: backspace())
root.bind("<Delete>", lambda e: clear_entry())
root.bind("!", lambda e: insert_character('!'))
root.bind("<KeyPress-c>", lambda e: clear_entry())
root.bind("<KeyPress-C>", lambda e: clear_entry())

root.mainloop()
