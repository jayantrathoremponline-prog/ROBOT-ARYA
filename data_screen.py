import tkinter as tk
from PIL import Image, ImageTk

cro_gif_path = "images/analog multimeter.png"
cro_file_path = "lib/analog multimeter.txt"

def play_gif(img_path):
    global new_width, new_height

    image = Image.open(img_path)

    image_width, image_height = image.size

    if image_width > image_height:
        ratio = image_width / image_height
        new_height = int(image_height * 0.7)
        new_width = int(new_height * ratio)
    else:
        ratio = image_height / image_width
        new_width = int(image_width * 0.7)
        new_height = int(new_width * ratio)
        
    img_type = image.format
    # print(img_type)

    if img_type == "GIF":
        image.seek(0)
        new_img = image.resize((new_width, new_height), Image.ANTIALIAS)
        gif_frames = [ImageTk.PhotoImage(new_img.copy())]

        for i in range(1, image.n_frames):
            image.seek(i)
            gif_frames.append(ImageTk.PhotoImage(image.copy()))

        gif_label = tk.Label(root, image=gif_frames[0], bg='#F0F8FF')
        gif_label.place(relx=0.5, rely=0.7, anchor='center')
        gif_label.gif_frames = gif_frames
        gif_label.gif_index = 0
        gif_label.gif_animation = gif_label.after(100, update_gif, gif_label)
    
    elif img_type != "GIF":
        new_img = image.resize((new_width, new_height), Image.ANTIALIAS)
        new_img = ImageTk.PhotoImage(new_img)

        img_label = tk.Label(root, image=new_img, bg='#F0F8FF')
        img_label.place(relx=0.5, rely=0.990, anchor='s')
        root.image = new_img

def update_gif(gif_label):
    gif_label.gif_index += 1
    gif_label.config(image=gif_label.gif_frames[gif_label.gif_index % len(gif_label.gif_frames)])
    gif_label.gif_animation = gif_label.after(100, update_gif, gif_label)

def data_window(text_file_path, img_path = None):
    global root, screen_height, screen_width
    root = tk.Tk()
    root.config(bg="#F0F8FF")
    root.attributes("-fullscreen", True)

    try:
        with open(text_file_path, "r") as f:
            text_data = f.read()
    except:
        text_data = text_file_path

    screen_height = root.winfo_screenheight()
    screen_width = root.winfo_screenwidth()
    text_height = int(screen_height * 0.9)
    text_width = int(screen_width * 0.9)
    font_size = int((screen_height + screen_width) / 97)

    text = tk.Text(root, bg="#F0F8FF", font=("Helvetica", font_size), wrap=tk.WORD, spacing1=1,pady=20, bd=0, highlightthickness=0)
    # text = tk.Text(root, bg="#F0F8FF", font=("Helvetica", font_size, "bold"), wrap=tk.WORD, spacing1=1, pady=20)
    text.config(state="normal")
    text.insert(tk.END, text_data)
    text.tag_configure("justified", justify='center')
    text.tag_add("justified", "1.0", "end")
    text.config(state="disabled")
    text.place(relx=0.5, rely=0.5, anchor="center", height=text_height, width=text_width)

    if img_path != None:
        play_gif(img_path)

    root.mainloop()

if __name__ == "__main__":
    data_window(text_file_path = cro_file_path, img_path = cro_gif_path)