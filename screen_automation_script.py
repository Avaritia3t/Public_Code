#Automation script. This script is responsible for executing a series of actions based on computer vision, in the form of automating game tasks.
import detection #this is a custom script not included in the repository, it will be made public eventually.
import mss
import time
import random
import keyboard
import pyautogui
import cv2
import torch
import win32gui
import win32api
import threading
import numpy as np
import psutil

# Get the handle of the window to capture
hwnd = win32gui.FindWindow(None, 'Window_Name')

# Get the dimensions of the window
# Pre-define a monitor object to use for screenshotting
window_rect = win32gui.GetWindowRect(hwnd)
left, top, right, bottom = window_rect
width = right - left
height = bottom - top
monitor = {"top": top, "left": left, "width": width, "height": height, "name": "Window_Name"}

# Load the YOLOv5 model
# This must be changed every time to select the appropriate weights!
model = torch.hub.load('ultralytics/yolov5', 'custom', r'C:\path\to\weights')
model.cuda()

# This function is responsible for screenshotting and streaming the capture window with bounding box overlays imposed by the model.
def ss():
    # Create a screenshot object
    with mss.mss() as sct:
        while True:
            # Capture the screen as a np array image (for easy processing, adjust to your image type as you like)
            img = np.array(sct.grab(monitor))

            # Convert the image from BGR to RGB (may not be necessary for your application)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Pass the image to the model for inference
            results = model(img)

            # Display the image with bounding boxes
            # Create a named window with custom dimensions and make it resizable
            cv2.namedWindow("Screenshot", cv2.WINDOW_NORMAL)
            cv2.imshow("Screenshot", cv2.cvtColor(results.render()[0], cv2.COLOR_RGB2BGR))

            # Press 'q' to quit
            # This is more useful if you want to take single screenshots, and is generally useless inside the while loop.
            # If you don't include cv2.waitKey() after cv2.imshow(), the kernel will crash and your screenshot will not load. :)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break 
            
            # Simple memory management to make sure the loop doesn't consume too many resources
            cpu_percent = psutil.cpu_percent()
            mem_percent = psutil.virtual_memory().percent
            # Break the loop if CPU usage or memory consumption exceeds a threshold
            if cpu_percent > 80 or mem_percent > 80:
                print("Resource usage too high, breaking loop")
                break

# This function is responsible for clicking based on a set of coordinates retrieved from the object detection script.
def click(coords):
    print('Searching for coordinates...')
    if coords == None: # No coordinates will arise from an empty object detction set, so should be addressed in error/exception handling.
        print('No coordinates received', coords)
        return
    elif not isinstance(coords, tuple) or len(coords) != 2: # If coords are not None, but are not an expected (x, y) pair:
        print('Coordinates not recognized', coords)
        return
    else: # Otherwise,
        # Move the mouse to the destination in a bezier curve with easing
        print('Coordinates found, moving mouse to', coords)
        duration = 0.7 # Mouse movement duration, can be adjusted or defined elsewhere. Instant moving is not acceptable input.
        x, y = coords #split the coordinates into an x, y pair.
        pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeOutQuad)

        # Perform a mouse down and mouse up action
        print('Clicking...')
        pyautogui.click()
        
        # Generate a series of random mouse movements
        print('Moving mouse randomly')
        duration = random.uniform(0.2, 2)
        start_time = time.time()
        while time.time() - start_time < duration:
            x_offset = random.randint(-5, 5)
            y_offset = random.randint(-5, 5)
            pyautogui.moveRel(x_offset, y_offset, duration=0.01)

        # Wait for a random duration between 0.1 and 0.3 seconds
        print('Waiting...')
        time.sleep(random.uniform(0.1, 3))

# A custom function to collect items based on what the computer sees.
def harvest_things():
    objects = detection.detect() # Custom detection function from a script included but not outlined here.
    coords = detection.find_center_coords('thing1', objects) # Custom coordinate isolation function from the same script
    while coords is None:
        objects = detection.detect()
        coords = detection.find_center_coords('thing1', objects)
    click(coords) 

# A custom function to perform another UI interaction based on computer vision.
def exchange_things():
    objects = detection.detect()
    coords = detection.find_center_coords('thing2', objects)
    while coords is None:
        objects = detection.detect()
        coords = detection.find_center_coords('thing2', objects)
    click(coords) 

inventories_emptied = 0

# High level function to control all actions.
def train():
    while True:
        harvest_things()
        sleep_duration1 = random.uniform(37,50)
        print('sleeping for ', sleep_duration1, 'seconds.')
        time.sleep(sleep_duration1)
        exchange_things()
        sleep_duration2 = random.uniform(20,30)
        print('sleeping for ', sleep_duration2, 'seconds.')
        time.sleep(sleep_duration2)
        global inventories_emptied
        inventories_emptied += 1
        print('Inventories emptied: ', inventories_emptied)

        cpu_percent = psutil.cpu_percent()
        mem_percent = psutil.virtual_memory().percent
        # Break the loop if CPU usage or memory consumption exceeds a threshold
        if cpu_percent > 80 or mem_percent > 80:
            print("Resource usage too high, breaking loop")
            break

# While true, Train.
# Threading required to allow image printing and click execution to happen simultaneously.
def train_loop():
    if __name__ == '__main__':
        t1 = threading.Thread(target=train)
        t2 = threading.Thread(target=ss)
        t1.start()
        t2.start()

train_loop() #do the thing! That felt good, right?