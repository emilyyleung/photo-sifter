import tkinter as tk
from os import listdir
from os.path import isfile, join

from PIL import Image, ImageTk

class PhotoSifter:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Sifter")

        self.path = './photos'
        self.images = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        
        self.count = 0

        self.image_load = Image.open('./photos/' + self.images[self.count])
        self.image_resized = self.image_load.resize((300, 300))
        self.image = ImageTk.PhotoImage(self.image_resized)

        self.label = tk.Label(image=self.image)
        self.label.image = self.image
        self.label.pack()

        # Bind arrow key events to actions
        self.root.bind("<Right>", self.press_right)
        self.root.bind("<Left>", self.press_left)
        self.root.bind("<Up>", self.press_up)
        self.root.bind("<Down>", self.press_down)

        self.root.focus_set()

    def load_image(self, image_path):
        self.image_load = Image.open('./photos/' + image_path)
        self.image_resized = self.image_load.resize((300, 300))
        self.image = ImageTk.PhotoImage(self.image_resized)
        self.label.config(image=self.image)
        self.label.pack()

    def press_right(self, action):
        print("RIGHT")

    def press_left(self, action):
        print("LEFT")

    def press_up(self, action):
        print("UP")

    def press_down(self, action):
        print("DOWN")
        print(self.count, len(self.images))
        if self.count == len(self.images) - 1:
            print("FINISHED")
        else:
            self.count += 1
            print(self.count)
            new_image = self.images[self.count]
            print(new_image)
            self.load_image(new_image)

if __name__ == '__main__':
    root = tk.Tk()
    PhotoSifter(root)
    root.mainloop()