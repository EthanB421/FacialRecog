import cv2
import pyfirmata
import time
import threading

#Facial code setup

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#readInput
cap = cv2.VideoCapture(1)


#ARDUINO setup

board = pyfirmata.Arduino('COM5')

spin = 0

#defining pinnout pins
#motor1:
a1 = 5
a2 = 6

#motor2:
b1 = 9
b2 = 10

def spinnerCycle():
    while True:
        time.sleep(0.03)
        if spin == 0:
            #stay still
            spin_and_wait(0, 0, 100)
        elif spin == 1:
            #camera left
            spin_and_wait(-255, -255, 20)
            spin_and_wait(0, 0, 100)
        elif spin == -1:
            #camera right
            spin_and_wait(255, 255, 20)
            spin_and_wait(0, 0, 100)
        elif spin == 2:
            #no face
            #spin_and_wait(255, 255, 80)
            spin_and_wait(0, 0, 100)


def set_motor_pwm(pwm, pin1, pin2):
    if pwm < 0:
        #do analog
        board.digital[pin1].write(-pwm/255)
        board.digital[pin2].write(0)
    else:
        board.digital[pin1].write(0)
        board.digital[pin2].write(pwm/255)


def set_motor_current(PWMA, PWMB):
      set_motor_pwm(PWMA, a1, a2)
      set_motor_pwm(PWMB, b1, b2)

def spin_and_wait(PWMA, PWMB, duration):
      set_motor_current(PWMA, PWMB)
      time.sleep(duration/1000)

sThread = threading.Thread(target=spinnerCycle, args=[])
sThread.start()

#facial detection truth loop
switch = True
while (switch):
    check, img = cap.read()

#convert to greyscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

# Draw bounding box around the faces
    maxx = 0
    maxy = 0
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        if x > maxx:
            maxx = x

        if y > maxy:
            maxy = y
    if maxx > 0:
        if maxx < 180:
            print("left")
            spin = -1
        elif maxx > 320:
            print("right")
            spin = 1
        else:
            spin = 0
            print("nil")
    else:
        print("not here")
        spin = 2

    cv2.imshow('img', img)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()