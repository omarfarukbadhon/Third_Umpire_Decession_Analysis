
# Omar Faruk Badhon 
# Email: omarfarukbadhon@gmail.com



# import Library
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from functools import partial
import threading
import imutils
import time

# Video load 
stream = cv2.VideoCapture("run_out.mp4")
flag = True


# Speed control function of video
def play(speed):
    global flag
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)
    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width=set_width, height=set_height)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    if flag:
        canvas.create_text(132, 29, fill="green", font="Times 20 italic bold",
                           text="Decision Pending")
    flag = not flag


def pending(decision):
    frame = cv2.cvtColor(cv2.imread("decision_pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=set_width, height=set_height)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

    time.sleep(1.5)

    if decision == 'Out':
        decision_img = "out.png"
    else:
        decision_img = "not_out.png"
    frame = cv2.cvtColor(cv2.imread(decision_img), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=set_width, height=set_height)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)


def out():
    thread = threading.Thread(target=pending, args=("Out", ))
    thread.daemon = 1
    thread.start()
    
    
def not_out():
    thread = threading.Thread(target=pending, args=("Not Out",))
    thread.daemon = 1
    thread.start()
    

set_width = 650
set_height = 368

# Tkinter gui starts here
window = tkinter.Tk()
window.title("Third Umpire Decision")
cv_img = cv2.cvtColor(cv2.imread("ground.png"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=set_width, height=set_height)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image=photo)
canvas.pack()

# Buttons to control playback
btnPF = tkinter.Button(window, text="<< Previous(fast)", width=50,
                     command=partial(play, -25)).pack()

btnPS = tkinter.Button(window, text="<< Previous(slow)", width=50,
                     command=partial(play, -2)).pack()

btnNF = tkinter.Button(window, text="next(fast) >>", width=50,
                     command=partial(play, 25)).pack()

btnNS = tkinter.Button(window, text="Next(slow) >>", width=50,
                     command=partial(play, 2)).pack()

btnO = tkinter.Button(window, text="Give Out", width=50,
                     command=out).pack()

btnNO = tkinter.Button(window, text="Give Not Out", width=50,
                     command=not_out).pack()


window.mainloop()



