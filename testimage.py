from tkinter import *
from PIL import Image


n = 10
image1 = Image.open('IconsAndImages/Buttonnext.gif')
image1.resize((n,n))
image1.save('IconsAndImages/butontestnext.gif')

# file='IconsAndImages/Buttonnext.gif'
# photo = PhotoImage(image1)

"""
root = Tk()
button1 = Button(root, image=photo)
button1.pack()

Label(root, text="toto").pack()

root.mainloop()
"""
