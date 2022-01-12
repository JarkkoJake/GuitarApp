# File: artist.py
# Author: Jarkko Heinonen
# Description: Artist, album, song classes
import os
from tkinter import *

selected = "homepage" # this variable tracks the open page
artists = []
string_chars = ["A","B","C","D","E","F","G","b",
                "a","c","d","e","f","g"]
def select(sel):
    global selected
    selected = sel
def getselected():
    global selected
    return selected
def getnextid(lis):
    if len(lis) == 0:
        return 1
    return lis[-1].id + 1
def resetgrid(): #grid_forget() for everything
    for a in artists:
        a.resetgrid()

class Artist:

    def __init__(self, filename, root, buttons):
        self.id = getnextid(artists)
        self.name = filename
        self.root=root
        self.buttons = buttons
        artists.append(self)
        self.logo = PhotoImage(file=self.name+"/logo.png")
        self.albums = []
        self.loadalbums()
        self.button = Button(self.root,image = self.logo,
                             bg = "grey",
                             command = self.loadalbumpage)
    def select(self):
        select(self)
    def loadalbumpage(self):
        self.select()
        resetgrid()
        for al in self.albums:
            al.button.grid(row = (al.id-1)%4,column = (al.id-1)//4)
        self.buttons[0].config(state = NORMAL)
        self.buttons[1].config(state = NORMAL)
    def loadprevpage():
        pass

    def loadalbums(self): #load artists albums from the folder structure
        for f in os.listdir(self.name):
            if ".png" in f:
                continue
            a = Album(f,self)
            self.albums.append(a)
    def resetgrid(self):
        self.button.grid_forget()
        for a in self.albums:
            a.resetgrid()

class Album:
    
    def __init__(self, filename, artist):
        self.name = filename
        self.id = getnextid(artist.albums)
        self.songs = []
        self.artist = artist
        self.logo = PhotoImage(file = artist.name+"/"+self.name+"/logo.png")
        self.button = Button(self.artist.root,image = self.logo,
                             bg = "grey",command=self.load_song_page)
        self.loadsongs()
        self.albumpic = Label(self.artist.root, image = self.logo,
                              bg = "grey")
    def select(self):
        select(self)
    def loadsongs(self): #loading songs from the folder structure
        for f in os.listdir(self.artist.name+"/"+self.name):
            if ".png" in f:
                continue
            song = Song(f,self)
            self.songs.append(song)
    def load_song_page(self):
        self.select()
        for a in self.artist.albums:
            a.button.grid_forget()
        self.albumpic.grid(row = 0, column = 0, rowspan=2, columnspan = 2)
        for s in self.songs:
            s.tabsl.grid_forget()
            s.button.grid(row = s.id+1, column = 0, columnspan=2)
    def loadprevpage(self):
        self.albumpic.grid_forget()
        for s in self.songs:
            s.resetgrid()
        self.artist.loadalbumpage()
    def resetgrid(self):
        self.button.grid_forget()
        self.albumpic.grid_forget()
        for s in self.songs:
            s.resetgrid()

class Song:

    def __init__(self, filename, album):
        self.name = filename
        self.album = album
        self.id = getnextid(self.album.songs)
        self.tabs = []
        self.titles = []
        self.button = Button(self.album.artist.root,
                             width = 36,
                             text = self.name,
                             bg = "grey",
                             command = self.loadtabs)
        self.next_button = Button(self.album.artist.root, command = lambda: self.move_bar(1),
                             text = "-->", width = 17, bg = "grey")
        self.prev_button = Button(self.album.artist.root, command = lambda: self.move_bar(-1),
                             text = "<--", width = 17, bg = "grey")
        self.at_bar = 0
        self.tabsl = Label(self.album.artist.root, text = "no tabs")
        self.part_label = Label(self.album.artist.root, font = ("Courier New", 20),justify=LEFT, bg="grey", bd = 10)
        self.tab_label_1 = Label(self.album.artist.root, font= ("Courier New", 20),justify=LEFT, bg="grey", bd = 10)
        self.tab_label_2 = Label(self.album.artist.root, font= ("Courier New", 12),justify=LEFT, bg="grey", bd = 10)
        self.tab_label_3 = Label(self.album.artist.root, font= ("Courier New", 12),justify=LEFT, bg="grey", bd = 10)
    def resetgrid(self):
        self.button.config(fg = "black")
        self.button.grid_forget()
        self.tabsl.grid_forget()
        self.next_button.grid_forget()
        self.prev_button.grid_forget()
        self.part_label.grid_forget()
        self.tab_label_1.grid_forget()
        self.tab_label_2.grid_forget()
        self.tab_label_3.grid_forget()
    def loadtabs(self):
        if type(getselected()) == Song: # clear old tabs if they are still open
            getselected().tabsl.grid_forget()
            getselected().next_button.grid_forget()
            getselected().prev_button.grid_forget()
            getselected().part_label.grid_forget()
            getselected().tab_label_1.grid_forget()
            getselected().tab_label_2.grid_forget()
            getselected().tab_label_3.grid_forget()
        self.select()
        if self.tabs:
            self.display_tabs()
            return
        f = open(self.album.artist.name+"/"+self.album.name+"/"\
                     +"/"+self.name+"/"+self.name+".txt","r")
        ln = 0
        lines = f.read().split("\n")
        title = "title"
        for line in lines:
            if ln >= len(lines):
                break
            if lines[ln][0:3] == "---":
                title = lines[ln].strip("-")
                #self.tabs.append(title)
                ln += 1
                continue
            if lines[ln][0] in string_chars:
                bar = []
                for i in range(-1,7):
                    bar.append(lines[ln+i])
                self.tabs.append("\n".join(bar))
                self.titles.append(title)
                ln += 6
                continue
            else:
                ln += 1
        f.close()
        self.display_tabs()
    def display_tabs(self):
        self.at_bar = 0
        root = self.album.artist.root
        self.part_label.config(text=self.titles[0])
        self.tab_label_1.config(text=self.tabs[0])
        self.tab_label_2.config(text=self.tabs[1])
        self.tab_label_3.config(text=self.tabs[2])
        self.part_label.grid(row = 0, column = 2)
        self.tab_label_1.grid(row = 1, column = 2, rowspan=9)
        self.tab_label_2.grid(row = 10, column = 2, rowspan=6)
        self.tab_label_3.grid(row = 16, column = 2, rowspan=6)
        row = len(self.album.songs)+2
        self.next_button.grid(row = row, column = 1)
        self.prev_button.grid(row = row, column = 0)
    def move_bar(self, i):
        self.at_bar += i
        self.next_bar()
    def next_bar(self):
        i = self.at_bar
        self.part_label.config(text=self.titles[i])
        if i >= len(self.tabs):
            self.tab_label_1.config(text="----------------")
        else:
            self.tab_label_1.config(text=self.tabs[i])
        if i >= len(self.tabs)-1:
            self.tab_label_2.config(text="--------END--------")
        else:
            self.tab_label_2.config(text=self.tabs[i+1])
        if i >= len(self.tabs)-2:
            self.tab_label_3.config(text="--------END--------")
        else:
            self.tab_label_3.config(text=self.tabs[i+2])
    def select(self):
        for s in self.album.songs:
            s.button.config(fg="black")
        self.button.config(fg = "darkred")
        select(self)
    def loadprevpage(self):
        self.resetgrid()
        self.album.load_song_page()
        
        
