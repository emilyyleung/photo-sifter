import tkinter as tk
from os import listdir, rename, scandir
from os.path import isfile, join, isdir, splitext

from PIL import Image, ImageTk

class PhotoSifter:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Sifter")

        self.path = './photos/'
        self.skip_folder = self.path + 'skip/'
        self.upload_folder = self.path + 'upload/'

        file_extensions = ['.png', '.jpeg', '.jpg']

        # START CHECKS ################################################################

        if isdir(self.path) == False or isdir(self.skip_folder) == False or isdir(self.upload_folder) == False:
            print("Please provide the following folders: /photos, /photos/skip, /photos/upload")
            exit()
        
        self.total = 0

        for path in scandir(self.path):
            if path.is_file():
                file_name, file_extension = splitext(path)
                if file_extension in file_extensions:
                    self.total += 1

        if self.total == 0:
            print("No images provided")
            exit()

        # FINISH CHECKS ################################################################

        if self.total > 0:
            self.images = [f for f in listdir(self.path) if isfile(join(self.path, f))]
            
            self.count = 0

            self.image_load = Image.open(self.path + self.images[self.count])

            self.image_resized = self.resize_image()
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
        else:
            print("NO IMAGES AVAILABLE")
    
    def reload_images(self):
        self.images = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        print(self.images, self.count)
        if self.count != 0:
            self.count -= 1

        if len(self.images) == 0:
            self.label.config(image='')
        elif len(self.images) == 1:
            self.load_image(self.images[0])
        else:
            self.load_image(self.images[self.count])
    
    def resize_image(self):
        raw_image_width = self.image_load.width
        raw_image_height = self.image_load.height

        if raw_image_width > raw_image_height:
            image_width = 1000
            image_height = int(( raw_image_height/raw_image_width ) * 1000)
            return self.image_load.resize((image_width, image_height))
        else:
            image_height = 1000
            image_width = int(( raw_image_width/raw_image_height ) * 1000)
            return self.image_load.resize((image_width, image_height))

    def load_image(self, image_path):
        self.image_load = Image.open(self.path + image_path)
        self.image_resized = self.resize_image()
        self.image = ImageTk.PhotoImage(self.image_resized)
        self.label.config(image=self.image)
        self.label.pack()

    def press_right(self, action):
        if len(self.images) == 0:
            print("RIGHT")
        else:
            current_image = self.images[self.count]
            current_file = self.path + current_image
            move_file = self.upload_folder + current_image
            rename(current_file, move_file)
            self.reload_images()

    def press_left(self, action):
        if len(self.images) == 0:
            print("LEFT")
        else:
            current_image = self.images[self.count]
            current_file = self.path + current_image
            move_file = self.skip_folder + current_image
            rename(current_file, move_file)
            self.reload_images()

    def press_up(self, action):
        if (self.count == 0):
            print("START")
        else:
            self.count -= 1
            print(self.count)
            new_image = self.images[self.count]
            self.load_image(new_image)

    def press_down(self, action):
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