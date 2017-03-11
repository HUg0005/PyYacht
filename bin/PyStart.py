import datetime
import threading
import time
from tkinter import *


# Classes for data transfer between threads
class TimeCapture(object):
    __slots__ = ("data",)


class AddTimeCapture(object):
    __slots__ = ("data",)


class StopThread(object):
    __slots__ = ("state",)


# Main timer
def timer(hour, minute, second):
    while threadstop.state == 0:
        try:
            th = time.localtime().tm_hour
            tm = time.localtime().tm_min
            ts = time.localtime().tm_sec
            dtcurrent = datetime.datetime(year=1, month=1, day=1, hour=th, minute=tm, second=ts)
            dtstart = datetime.datetime(year=1, month=1, day=1, hour=hour, minute=minute,
                                        second=second) + datetime.timedelta(minutes=atime.data)
            diff = dtstart - dtcurrent
            t = diff.total_seconds()
            stime.data = t
            m, s = divmod(int(t), 60)
            timeformat = '{:02d}:{:02d}'.format(m, s)
            outputlabel["text"] = timeformat

            # Colour
            if ((m != 3 and m != 2 and m < 6) or s == 0) and (s == 20 or s == 30 or s <= 10) and sixmin.get() == 0:
                timeflag["fg"] = "red"
                tolabel["fg"] = "red"
                flaglabel["fg"] = "red"
            elif ((m != 3 and m != 2 and m < 6) or s == 0) and (s == 20 or s == 30 or s <= 10) and sixmin.get() == 1:
                timeflag["fg"] = "red"
                tolabel["fg"] = "red"
                flaglabel["fg"] = "red"
            elif timeflag["fg"] != "black":
                timeflag["fg"] = "black"
                tolabel["fg"] = "black"
                flaglabel["fg"] = "black"
            if t < -1:
                error()
                break
            time.sleep(0.1)
        except:
            error()
            break


# Flag management and countdown
def flags():
    while threadstop.state == 0:
        t = stime.data
        if t >= 360 and sixmin.get() == 1:
            m, s = divmod(int(t - 360), 60)
            ttapd = '{:02d}:{:02d}'.format(m, s)
            timeflag["text"] = ttapd
            flaglabel["text"] = "AP or Recall Down"

        elif t >= 300 and sixmin.get() == 0:
            m, s = divmod(int(t - 300), 60)
            ttc = '{:02d}:{:02d}'.format(m, s)
            timeflag["text"] = ttc
            flaglabel["text"] = "Class Up"

        elif 360 > t >= 300 and sixmin.get() == 1:
            m, s = divmod(int(t - 300), 60)
            ttca = '{:02d}:{:02d}'.format(m, s)
            timeflag["text"] = ttca
            flaglabel["text"] = "Class Up"

        elif 300 > t >= 240:
            m, s = divmod(int(t - 240), 60)
            ttw = '{:02d}:{:02d}'.format(m, s)
            timeflag["text"] = ttw
            flaglabel["text"] = "Warning Up"

        elif 240 > t >= 60:
            m, s = divmod(int(t - 60), 60)
            ttwd = '{:02d}:{:02d}'.format(m, s)
            timeflag["text"] = ttwd
            flaglabel["text"] = "Warning Down"

        elif 60 >= t > 0:
            m, s = divmod(int(t), 60)
            ttcd = '{:02d}:{:02d}'.format(m, s)
            timeflag["text"] = ttcd
            flaglabel["text"] = "Start"

        elif t == 0 and onemin.get() == 0:
            atime.data += 5
            timelist.insert(END, currenttimelabel["text"])

        elif t == 0 and onemin.get() == 1:
            atime.data += 6
            timelist.insert(END, currenttimelabel["text"])

        time.sleep(0.1)


def start():
    try:
        threadstop.state = 0
        threading._start_new_thread(timer, (int(h.get()), int(m.get()), int(s.get())))
        threading._start_new_thread(flags, ())
    except:
        error()


def stop():
    threadstop.state = 1


