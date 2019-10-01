import tkinter as tk
from tkinter import ttk
from tkinter import font
import time

def resize(event):

    print(window.winfo_height())
    width = int(window.winfo_width())
    height = int(width/5*3)
    
    window.geometry(f"{width}x{height}+500+100")
    resize.font = font.Font(size=int(window.winfo_width()/15))
    label1.config(font=resize.font)

window = tk.Tk()
window.title("Spotif'Air")
window.geometry("500x300+500+100")
resize.font = ('arial', 10)



window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

Main_Menu = tk.Frame(window, bg='red')
Main_Menu.grid(row=0, column=0, sticky='nsew')
Second = tk .Frame(window, bg='yellow')
Second.grid(row=0, column=0, sticky='nsew')
Main_Menu.tkraise()

label1 = tk.Label(Main_Menu, text="Welcome on Spotif'air", font=resize.font)
label1.grid(sticky='nsew')


tk.Button(Main_Menu, text='Second', command=Second.tkraise).grid()
tk.Button(Second, text='Menu', command=Main_Menu.tkraise).grid()

window.bind('<Configure>', resize)
window.mainloop()