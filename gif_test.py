import tkinter as tk
from PIL import Image, ImageTk
import os

cro_gif_path = "images/cro.gif"
text_file_path = "lib/cro.txt"

def play_gif(gif_path):
    gif = Image.open(gif_path)
    gif.seek(0)
    gif_frames = [ImageTk.PhotoImage(gif.copy())]
    
    for i in range(1, gif.n_frames):
        gif.seek(i)
        gif_frames.append(ImageTk.PhotoImage(gif.copy()))

    gif_label = tk.Label(root, image=gif_frames[0])
    gif_label.place(relx=0.5, rely=0.8, anchor='center')
    gif_label.gif_frames = gif_frames
    gif_label.gif_index = 0
    gif_label.gif_animation = gif_label.after(100, update_gif, gif_label)

def update_gif(gif_label):
    gif_label.gif_index += 1
    gif_label.config(image=gif_label.gif_frames[gif_label.gif_index % len(gif_label.gif_frames)])
    gif_label.gif_animation = gif_label.after(100, update_gif, gif_label)

root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(bg = "#F0F8FF")
# root.geometry("{}x{}".format(root.winfo_screenwidth(), root.winfo_screenheight()))
# root.overrideredirect(1)

# Read text from file and wrap it to window size
with open(text_file_path, 'r') as f:
    text = f.read()

# text_label = tk.Label(root, text=text, wraplength=root.winfo_screenwidth(), bg='#F0F8FF')
# text_label = tk.Label(root, text=text, bg='#F0F8FF')
# text_label.pack()

text_widget = tk.Text(root, wrap='word', bg='#F0F8FF', padx=20, pady=20, highlightthickness=0)
text_widget.insert('1.0', text)
text_widget.configure(state='disabled', font=("Arial", 20, "bold"))
text_widget.place(relx=0.5, rely=0.5, anchor='center')

# Play gif at center bottom of the window
play_gif(cro_gif_path)

root.mainloop()