def clear():
    timeflag["text"] = "00:00"
    flaglabel["text"] = "NONE"
    outputlabel["text"] = "00:00"
    timeflag["fg"] = "black"
    tolabel["fg"] = "black"
    flaglabel["fg"] = "black"
    timelist.delete(0, END)
    atime.data = 0


def close():
    threadstop.state = 1
    root.destroy()


root = Tk()
root.wm_title("Race Start Timer")


def error():
    threadstop.state = 1
    errormsg = Toplevel()
    errormsg.title("ERROR")
    fataltext = Message(errormsg, text="ERROR:", font=(None, 10))
    fataltext.pack()
    errortext = Message(errormsg,
                        text="Have you entered the correct start time? Accepted time format is HH:MM:SS 24 hour time.")
    errortext.pack()
    errorbutton = Button(errormsg, text="Dismiss", command=errormsg.destroy)
    errorbutton.pack()


def currenttime():
    while True:
        th = time.localtime().tm_hour
        tm = time.localtime().tm_min
        ts = time.localtime().tm_sec
        currenttimelabel["text"] = '{:02d}:{:02d}:{:02d}'.format(th, tm, ts)
        time.sleep(0.1)


h = IntVar()
m = IntVar()
s = IntVar()
sixmin = IntVar()
onemin = IntVar()

# Used to transfer seconds to start to  flags()
stime = TimeCapture()
stime.data = 0

# Used to add time to start time
atime = AddTimeCapture()
atime.data = 0

threadstop = StopThread()
threadstop.state = 1

# GUI

# Make window maximised
width, hight = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (width, hight))

timeframe = Frame()
timeframe.pack(side=RIGHT, expand=YES)
entryframe = Frame()
entryframe.pack(side=TOP)
checkframe = Frame()
checkframe.pack()

# root.configure(background="beige")

hourlabel = Label(entryframe, text="First start time:", anchor=E)
hourlabel.pack(side=LEFT)
hourentry = Entry(entryframe, width=2, textvariable=h)
hourentry.pack(side=LEFT)
minuteentry = Entry(entryframe, width=2, textvariable=m)
minuteentry.pack(side=LEFT)
secondentry = Entry(entryframe, width=2, textvariable=s)
secondentry.pack(side=LEFT)

timertypecheckbox = Checkbutton(checkframe, text="6min start", variable=sixmin)
timertypecheckbox.pack()
mingapcheckbox = Checkbutton(checkframe, text="1min gap between starts", variable=onemin)
mingapcheckbox.pack()
timelabel = Label(checkframe, text="Race start times:")
timelabel.pack()
timelist = Listbox(root)
timelist.pack(fill=Y, expand=YES, side=TOP)

currenttimetext = Label(timeframe, text="Current Time:", font=(None, 20))
currenttimetext.pack(side=TOP)
currenttimelabel = Label(timeframe, text="00:00:00", font=(None, 90))
currenttimelabel.pack(side=TOP)
timerlabel = Label(timeframe, text="Timer:", font=(None, 40))
timerlabel.pack(side=TOP)
outputlabel = Label(timeframe, text="00:00", font=(None, 160))
outputlabel.pack(side=TOP)
timeflag = Label(timeframe, text="00:00", font=(None, 70))
timeflag.pack(side=LEFT)
tolabel = Label(timeframe, text="to", font=(None, 20))
tolabel.pack(side=LEFT)
flaglabel = Label(timeframe, text="NONE", font=(None, 70))
flaglabel.pack(side=LEFT)

startbutton = Button(root, text="Start Timer", command=start)
startbutton.pack(side=LEFT)
stopbutton = Button(root, text="Stop Timer", command=stop)
stopbutton.pack(side=LEFT)
clearbutton = Button(root, text="Clear Timer", command=clear)
clearbutton.pack(side=LEFT)
closebutton = Button(root, text="Close", command=close)
closebutton.pack(side=LEFT)

threading._start_new_thread(currenttime, ())
root.mainloop()
