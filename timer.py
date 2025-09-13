from tkinter import *
from PIL import ImageTk, Image
from threading import Thread
import os
from itertools import count
from playsound import playsound


BASE_DIR = os.path.dirname(__file__)
gif_path = os.path.join(BASE_DIR, "gifgit.gif")
sound_path = os.path.join(BASE_DIR, "ticktock.wav")

root = Tk()
root.geometry('400x500')
root.configure(bg='#72A0C1')
root.title("Fitness Timer")

is_paused = False
current_time = 0
countdown_id = None

try:
    RESAMPLE_MODE = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLE_MODE = Image.ANTIALIAS  



class ImageLabel(Label):
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)

      
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                frame = im.copy().resize((200, 200), RESAMPLE_MODE)
                self.frames.append(ImageTk.PhotoImage(frame))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc = (self.loc + 1) % len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


def reset_to_home():
    global countdown_id
    if countdown_id:
        root.after_cancel(countdown_id) 
    for widget in root.winfo_children():
        widget.destroy()
    build_home_screen()



def toggle_pause():
    global is_paused
    is_paused = not is_paused
    if is_paused:
        pause_button.config(text="Resume")
    else:
        pause_button.config(text="Pause")
        countdown(current_time) 



def get_value():
    global current_time, time_output, time_counter2, pause_button, cancel_button

    user_input = time_value.get().strip()

   
    if not user_input.isdigit():
        error_label = Label(root, text="⚠ Please enter a valid number!",
                            font=('opensans', 11), bg='#72A0C1', fg='red')
        error_label.place(relx=0.5, y=360, anchor="center")
        root.after(2000, error_label.destroy) 
        return

   
    current_time = int(user_input)

    input_time.place_forget()
    time_value.place_forget()
    start_Button.place_forget()

   
    minutes, seconds = divmod(current_time, 60)
    time_counter2 = Label(root,
                          text=f'Your timer is set for {minutes} minutes and {seconds} seconds',
                          font=('opensans', 11), bg='#72A0C1')
    time_counter2.place(relx=0.5, y=330, anchor="center")

    time_output = Label(root, font=('opensans', 16), bg='#72A0C1')
    time_output.place(relx=0.5, y=370, anchor="center")

  
    pause_button = Button(root, text="Pause", command=toggle_pause,
                          padx=20, pady=10, bg='#FFD580')
    pause_button.place(relx=0.3, y=420, anchor="center")

    cancel_button = Button(root, text="Cancel", command=reset_to_home,
                           padx=20, pady=10, bg='#FF6961')
    cancel_button.place(relx=0.7, y=420, anchor="center")

    countdown(current_time)



def countdown(t):
    global current_time, countdown_id
    current_time = t

    if is_paused:
        return 

    mins, secs = divmod(t, 60)
    time_str = f"{mins}:{secs:02d}"
    time_output.config(text=time_str)

    if t > 0:
        countdown_id = root.after(1000, countdown, t - 1)
    else:
       
        time_counter2.destroy()
        time_output.config(text="⏰ Time is up!", font=('opensans', 16, 'bold'),
                           bg='#7CB9E8')

   
        Thread(target=lambda: playsound(sound_path)).start()

      
        pause_button.destroy()
        cancel_button.destroy()
        go_back_button = Button(root, text='Go Back', command=reset_to_home,
                                padx=25, pady=15, bg='#7CB9E8')
        go_back_button.place(relx=0.5, y=450, anchor="center")


def build_home_screen():
    global input_time, time_value, start_Button, lbl

  
    lbl = ImageLabel(root)
    lbl.place(relx=0.5, y=120, anchor="center")
    lbl.load(gif_path)

  
    input_time = Label(root, text="Enter a number of seconds to countdown :",
                       font=('opensans', 12), bg='#72A0C1')
    input_time.place(relx=0.5, y=250, anchor="center")

   
    time_value = Entry(root, width=35, borderwidth=4)
    time_value.place(relx=0.5, y=285, anchor="center") 


    start_Button = Button(root, text='Start', command=get_value,
                          padx=25, pady=15, bg='#7CB9E8')
    start_Button.place(relx=0.5, y=345, anchor="center")


build_home_screen()
root.mainloop()
