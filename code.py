# import sys
# sys.path.append('D:\sw\anaconda3\envs\pycharm_workspace\Lib\site-packages')

import cv2  # importing the packages and libraries
import numpy as np
import face_recognition
import os  # handy when processing files from other places in the system
from datetime import datetime

from pyzbar.pyzbar import decode
import sys
import tkinter


# convert images to rgb
# find encodings for images


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]  # get the first image only
        encodeList.append(encode)
    return encodeList


def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()  # read all the data in the file so that the one who is already arrived, we won't check
        nameList = []
        for line in myDataList:  # loop through each line in the file
            entry = line.split(',')
            nameList.append(
                entry[0])  # will append only the names(as index given is 0 and at 1 we have time) to the nameList
        if name not in nameList:
            now = datetime.now()  # give us the date and time
            dtString = now.strftime('%H :%M:%S')
            f.writelines(f'\n{name}, {dtString}')


def ap_main():
    # import the images
    # path = 'ImagesAttendance'
    images = []  # list of images
    classNames = []  # to get the names as well of images
    # print(f'in module {os.path.realpath(__file__)}')
    path = os.path.dirname(os.path.realpath(__file__)) + '\ImagesAttendance'
    print(f'in module {path}')

    myList = os.listdir(path)  # get the images from this folder

    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')  # read the current image
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)

    encodeListKnown = findEncodings(images)#contains the encoding of all the images of the dataset
    print('Encoding Complete')

    # to get an image and match it with our given images in folder
    cap = cv2.VideoCapture(0)  # to initialize webcam and get image from webcam

    while True:
        success, img = cap.read()  # this will give our image
        imgS = cv2.resize(img, (0, 0), None, 0.25,
                          0.25)  # to make our image small this will increase the speed of our process
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        # find matches
        # iterate through all the faces in our current webcam frame
        for encodeFace, faceLoc in zip(encodesCurFrame,
                                       facesCurFrame):  # we want both of them in same loop hence we use zip
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,
                                                     encodeFace)  # faceDis gives how close the two images are i.e., same or not
            # print(faceDis)
            matchIndex = np.argmin(faceDis)  # this is to print which image is closer and hence will have a lesser value
            # give index of the image which is closer to the one shown in webcam

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                # print(name)#print the name of image shown on webcam
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name)  # whenever we get a match, we will mark attendance

        cv2.imshow('Webcam', img)  # show the webcam image
        cv2.waitKey(1)


# -----------face recognition-------


def func1():
    # os.system('qr_bar_test.py')

    # img = cv2.imread('8.png')
    cap = cv2.VideoCapture(0)  # for web cam image capture
    # set the width and height
    cap.set(3, 640)  # id for width is 3
    cap.set(4, 480)  # id for height is 4
    # code = decode(img)
    # print(code)

    # for barcode in decode(img):
    #     print(barcode.data)

    while True:

        success, img = cap.read()
        for barcode in decode(img):
            print(barcode.data)
            # print(barcode.rect) # this will tell us the position
            myData = barcode.data.decode('utf-8')
            print(myData)
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (255, 0, 255), 5)
            pts2 = barcode.rect
            cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (255, 0, 255), 5)

        cv2.imshow('Result', img)
        cv2.waitKey(1)


def func2():
    path = os.path.dirname(os.path.realpath(__file__)) + '\ImagesAttendance'
    print(f'in module {path}')
    print(f'in module {os.path.realpath(__file__)}')

    os.system('/pycharm_workspace/qr_code_detector/test1/AttendanceProject.py')


def qr_main():
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
