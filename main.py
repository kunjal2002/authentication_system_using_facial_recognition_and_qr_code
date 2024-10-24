# from code import ap_main
# from code import qr_main
from code import *
from tkinter import *

# import tkMessageBox

top = tkinter.Tk()
top.geometry('1000x1000')
canvas = Canvas(top, width = 800, height = 399)
canvas.pack()
img = PhotoImage(file="blog_image.png")
canvas.create_image(20, 20, anchor=NW, image=img)

l = Label(top, text="Authentication System using Facial Recognition and QR Code", font=("Arial", 21))
l.pack(side='top', padx=80, pady=10)
B1 = tkinter.Button(top, text="SCAN Face..", command=ap_main, height=5, width=30)
B2 = tkinter.Button(top, text="Scan QR..", command=qr_main,  height=5, width=30)
B1.pack(side='left', padx=100, pady=10)
B2.pack(side='right', padx=150, pady=20)
top.mainloop()




