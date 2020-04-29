from tkinter import ttk
from tkinter import filedialog
from tkinter import *
import tkinter as tk
from mutagen.mp3 import MP3
import pygame
import os

def main():

    def set_time():
        time = pygame.mixer.music.get_pos() / 1000
        l_time = song_length_list[song_n[0]]
        #formatted seconds variable
        seconds = round(float(time)) % 60
        #formatted minutes variable
        minutes = round((round(float(time)) - seconds) / 60)
        l_seconds = round(float(l_time)) % 60
        l_minutes  = round((round(float(l_time)) - l_seconds) / 60)
        #change text length label
        length_label['text'] = str(minutes) + ':' + str(seconds) + ' - ' + \
            str(l_minutes) + ':' + str(l_seconds)
        playlist.selection_clear(0, len(song_list))
        playlist.selection_set(song_n[0])
        app.after(500, set_time)

    def end():
        MUSIC_END = pygame.USEREVENT+1
        pygame.mixer.music.set_endevent(MUSIC_END)
        for event in pygame.event.get():
            if event.type == MUSIC_END:
                next()

        app.after(100, end)

    def Pause():
        if pause_btn['text'] == '⏯️':
            pause_btn['text'] = '⏸️'
            pygame.mixer.music.load(song_path_list[song_n[0]])
            label['text'], a = os.path.splitext(song_list[song_n[0]])
            pygame.mixer.music.play()
            set_time()
        elif pause_btn['text'] == '⏸️':
            pause_btn['text'] = '▶️'
            pygame.mixer.music.pause()
            playing = False
        elif pause_btn['text'] == '▶️':
            pause_btn['text'] = '⏸️'
            pygame.mixer.music.unpause()
            playing = True

    def next():
        if len(song_list) > song_n[0] + 1:
            pygame.mixer.music.load(song_path_list[song_n[0] + 1])
            song_n[0] += 1
            label['text'], a = os.path.splitext(song_list[song_n[0]])
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.load(song_path_list[0])
            song_n[0] = 0
            label['text'], a = os.path.splitext(song_list[song_n[0]])
            pygame.mixer.music.play()
        pause_btn['text'] = '⏸️'
        length_label['text'] = '0:00 - 0:00'

    def prev():
        if song_n[0] > 0:
            pygame.mixer.music.load(song_path_list[song_n[0] - 1])
            song_n[0] -= 1
            label['text'], a = os.path.splitext(song_list[song_n[0]])
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.load(song_path_list[len(song_list)-1])
            song_n[0] = (len(song_list)-1)
            label['text'], a = os.path.splitext(song_list[song_n[0]])
            pygame.mixer.music.play()
        pause_btn['text'] = '⏸️'
        length_label['text'] = '0:00 - 0:00'

    def set_volume(volume):
        #set volume
        pygame.mixer.music.set_volume(float(volume)/100)

    def choose_track(track):
        song_n[0] = playlist.curselection()[0]
        set_time()
        song_n[0] = playlist.curselection()[0]
        pause_btn['text'] = '⏸️'
        pygame.mixer.music.load(song_path_list[song_n[0]])
        label['text'], a = os.path.splitext(song_list[song_n[0]])
        pygame.mixer.music.play()

    def delete():
        song_n[0] -= 1
        song_list.pop(playlist.curselection()[0])
        song_length_list.pop(playlist.curselection()[0])
        song_path_list.pop(playlist.curselection()[0])
        pause_btn['text'] = '▶️'
        label['text'] = 'Song Name'
        length_label['text'] = '0:00 - 0:00'
        pygame.mixer.music.pause()
        playing = False
        pygame.mixer.music.load(song_path_list[song_n[0]])
        playlist['listvariable'] = StringVar(value = song_list)

    def add():
        file = filedialog.askopenfilename()
        head, tail = os.path.split(file)
        filename, fileextension = os.path.splitext(tail)
        if fileextension == '.mp3' or fileextension == '.ogg':
            song_path_list.append(file)
            song = MP3(file)
            song_length_list.append(song.info.length)
            song_list.append(tail)
        playlist['listvariable'] = StringVar(value = song_list)

    #song number in song_list
    song_n = [0]

    song_path_list = []
    song_list = []
    song_length_list = []

    #adding tracks from folder to track list
    for file in os.listdir('.'):
        filename, fileextension = os.path.splitext(file)
        if fileextension == '.mp3' or fileextension == '.ogg':
            song = MP3(file)
            song_path_list.append(file)
            song_length_list.append(song.info.length)
            song_list.append(file)

    #track name label
    label = Label(app, text='Song Name', background = '#1C2835', foreground = 'white')
    label.grid(row = 0, column = 4)

    #Previous track button
    prev_btn = Button(app, text = '⏮️', width = 20, command = prev, \
        background = '#17212B', highlightthickness = 0, \
        activebackground = '#222C36', foreground = 'white')
    prev_btn.grid(row=2, column=2)

    #pause track button
    pause_btn = Button(app, text = '⏯️', width=20, command = Pause, \
        background = '#17212B', highlightthickness = 0, \
        activebackground = '#222C36', foreground = 'white')
    pause_btn.grid(row=2, column = 4)
    pause_btn.bind('<Space>')

    #next track button
    next_btn = Button(app, text = '⏭️', width = 20, command = next, \
        background = '#17212B', highlightthickness = 0, \
        activebackground = '#222C36', foreground = 'white')
    next_btn.grid(row=2, column=6)

    #volume scale
    volume_scale = Scale(app, orient = VERTICAL, length = 200, from_ = 100.0, \
        to = 0.0, command = set_volume, background = '#1C2835', troughcolor='#17212B', \
        activebackground='#17212B', highlightthickness=0, foreground = 'white')
    volume_scale.grid(row = 0, column = 7)
    pygame.mixer.music.set_volume(0)

    #actual audio length position
    length_label = Label(app, text = '0:00 - 0:00', background = '#1C2835', \
        foreground = 'white')
    length_label.grid(row = 1, column = 4)

    song_playlist = StringVar(value = song_list)
    playlist = Listbox(app, listvariable = song_playlist, width = 40, \
        height = 20, background = '#1C2835', highlightthickness = 0, \
        selectforeground = 'black', selectbackground = '#17212B', foreground = 'white')
    playlist.grid(row = 0, column = 0)
    playlist.bind('<<ListboxSelect>>', choose_track)

    add_btn = Button(app, text = 'Add', width = 34, command = add, \
        background = '#17212B', highlightthickness = 0, \
        activebackground = '#222C36', foreground = 'white')
    add_btn.grid(row = 1, column = 0)

    delete_btn = Button(app, text = 'Delete', width = 34, command = delete, \
        background = '#17212B', highlightthickness = 0, \
        activebackground = '#222C36', foreground = 'white')
    delete_btn.grid(row = 2, column = 0)

    app.configure(background = '#1C2835')

    app.title('MP3 Player')
    img = Image('photo', file='icon2.png')
    app.tk.call('wm','iconphoto',app._w, img)

    end()

pygame.init()
app = Tk()
app.geometry('740x420')
main()
app.mainloop()
