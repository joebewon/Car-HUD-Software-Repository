# Copyright (c) 2022 Joseph Habisohn

import serial # Import the Python Serial package for serial communication
from tkinter import * # Import Tkinter for the GUI
import threading as thread # Import the Python Threading package for multithreading

# Set up serial connection to laser
ser = serial.Serial(
    port='/dev/ttyAMA1',
    baudrate = 19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# GUI class based on APP class from
# stackoverflow.com/questions/459083 | Kevin's Response

# Run all GUI code in its own thread
# to allow both the rest of the code to run
class GUI(thread.Thread):
    def __init__(self):
        thread.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    # Run the GUI
    def run(self):
        # Set up window
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        width = self.root.winfo_screenwidth() # Get width of screen
        height = self.root.winfo_screenheight() # Get height of screen

        self.root.geometry("%dx%d" % (width, height)) # Set size of window to fullscreen

        # Set up Distance text
        global distance # Put distance into the global scope
        distance = Label(self.root, text="Starting Up", font=("Arial", 25))
        distance.grid(row=0, column=0)

        # Set up Braking Distance Text
        global braking_distance
        braking_distance = Label(self.root, text=" ", font=("Arial", 25))
        braking_distance.grid(row=0, column=2)

        # Braking Distance indicator
        global BD_indicator
        BD_indicator = Canvas(self.root, height=76, width=228, bg="gray")
        BD_indicator.grid(row=1, column=2)

        global BDlight
        BDlight = BD_indicator.create_oval(8, 8, 68, 68, outline="gray", fill="gray")

        global BDtext
        BDtext = BD_indicator.create_text(114, 38, font=("Arial", 13), text="Error, Proceed with caution")

        # TEMP: Make speed slider in m/s
        global speed
        speed = Scale(self.root, from_=0, to=40, orient="horizontal")
        speed.grid(row=2, column=0)

        # 3 second rule header
        global threeSHeader
        threeSHeader = Label(self.root, text="Three second rule distance:", font=("Arial", 25))
        threeSHeader.grid(row=0, column=3)

        # 3 second rule indicator
        global TSR_indicator
        TSR_indicator = Canvas(self.root, height=76, width=228, bg="gray")
        TSR_indicator.grid(row=1, column=3)

        # create the TSR stop light
        global TSRlight
        TSRlight = TSR_indicator.create_oval(8, 8, 68, 68, outline="gray", fill="gray")

        global TSRtext
        TSRtext = TSR_indicator.create_text(114, 38, font=("Arial", 13), text="Error, Proceed with caution")

        # Start event loop
        self.root.mainloop()
        
        # print to GUI as (widget, new_text)
        def printg(*args):
            args[1].config(text=args[2])
    
        # Change the options of the canvas oval item
        # red = "red", yellow = "yellow", green = "#00E518"
        def changeTSRLight(self, color):
            if color.lower() == "red":
                TSR_indicator.itemconfigure(TSRtext, fill="gray")
                TSR_indicator.coords(TSRtext, 0, 0)
                TSR_indicator.itemconfigure(TSRlight, outline=color.lower(), fill=color.lower())
                TSR_indicator.coords(TSRlight, 8, 8, 68, 68)

        def changeBDLight(self, color):
            if color.lower() == "red":
                BD_indicator.itemconfigure(BDtext, fill="gray")
                BD_indicator.coords(BDtext, 0, 0)
                BD_indicator.itemconfigure(BDlight, outline=color.lower(), fill=color.lower())
                BD_indicator.coords(BDlight, 8, 8, 68, 68)

            elif color.lower() == "yellow":
                BD_indicator.itemconfigure(BDtext, fill="gray")
                BD_indicator.coords(BDtext, 0, 0)
                BD_indicator.itemconfigure(BDlight, outline=color.lower(), fill=color.lower())
                BD_indicator.coords(BDlight, 8 + 76, 8, 68 + 76, 68)
        
            elif color.lower() == "#00E518" or color.lower() == "green":
                BD_indicator.itemconfigure(BDtext, fill="gray")
                BD_indicator.coords(BDtext, 0, 0)
                BD_indicator.itemconfigure(BDlight, outline="#00E518", fill="#00E518")
                BD_indicator.coords(BDlight, 8 + 76 + 76, 8, 68 + 76 + 76, 68)

            elif color.lower() == "err":
                BD_indicator.itemconfigure(BDlight, outline="gray", fill="gray")
                BD_indicator.itemconfigure(BDtext, fill="black")
                BD_indicator.coords(BDtext, 114, 38)

            else:
                raise ValueError("Incorrect input: color must be \"red\", \"yellow\", \"#00E518\", \"green\", or \"err\"")

gui = GUI() # Start the GUI

mu_tire_road = 0.7 # Coefficient of Friction of a dry road

# Error codes of the laser
err = {":Er01!": "Power input to low, power voltage should be >= 2.0V.",
    ":Er02!": "Internal error, don\'t care.",
    ":Er03!": "Module temperature is too low (< -20C).",
    ":Er04!": "Module temperature is too high (> +40C).",
    ":Er05!": "Target out of range.",
    ":Er06!": "Measure result invalid.",
    ":Er07!": "Background light too strong.",
    ":Er08!": "Laser signal too weak.",
    ":Er09!": "Laser signal too strong.",
    ":Er10!": "Hardware fault 1.",
    ":Er11!": "Hardware fault 2.",
    ":Er12!": "Hardware fault 3.",
    ":Er13!": "Hardware fault 4.",
    ":Er14!": "Hardware fault 5.",
    ":Er15!": "Laser signal not stable.",
    ":Er16!": "Hardware fault 6.",
    ":Er17!": "Hardware fault 7."
    }

# Function to send the command, calculate the values, and print the data
def send(string):
    #ser.write(string) # Send command

    x = str(ser.readline()) # Read laser data
    print(x)

    # Parse data, ep. 1: there could be an error | can be changed to suit other lasers
    potential_err = x[3:9] # Where the error key could be (see err.keys())

    # Check if an error was received
    flag = False
    for i in err.keys():
        if potential_err == i:
            flag = True
    
    # If there was an error
    if flag:
        # Parse data, ep. 2: print the error | can be changed to suit other lasers
        actual_err_c = x[2:9] + " " + err.get(x[3:9]) # Error message printed to console
        actual_err_g = x[4:9] + " " + err.get(x[3:9]) # Error message printed to GUI

        # Print error
        print(actual_err_c) # to console
        gui.printg(distance, actual_err_g) # to GUI

        # Print braking distance
        brakingDistance = ((speed.get() ** 2)) / (2 * mu_tire_road *  9.81) # Calculate
        print(brakingDistance) # to console
        gui.printg(braking_distance, "Braking Distance:\n" + str(brakingDistance) + "m") # to GUI

        # Print three second rule distance
        threeSDist = speed.get() * 3.0 # Calculate
        print(threeSDist) # to console
        gui.printg(threeSHeader, "Three second rule distance:\n" + str(threeSDist) + "m") # to GUI
        gui.changeTSRLight("err") # Make TSR_indicator show an error message
        gui.changeBDLight("err") # Make BD_indicator show an error message

    # otherwise
    else:
        # Parse data, ep. 3: There was no error | can be changed to suit other lasers
        try:
            dist_c = x[2:x.index("\\")] # Distance printed to console

        except BaseException as error:
            print("Failed at send().if:else.try_1.\n" + str(error))

        try:
            if x[5:6] == " ":
                dist = float(x[5:x.index("m")]) # Actual distance value as a float
                dist_g = "Distance: " + x[5:x.index(",")] # Distance printed to GUI

            else:
                dist = float(x[4:x.index("m")]) # Actual distance value as a float
                dist_g = "Distance: " + x[4:x.index(",")] # Distance printed to GUI

        except BaseException as error:
            print("Failed at send().if:else.try_2.\n" + str(error))
            
        try:    
            # Print distance
            print(dist_c) # to console
            gui.printg(distance, dist_g) # to GUI

            # Print braking distance
            brakingDistance = ((speed.get() ** 2)) / (2 * mu_tire_road *  9.81) # Calculate
            print(brakingDistance) # to console
            gui.printg(braking_distance, "Braking Distance:\n" + str(brakingDistance) + "m") # to GUI

            # Print three second rule distance
            threeSDist = speed.get() * 3.0 # Calculate
            print(threeSDist) # to console
            gui.printg(threeSHeader, "Three second rule distance:\n" + str(threeSDist) + "m") # to GUI

            # Change TSR_indicator depending on how close you are to the next car
            if dist > threeSDist + 10.0:
                gui.changeTSRLight("green")

            elif dist <= threeSDist + 10.0 and dist > threeSDist:
                gui.changeTSRLight("yellow")

            else:
                gui.changeTSRLight("red")

            # Change BD_indicator depending on how close you are to the next car
            if dist > brakingDistance + 10.0:
                gui.changeBDLight("green")

            elif dist <= brakingDistance + 10.0 and dist > brakingDistance:
                gui.changeBDLight("yellow")

            else:
                gui.changeBDLight("red")

        except BaseException as error:
            print("Failed at send().if:else.try_3.\n" + str(error))

# Dictionary of laser commands
commands = {"laser_on": [0x4F], # Hex value of O
            "laser_off": [0X43], # Hex value of C
            "laser_get_dist": [0x44], # Hex value of D
            "laser_get_temp": [0x53] # Hex value of S
            }

send(commands.get("laser_on")) # Turn laser on
while 1:
    send(commands.get("laser_get_dist")) # Continuously get the measured distance
