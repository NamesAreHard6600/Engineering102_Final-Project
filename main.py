from tkinter import *
from PIL import ImageTk, Image, ImageDraw
import colorsys

import random


#THE BOXES COULD JUST BE THE CLICKABLE THINGS AND THEN I USE THE FILL TOOL ON THE MAP ITSELF
#THAT SHOULD BE FLEXIBLE TOO THOUGH SO THAT SHOULD BE DONE WITH A PYTHON TOOL

def create_dict():
    with open("states.txt", 'r') as f:
        arr = [x.strip().split() for x in f.readlines()]
    return {x[0]: [float(y) for y in x[1:]] for x in arr}

class HeatMap:
    def __init__(self):
        self.win = Tk()
        self.win.geometry("1324x816")
        self.canvas = Canvas(self.win, width=1224, height=816)
        self.canvas.place(x = 0,y = 0)
        
        self.states = create_dict()

        self.bg = Image.open("US.png")
        self.bg = self.bg.convert("RGB")
        self.fill_image()
        self.bg = ImageTk.PhotoImage(self.bg)
        self.image_id = self.canvas.create_image(1224/2,816/2, image=self.bg)
        #self.bg.show()
        
        self.setup_rectangles()
    
    def fill_image(self):
        for state, coords in self.states.items():
            seed = (coords[0],coords[1])
            color = tuple(int(x*255) for x in list(colorsys.hsv_to_rgb(.33-((coords[2]-20.75)/24.53571/3),1,1)))
            print(color)
            ImageDraw.floodfill(self.bg, seed, color, thresh=90)
            
    
    def setup_rectangles(self):
        for state, coords in self.states.items():
            if len(coords) == 0:
                print(f"{state} not processed yet")
            else:
                self.canvas.create_rectangle(coords[0],coords[1],coords[0]+10,coords[1]+10, fill="white")
    
    def main(self):
        
        self.win.mainloop()


heatmap = HeatMap()
heatmap.main()




