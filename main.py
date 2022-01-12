# File: main.py
# Author: Jarkko Heinonen
# Description: Header and footer elements and starting the GUI
import os
from tkinter import *
from artist import *
from pygame import mixer
import time

#Clicktrack functionality-----------------------------
mixer.init()
mixer.music.load("GUI\Click.mp3") # Sound not working
clicktrack_is_on = False
def stopct(): # Stop clicktrack
    global clicktrack_is_on
    if type(getselected()) == Song:
        if getselected().at_bar: # If we are playing a song, this assures that
            getselected().at_bar -= 1 # no bars will be missed, if paused
    clicktrack_is_on = False
    ctstart.config(state=NORMAL)
def playctn(button): # play clicktrack
    global ctslider
    global clicktrack_is_on
    global CTI
    global half
    global halfv
    button.config(state=DISABLED) # disable the play button
    clicktrack_is_on = True
    halfv = half.get()
    def click(bol, n):
        global halfv
        #mixer.music.play()
        #mixer.music.play()
        if bol:
            CTI.config(bg = "grey") # This boolean based system changes color every
        else:
            CTI.config(bg="darkred") # time the counter goes up
        if n == 5: # we only count to 4
            n = 1
        CTI.config(text = str(n))
        if type(getselected())==Song and n==1: 
            if getselected().at_bar >= len(getselected().tabs): # stop the track when song ends
                stopct()
            getselected().next_bar() # here we actually play the song forward
            getselected().at_bar += 1
        if not clicktrack_is_on:
            return
        # halfv is used here to half the tempo if needed
        button.after(int((halfv+1)*60000/ctslider.get()), lambda: click(not bol, n+1))
    click(True, 1)
    

def changebpm(string): # Increase or decrease bpm
    if string == "plus":
        ctslider.set(ctslider.get()+1)
    if string == "minus":
        ctslider.set(ctslider.get()-1)

#define functions to load pages--------------------
def load_home_page():
    homepagebutton.config(state = DISABLED)
    prevbutton.config(state = DISABLED)
    resetgrid()
    for a in artists:
        a.button.grid(row = (a.id-1)%3, column = (a.id-1)//3)
    artistframe.grid(row = 1, column = 0,sticky = W)

def load_prev_page():
    resetgrid()
    if type(getselected()) == Artist:
        load_home_page()
    else:
        getselected().loadprevpage()

#define root and frames---------------------------
root = Tk()
root.title("MySick UI")
headerframe = Frame(root) #header background
hbuttonframe = Frame(root) #header buttons
midbg = Frame(root) #middle background
artistframe = Frame(root,bg = "grey") #middle buttons
footerframe = Frame(root) #footer background
footereles = Frame(root) #footer elements
half = IntVar() # these variables exist to half the tempo of clicktrack if needed
halfv = 0 # they are not with other clicktrack variables because the root has to be
# created before intvar()(?)

#Creating images----------------------------------
headerbg = PhotoImage(file = "GUI/headerbackground.png")
homepagebuttonbg = PhotoImage(file="GUI/homepagebutton.png")
prevbuttonbg = PhotoImage(file="GUI/prevbutton.png")
exitbuttonbg = PhotoImage(file="GUI/exitbutton.png")
bgimage = PhotoImage(file="GUI/background.png")
footerbg = PhotoImage(file="GUI/footerbackground.png")
plusimage = PhotoImage(file="GUI/plusbutton.png")
minusimage = PhotoImage(file="GUI/minusbutton.png")
playimage = PhotoImage(file="GUI/playbutton.png")
stopimage = PhotoImage(file="GUI/stopbutton.png")

#Creating buttons and slidebar--------------------
homepagebutton = Button(hbuttonframe, image = homepagebuttonbg,
                        bg = "grey",
                        command = load_home_page)
prevbutton = Button(hbuttonframe, image = prevbuttonbg,
                    bg = "grey", command = load_prev_page)
exitbutton = Button(hbuttonframe, image = exitbuttonbg,
                    bg = "grey",
                    command = root.destroy)
buttons = [homepagebutton, prevbutton]
ctslider = Scale(footereles, from_ = 30, to=170, orient = HORIZONTAL,
                 width = 50, length = 200, bg = "grey", bd = 0,
                 fg = "darkred", troughcolor = "darkred")
ctadd = Button(footereles, image = plusimage,
               bg = "grey", command = lambda: changebpm("plus"))
ctminus = Button(footereles, image = minusimage, bg = "grey",
                 command = lambda: changebpm("minus"))
ctstart = Button(footereles, image = playimage, bg = "grey",
                 command = lambda: playctn(ctstart))
ctstop = Button(footereles, image = stopimage, bg = "grey",
                command = stopct)
ct_magic_button = Checkbutton(footereles, variable = half, onvalue = 1, offvalue = 0)
CTI = Label(footereles, text = "1", bg="darkred", pady = 10, padx = 24,
            font=("Helvetica",32))

#Creating background labels------------------------
Label(headerframe, image = headerbg,bg="grey").grid(row = 0, column = 0)
Label(midbg, image = bgimage, bg="grey").grid(row = 0, column = 0)
Label(footerframe, image = footerbg,bg="grey").grid(row=0,column=0)

#Initialize artists based on the folder structure
for f in os.listdir():
    if ".py" in f:continue
    if f == "__pycache__":continue
    if f == "GUI":continue
    if ".wav" in f:continue
    a = Artist(f,artistframe,buttons)

#Griding things----------------------------
#header.grid
headerframe.grid(row = 0, column = 0)
homepagebutton.grid(row = 0, column = 1)
prevbutton.grid(row = 0, column = 2)
exitbutton.grid(row = 0, column = 3)
hbuttonframe.grid(row = 0, column = 0,sticky = E)
#footer.grid
footerframe.grid(row = 2, column = 0)
ctslider.grid(row = 0,column = 1)
ctadd.grid(row = 0,column = 2)
ctminus.grid(row = 0,column = 0)
ctstart.grid(row = 0, column = 3)
ctstop.grid(row = 0, column = 4)
CTI.grid(row = 0, column = 5)
ct_magic_button.grid(row = 0, column = 6)
footereles.grid(row = 2, column = 0)
#middle frame.grid
midbg.grid(row = 1, column = 0,columnspan = 5)
artistframe.grid(row = 1, column = 0,sticky = W)
#start by loading homepage
load_home_page()
root.mainloop()
