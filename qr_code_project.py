import cv2
import numpy as np
from pyzbar.pyzbar import decode

import sys
import os
import tkinter

#from test1 import AttendanceProject as ap


# import tkMessageBox
top = tkinter.Tk()
top.geometry('300x200')

# fr=tkinter.Tk()
# fr.geometry('4')


def func1():
    os.system('qr_bar_test.py')


def func2():
    path = os.path.dirname(os.path.realpath(__file__)) + '\ImagesAttendance'
    print(f'in module {path}')
    print(f'in module {os.path.realpath(__file__)}')

    os.system('/pycharm_workspace/qr_code_detector/test1/AttendanceProject.py')


B1 = tkinter.Button(top, text="Scan..", command=func1)
B2 = tkinter.Button(top, text="SCAN..", command=func2)
B1.pack(side='right')
B2.pack(side='left')
top.mainloop()

# img = cv2.imread('1.png')
cap = cv2.VideoCapture(0)  # for web cam image capture
# set the width and height
cap.set(3, 640)  # id for width is 3
cap.set(4, 480)  # id for height is 4
# code = decode(img)
# print(code)

with open('myDataFile.text') as f:
    myDataList = f.read().splitlines()
print(myDataList)

while True:

    success, img = cap.read()
    for barcode in decode(img):
        print(barcode.data)
        # print(barcode.rect) # this will tell us the position
        myData = barcode.data.decode('utf-8')
        print(myData)

        if myData in myDataList:
            myOutput = 'Authorized'
            myColor = (0, 255, 0)
        else:
            myOutput = 'Un-Authorized'
            myColor = (0, 0, 255)

        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, myColor, 2)
        pts2 = barcode.rect
        cv2.putText(img, myOutput, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, myColor, 2)

    cv2.imshow('Result', img)
    cv2.waitKey(1)
