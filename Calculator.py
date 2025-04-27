import tkinter as tk
import re

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 20)
DIGIT_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

LIGHT_GREEN = "#BBD8A3"
WHITE = "#94B4C1"
LIGHT_BLUE = "#9FB3DF"  
LIGHT_GRAY = "#547792"  
LABEL_COLOR = "#213448"
LIGHT_ = "#E8C999"

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(0,0)
        self.window.title("Calculator")
        
        self.total_expression = ""
        self.current_expression = ""
        
        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_labels()
        
        self.buttons_frame = self.create_buttons_frame()
        
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight = 1)
        for y  in range(1, 5):
            self.buttons_frame.columnconfigure(y, weight = 1)
        
        self.window.bind("<Key>", self.key_press)
        
        self.digits = {
            7:(1,1), 8:(1,2), 9:(1,3),
            4:(2,1), 5:(2,2), 6:(2,3),
            1:(3,1), 2:(3,2), 3:(3,3),
            0:(4,1), ".":(4,2)}
        
        self.operations = {
            "/" : "\u00F7",
            "*" : "\u00D7",
            "-" : "-",
            "+" : "+"}
        
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.update_label()
        
    def create_display_frame(self):
        frame = tk.Frame(self.window, 
                         height = 221,
                         bg = LIGHT_GRAY)
        frame.pack(expand = True, fill = "both")
        return frame
    
    def create_display_labels(self):
        total_label = tk.Label(self.display_frame,
                               text = self.total_expression,
                               anchor = tk.E,
                               bg = WHITE,
                               fg = LABEL_COLOR,
                               padx = 24,
                               font = LARGE_FONT_STYLE)
        total_label.pack(expand = True, fill = "both")
        label = tk.Label(self.display_frame, 
                         text = self.current_expression,
                         anchor = tk.E,
                         bg = WHITE,
                         fg = LABEL_COLOR,
                         padx = 24,
                         font = LARGE_FONT_STYLE)
        label.pack(expand = True, fill = "both")
        return total_label, label
    
    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand = True, fill = "both")
        return frame
    
    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()
    
    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame,
                               text = str(digit),
                               bg = LIGHT_GRAY,
                               fg = LABEL_COLOR,
                               font = DIGIT_FONT_STYLE,
                               borderwidth = 1,
                               command = lambda x = digit : self.add_to_expression(x))
            button.grid(row = grid_value[0], column =grid_value[1], sticky = tk.NSEW)
    
    def append_operator(self, operator):
        self.total_expression += self.current_expression + operator
        self.current_expression = ""
        self.update_total_label()
        self.update_label()
                
    def create_operator_buttons(self):
        i = 0
        for operator , symbol in self.operations.items():
            buttons = tk.Button(self.buttons_frame,
                                text = symbol,
                                bg = LIGHT_GRAY,
                                fg = LABEL_COLOR,
                                font = DEFAULT_FONT_STYLE,
                                borderwidth = 1,
                                command = lambda x = operator : self.append_operator(x))
            buttons.grid(row = i, column = 4, sticky = tk.NSEW)
            i += 1
    
    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()
        
    def create_clear_button(self):
        button = tk.Button(self.buttons_frame,
                           text= "C",
                           bg = LIGHT_GRAY,
                           fg = LABEL_COLOR,
                           font = DEFAULT_FONT_STYLE,
                           borderwidth = 1,
                           command = self.clear)
        button.grid(row = 0, column = 2, sticky = tk.NSEW)
        
    def evaluate(self):
        self.total_expression += self.current_expression
        try :
            self.current_expression = str(eval(self.total_expression))
        except Exception as e :
            self.current_expression = "Error"
        finally :
            self.total_expression = ""
            self.update_label()
            self.update_total_label()
         
    def create_equals_button(self):
        button = tk.Button(self.buttons_frame,
                           text= "=",
                           bg = LIGHT_GRAY,
                           fg = LABEL_COLOR,
                           font = DEFAULT_FONT_STYLE,
                           borderwidth = 1,
                           command = self.evaluate)
        button.grid(row = 4, column = 3, columnspan =2, sticky = tk.NSEW) 
        
    def backspace(self):
        self.current_expression = self.current_expression[:-1]
        self.update_label()
        
    def  create_backspace_button(self):
        button = tk.Button(self.buttons_frame,
                           text = "⌫",
                           bg = LIGHT_GRAY,
                           fg = LABEL_COLOR,
                           font = DEFAULT_FONT_STYLE,
                           borderwidth = 1,
                           command = self.backspace)
        button.grid(row = 0, column = 1, sticky = tk.NSEW)
    
    def percentage(self):
        try:
            if self.total_expression and self.current_expression:
               base_expr = self.total_expression.rstrip("+-*/")
               base_value = eval(base_expr) if base_expr else 0
               
               percent_value = eval(self.current_expression)
               result = base_value * (percent_value / 100)
               self.current_expression = str(result)
            else:
                self.current_expression = str(eval(self.current_expression) / 100)
        except Exception:
            self.current_expression = "Error"
            self.update_label()
            
    def cretae_percentage_button(self):
        button = tk.Button(self.buttons_frame,
                           text = "%",
                           bg = LIGHT_GRAY,
                           fg = LABEL_COLOR,
                           font = DEFAULT_FONT_STYLE,
                           borderwidth = 1,
                           command = self.percentage)
        button.grid(row = 0, column = 3, sticky = tk.NSEW)
         
    def key_press(self, event):
        print(f"Pressed : {event.char} | keysym : {event.keysym}")
        key = event.char
        if key.isdigit() or key == ".":
            self.add_to_expression(key)
        elif key in self.operations:
            self.append_operator(key)
        elif event.keysym == "Return":
            self.evaluate()
        elif event.keysym == "BackSpace":
            self.backspace()
        elif key.lower() == "c":
            self.clear()  
        elif key == "%":
            self.percentage() 
    
    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_backspace_button()
        self.cretae_percentage_button()
        
    def update_total_label(self):
        self.total_label.config(text = self.total_expression)
        
    def update_label(self):
        self.label.config(text = self.current_expression)
    
    def run(self):
        self.window.mainloop()
        
if __name__ == "__main__":
    calc = Calculator()
    calc.run()