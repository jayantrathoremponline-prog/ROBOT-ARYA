import tkinter as tk
from PIL import Image, ImageTk

mit_image_path = "/home/humanoid/Main/images/mit.png"
robotronix_image_path = "/home/humanoid/Main/images/robo.png"
cro_gif_path = "images/cro.gif"

def main():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(bg = "#F0F8FF")

    mit_image_label = tk.Label(root, bg = "#F0F8FF")
    mit_image = Image.open(mit_image_path)
    image_width, image_height = mit_image.size

    if image_width > image_height:
        ratio = image_width / image_height
        new_height = int(image_height * 0.7)
        new_width = int(new_height * ratio)
    else:
        ratio = image_height / image_width
        new_width = int(image_width * 0.7)
        new_height = int(new_width * ratio)

    mit_image = mit_image.resize((new_width, new_height), Image.ANTIALIAS)
    mit_photo_image = ImageTk.PhotoImage(mit_image)
    mit_image_label.config(image=mit_photo_image)
    mit_image_label.place(relx=0.5, rely=0.5, anchor='center')

    robotronix_image_label = tk.Label(root, bg = "#F0F8FF")
    robotronix_image = Image.open(robotronix_image_path)
    image_width, image_height = robotronix_image.size

    if image_width > image_height:
        ratio = image_width / image_height
        new_height = int(image_height * 0.8)
        new_width = int(new_height * ratio)
    else:
        ratio = image_height / image_width
        new_width = int(image_width * 0.8)
        new_height = int(new_width * ratio)

    robotronix_image = robotronix_image.resize((new_width, new_height), Image.ANTIALIAS)
    robotronix_photo_image = ImageTk.PhotoImage(robotronix_image)
    robotronix_image_label.config(image=robotronix_photo_image)
    robotronix_image_label.place(relx=1, rely=1, x=-5, y=-5, anchor='se')
    
    text_label = tk.Label(root, text="Developed By EC Group of MIT &:", font=("Helvetica", 14, "bold", "italic"), bg = "#F0F8FF")
    text_label.place(relx=0.965, rely=0.88, anchor=tk.SE)
    # text_label.place(relx=0, rely=1, anchor="sw", x=10, y=-10)

    root.mainloop()

if __name__ == "__main__":
    main()