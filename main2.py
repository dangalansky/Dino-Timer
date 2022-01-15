from tkinter import *
import math
import pygame

# ---------------------------- CONSTANTS ------------------------------- #
BLUE = "#A5E9F2"
FONT_NAME = "Helvetica"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15
reps = 0
timer = None


# ---------------------------- SOUNDS ----------------------------------- #
def work_sound():
    pygame.mixer.music.load('dino work.mp3')
    pygame.mixer.music.play(loops=0)


def break_sound():
    pygame.mixer.music.load('dino break.mp3')
    pygame.mixer.music.play(loops=0)


def long_break_sound():
    pygame.mixer.music.load('dino long break.mp3')
    pygame.mixer.music.play(loops=0)


# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    global reps
    global timer
    window.after_cancel(timer)
    progress_marker.config(image=prog0_img)
    canvas.itemconfig(timer_text, text="00:00")
    work_label.config(image="")
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    global work_label
    reps += 1
    work_label.place(x=197, y=110)

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        long_break_sound()
        work_label.config(image=breaktime)
        count_down(long_break_sec)
    elif reps % 2 == 0:
        break_sound()
        work_label.config(image=breaktime)
        count_down(short_break_sec)
    else:
        work_label.config(image=work)
        work_sound()
        count_down(work_sec)


# ---------------------------- COUNTDOWN MECHANISM --------------------- #


def count_down(count):
    global timer
    count_min = math.floor(count / 60)
    count_sec = count % 60
    # to guarantee proper readout ex) 00:00 instead of 00:0 or 0:00
    if count_min < 10:
        count_min = f'0{count_min}'
    if count_sec < 10:
        count_sec = f'0{count_sec}'
    canvas.itemconfig(timer_text, text=f'{count_min}:{count_sec}')
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        global reps
        global progress_marker
        start_timer()
        if reps < 2:
            progress_marker.config(image=prog0_img)
        if reps == 2:
            progress_marker.config(image=prog1_img)
        elif reps == 4:
            progress_marker.config(image=prog2_img)
        elif reps == 6:
            progress_marker.config(image=prog3_img)
        elif reps == 8:
            progress_marker.config(image=prog4_img)
            reps = 0


# ---------------------------- UI SETUP ------------------------------- #
## screen
window = Tk()
window.title('Dino Timer!')
window.config(padx=20, pady=50, bg=BLUE)
window.geometry('465x441')
## sound
pygame.mixer.init()

# --------------------------- IMAGE FILES ---------------------------- #
title = PhotoImage(file='title.png')
work = PhotoImage(file='work.png')
breaktime = PhotoImage(file='break.png')
start = PhotoImage(file='start.png')
reset = PhotoImage(file='reset.png')
word_bubble = PhotoImage(file='word_bubble.png')
prog0_img = PhotoImage(file='progress_0.png')
prog1_img = PhotoImage(file='progress_1.png')
prog2_img = PhotoImage(file='progress_2.png')
prog3_img = PhotoImage(file='progress_3.png')
prog4_img = PhotoImage(file='progress_4.png')

# -------------------------- GUI ------------------------------------ #

# timer readout and canvas create_image functionality
canvas = Canvas(width=465, height=441, bg=BLUE, highlightthickness=0)
canvas.create_image(150, 200, image=word_bubble)
timer_text = canvas.create_text(230, 143, text="00:00", font=("arial", 15, 'bold'), fill='black')
canvas.place(x=0, y=0)

# Labels
title_label = Label(image=title, bg=BLUE)
title_label.place(x=90, y=-45)
work_label = Label(image=work, borderwidth=0, bg='white')
##work_label.place() located in functions above as needed
progress_marker = Label(image=prog0_img, borderwidth=0, bg=BLUE, highlightthickness=0)
progress_marker.place(x=5, y=315)

# Buttons
start_button = Button(image=start, bg=BLUE, borderwidth=0, highlightthickness=0,
                      command=start_timer)
start_button.place(x=295, y=225)

reset_button = Button(image=reset, bg=BLUE, borderwidth=0, highlightthickness=0, command=reset_timer)
reset_button.place(x=295, y=275)

# in-built loop that keeps CPU checking for user input
window.mainloop()
