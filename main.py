from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image, ImageDraw
from functools import partial
import colorsys

# DON'T FORGET REQUIREMENT.TXT
# ALIGN BOXES IN TOP CORNER
# MAKE RHODE ISLAND AND SUCH EXCEPTIONS

def create_dict():
    with open("states.txt", 'r') as f:
        arr = [x.strip().split() for x in f.readlines()]
    return {x[0]: [float(y) for y in x[1:]] for x in arr}

def create_info_dict():
    with open("states_info.txt", 'r') as f:
        arr = [x.strip().split("-") for x in f.readlines()]
    return {x[0]: x[1] for x in arr}

def decimal_range(start, stop, step):
    while start < stop: # and not math.isclose(start, stop): Py>3.5
        yield start
        start += step

class HeatMap:
    def __init__(self):
        self.win = Tk()
        self.win.geometry("1324x816")
        self.canvas = Canvas(self.win, width=1324, height=816)
        self.canvas.place(x=0, y=0)
        
        self.states = create_dict()
        self.states_info = create_info_dict()

        self.hawaii_cords = [(438, 693), (392, 675), (338, 657), (318, 661)]
        self.min_aqi = min([x[2] for x in self.states.values()])
        self.max_aqi = max([x[2] for x in self.states.values()])

        #Background and Image
        self.bg = Image.open("US.png")
        self.bg = self.bg.convert("RGB")
        self.fill_image()
        self.bg = ImageTk.PhotoImage(self.bg)
        self.image_id = self.canvas.create_image(1224/2, 816/2, image=self.bg)

        #INPUT
        self.input_label = Label(self.win, text="Desired AQI (or better):", bg="white")
        self.input_label.place(x=930,y=60)
        self.input_slider = Scale(self.win, from_=self.min_aqi-1, to_=self.max_aqi+1, orient=HORIZONTAL, command=self.update)
        self.input_slider.place(x=930, y=80)
        self.input_slider.set(self.max_aqi+1)
        # self.input_button = Button(self.win, text="Submit", command=self.update)
        # self.input_button.place(x=930, y=100)

        # Extras
        self.setup_buttons()
        self.create_gradient()

    def convert_aqi_to_color(self, aqi):
        rgb = colorsys.hsv_to_rgb(.5 - ((aqi - self.min_aqi) / (self.max_aqi-self.min_aqi) / 2), 1, 1)
        return tuple(int(x*255) for x in list(rgb))

    def fill_image(self):
        for state, coords in self.states.items():
            seed = (coords[0],coords[1])
            color = self.convert_aqi_to_color(coords[2])
            ImageDraw.floodfill(self.bg, seed, color, thresh=90)
            if state.lower() == "hawaii":
                for coord in self.hawaii_cords:
                    ImageDraw.floodfill(self.bg, coord, color, thresh=90)
            
    
    def setup_buttons(self):
        for state, coords in self.states.items():
            if len(coords) == 0:
                print(f"{state} not processed yet")
            else:
                button = Button(self.win, width=1, height=1, bg="green", command=partial(self.button_pressed, state))
                button.place(x=coords[0], y=coords[1])
                self.states[state].append(button)
                # self.canvas.create_rectangle(coords[0],coords[1],coords[0]+10,coords[1]+10, fill="white")

    def button_pressed(self, state):
        info = self.states_info.get(state,"STATE INFO UNAVALIABLE")
        info = f"Average AQI: {round(self.states[state][2],2)}\n" + "Why?: " + info
        messagebox.showinfo(state, info)

    def create_gradient(self):
        label_label = Label(self.win, text="AQI")
        label_label.place(x=1225,y=20)
        min_label = Label(self.win, text=round(self.min_aqi,2))
        min_label.place(x=1225, y=40)
        max_label = Label(self.win, text=round(self.max_aqi,2))
        max_label.place(x=1225, y=50+(self.max_aqi-self.min_aqi+.1)*27)

        for i in decimal_range(self.min_aqi, self.max_aqi, .1):
            color = '#%02x%02x%02x' % self.convert_aqi_to_color(i) # Converts to Hex
            try:
                self.canvas.create_rectangle(1230,50+(i-self.min_aqi)*27,1230+20,50+(i-self.min_aqi+.1)*27, fill=color, outline=color)
            except TclError:
                pass # Ignore this color error

    def update(self, requested_aqi):
        for state, arr in self.states.items():
            if arr[2] > int(requested_aqi):
                arr[3].configure(bg="red")
            else:
                arr[3].configure(bg="green")

    def main(self):
        self.win.mainloop()

if __name__ == '__main__':
    heatmap = HeatMap()
    heatmap.main()




