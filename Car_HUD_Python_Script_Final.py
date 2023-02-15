# Copyright (c) 2022 Joseph Habisohn

from numpy import ceil # Import the ceil() function from numpy
import threading as thread # Import the Python threading package and name it thread
import serial #Import Python Serial package
import obd # Import the python-OBD package
from tkinter import * # Import Tkinter

# Try all USB ports until the LiDAR connects
j = None
for i in range(5):
    try:
        ser = serial.Serial(
            port='/dev/ttyUSB' + str(i), 
            baudrate = 115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        print(ser.read())
        if ser.read() == b'Y':
            j = i
            break
    except:
        print("Wrong Port")

# Try all USB ports until the OBD-II connects
for i in range(5):
    if i == j:
        continue
    
    connection = obd.OBD("/dev/ttyUSB" + str(i))
    print(connection.is_connected())
    if connection.is_connected():
       break
    
if not connection.is_connected():
    velocity = 0.0
# Set up Tkinter
root = Tk()

guiFactor = 1.6 # Used to scale the entire gui by 1.6 times to fit the screen

# Set the size of the window to fullscreen
width = root.winfo_screenwidth() # Get width of screen
height = root.winfo_screenheight() # Get height of screen

root.geometry("%dx%d" % (width, height)) # Set size of window to fullscreen

# Padding
padding = Label(root, text="|\n|\n|\n|\n|\n|", font=("Arial", 30), fg='gainsboro')
padding.grid(row=0, column=0)

# Set up Distance text
distance = Label(root, text="Starting Up", font=("Arial", int(ceil(25 * guiFactor))), padx=5, pady=5)
distance.grid(row=1, column=0)

# Set up speed header
speed = Label(root, text="Starting Up", font=("Arial", int(ceil(25 * guiFactor))))
speed.grid(row=1, column=1, padx=5, pady=5)

# Set up Braking Distance Text
braking_distance = Label(root, text=" ", font=("Arial", int(ceil(25 * guiFactor))), padx=5, pady=5)
braking_distance.grid(row=2, column=1, padx=5, pady=5)

# Braking Distance indicator
BD_indicator = Canvas(root, height= int(ceil(76 * guiFactor)), width= int(ceil(228 * guiFactor)), bg="gray")
BD_indicator.grid(row=3, column=1, padx=5, pady=5)

# Create the BD stop light
BDlight = BD_indicator.create_oval(int(ceil(8 * guiFactor)), int(ceil(8 * guiFactor)), int(ceil(68 * guiFactor)), int(ceil(68 * guiFactor)), outline="gray", fill="gray")
BDtext = BD_indicator.create_text(int(ceil(114 * guiFactor)),  int(ceil(38 * guiFactor)), font=("Arial",  int(ceil(13 * guiFactor))), text="Error, Proceed with caution")
        
# 3 second rule header
threeSHeader = Label(root, text="Three second rule distance:", font=("Arial", int(ceil(25 * guiFactor))))
threeSHeader.grid(row=2, column=0, padx=5, pady=5)

# 3 second rule indicator
TSR_indicator = Canvas(root, height= int(ceil(76 * guiFactor)), width= int(ceil(228 * guiFactor)), bg="gray")
TSR_indicator.grid(row=3, column=0, padx=5, pady=5)

# Create the TSR stop light
TSRlight = TSR_indicator.create_oval(int(ceil(8 * guiFactor)), int(ceil(8 * guiFactor)), int(ceil(68 * guiFactor)), int(ceil(68 * guiFactor)), outline="gray", fill="gray")
TSRtext = TSR_indicator.create_text(int(ceil(114 * guiFactor)),  int(ceil(38 * guiFactor)), font=("Arial",  int(ceil(13 * guiFactor))), text="Error, Proceed with caution")

# print to GUI as printg(widget, new_text)
def printg(widget, string):
    widget.config(text=string)

# Change the options of the canvas oval item
# red = "red", yellow = "yellow", green = "#00E518"
def changeTSRLight(color):
    if color.lower() == "red":
        TSR_indicator.itemconfigure(TSRtext, fill="gray")
        TSR_indicator.coords(TSRtext, 0, 0)
        TSR_indicator.itemconfigure(TSRlight, outline=color.lower(), fill=color.lower())
        TSR_indicator.coords(TSRlight, int(ceil(8 * guiFactor)), int(ceil(8 * guiFactor)), int(ceil(68 * guiFactor)), int(ceil(68 * guiFactor)))
    
    elif color.lower() == "yellow":
        TSR_indicator.itemconfigure(TSRtext, fill="gray")
        TSR_indicator.coords(TSRtext, 0, 0)
        TSR_indicator.itemconfigure(TSRlight, outline=color.lower(), fill=color.lower())
        TSR_indicator.coords(TSRlight, int(ceil((8 * guiFactor) + (76 * guiFactor))), int(ceil(8 * guiFactor)), int(ceil((68 * guiFactor) + (76 * guiFactor))), int(ceil(68 * guiFactor)))
    
    elif color.lower() == "#00E518" or color.lower() == "green":
        TSR_indicator.itemconfigure(TSRtext, fill="gray")
        TSR_indicator.coords(TSRtext, 0, 0)
        TSR_indicator.itemconfigure(TSRlight, outline="#00E518", fill="#00E518")
        TSR_indicator.coords(TSRlight, int(ceil((8 * guiFactor) + (76 * guiFactor) + (76 * guiFactor))), int(ceil(8 * guiFactor)), int(ceil((68 * guiFactor) + (76 * guiFactor) + (76 * guiFactor))), int(ceil(68 * guiFactor)))
    
    elif color.lower() == "err":
        TSR_indicator.itemconfigure(TSRlight, outline="gray", fill="gray")
        TSR_indicator.itemconfigure(TSRtext, fill="black")
        TSR_indicator.coords(TSRtext,  int(ceil(114 * guiFactor)),  int(ceil(38 * guiFactor)))
    
    else:
        raise ValueError("Incorrect input: color must be \"red\", \"yellow\", \"#00E518\", \"green\", or \"err\"")
    
def changeBDLight(color):
    if color.lower() == "red":
        BD_indicator.itemconfigure(BDtext, fill="gray")
        BD_indicator.coords(BDtext, 0, 0)
        BD_indicator.itemconfigure(BDlight, outline=color.lower(), fill=color.lower())
        BD_indicator.coords(BDlight, int(ceil(8 * guiFactor)), int(ceil(8 * guiFactor)), int(ceil(68 * guiFactor)), int(ceil(68 * guiFactor)))
    
    elif color.lower() == "yellow":
        BD_indicator.itemconfigure(BDtext, fill="gray")
        BD_indicator.coords(BDtext, 0, 0)
        BD_indicator.itemconfigure(BDlight, outline=color.lower(), fill=color.lower())
        BD_indicator.coords(BDlight, int(ceil((8 * guiFactor) + (76 * guiFactor))), int(ceil(8 * guiFactor)), int(ceil((68 * guiFactor) + (76 * guiFactor))), int(ceil(68 * guiFactor)))
    
    elif color.lower() == "#00E518" or color.lower() == "green":
        BD_indicator.itemconfigure(BDtext, fill="gray")
        BD_indicator.coords(BDtext, 0, 0)
        BD_indicator.itemconfigure(BDlight, outline="#00E518", fill="#00E518")
        BD_indicator.coords(BDlight, int(ceil((8 * guiFactor) + (76 * guiFactor) + (76 * guiFactor))), int(ceil(8 * guiFactor)), int(ceil((68 * guiFactor) + (76 * guiFactor) + (76 * guiFactor))), int(ceil(68 * guiFactor)))
    
    elif color.lower() == "err":
        BD_indicator.itemconfigure(BDlight, outline="gray", fill="gray")
        BD_indicator.itemconfigure(BDtext, fill="black")
        BD_indicator.coords(BDtext,  int(ceil(114 * guiFactor)),  int(ceil(38 * guiFactor)))
    
    else:
        raise ValueError("Incorrect input: color must be \"red\", \"yellow\", \"#00E518\", \"green\", or \"err\"")

mu_tire_road = 0.7 # Coefficient of Friction of a dry road

# Send OBD command and parse the response
velocity = connection.query(obd.commands.SPEED).value.to("m/s")
velocity = float(str(velocity).split(" ")[0])
printg(speed, "Current speed: " + format(velocity, ".2f") + "m/s") # Print to gui

# Function to parse the data from the lidar, calculate the values and print the data
def send():    
    global velocity
    
    #Get the distance from the lidar
    dist = 0
    TFbuff = [0,0,0,0,0,0,0,0,0]
    TFbuff[0] = ser.read() # Read laser data
    if TFbuff[0] == b'Y':
        TFbuff[1] = ser.read()
        if TFbuff[1] == b'Y':
            for i in range(2,8):
                TFbuff[i] = ser.read()
            TFbuff[8] = ser.read()
            dist = int.from_bytes(TFbuff[2],"big") + int.from_bytes(TFbuff[3],"big")*256 - 7                
            dist /= 100

    # If there was an error
    if dist > 170.00:
        # Parse data, ep. 1: print the error | can be changed to suit other lasers
        
        # Print error
        printg(distance, "Distance: Error") # to GUI
        
        # Print braking distance
        printg(braking_distance, "Braking Distance:\n" + format(((velocity ** 2)) / (2 * mu_tire_road *  9.81), ".2f") + "m") # to GUI
        
        # Print three second rule distance
        printg(threeSHeader, "Three second rule distance:\n" + format(velocity * 3.0, ".2f") + "m") # to GUI
            
        changeTSRLight("err") # Make TSR_indicator show an error message
        changeBDLight("err") # Make BD_indicator show an error message
        
    # otherwise
    else:
        # Parse data, ep. 2: There was no error | can be changed to suit other
        
        # Print distance
        printg(distance, "Distance: " + format(dist, ".2f") + "m") # to GUI
            
        # Print braking distance
        brakingDistance = ((velocity ** 2)) / (2 * mu_tire_road *  9.81) # Calculate
        printg(braking_distance, "Braking Distance:\n" + format(brakingDistance, ".2f")  + "m") # to GUI
        
        # Print three second rule distance
        threeSDist = velocity * 3.0 # Calculate
        printg(threeSHeader, "Three second rule distance:\n" + format(threeSDist, ".2f") + "m") # to GUI
        
        # Change TSR_indicator depending on how close you are to the next car
        if dist > threeSDist + 10:
            changeTSRLight("green")
        
        elif dist <= threeSDist + 10.0 and dist > threeSDist:
            changeTSRLight("yellow")
        
        else:
            changeTSRLight("red")
    
        # Change BD_indicator depending on how close you are to the next car
        if dist > brakingDistance + 10.0:
            changeBDLight("green")
        
        elif dist <= brakingDistance + 10.0 and dist > brakingDistance:
            changeBDLight("yellow")
        
        else:
            changeBDLight("red")
            
    #Get the distance form the lidar
    #dist = 0
    #TFbuff = [0,0,0,0,0,0,0,0,0]
    TFbuff[0] = ser.read() # Read laser data
    if TFbuff[0] == b'Y':
        TFbuff[1] = ser.read()
        if TFbuff[1] == b'Y':
            for i in range(2,8):
                TFbuff[i] = ser.read()
            TFbuff[8] = ser.read()
            dist = int.from_bytes(TFbuff[2],"big") + int.from_bytes(TFbuff[3],"big")*256 - 7                
            dist /= 100
            dist += 1.15
    
    # Send OBD command and parse the response
    velocity = connection.query(obd.commands.SPEED).value.to("m/s")
    velocity = float(str(velocity).split(" ")[0])
    printg(speed, "Current speed: " + format(velocity, ".2f") + "m/s") # Print to gui
    root.after(1, send)

# Constantly get the measured distance, calculate the data, and update the GUI
root.after(0, send)
root.mainloop() # Start event loop
