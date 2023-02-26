# Public_Code
# Repository for public-facing code! All of my publicly published work will be available here. 

# Simple YoloV5-based object detection script
# This is a simple script demonstrating the power of object detection with regards to automation.

# Possible implementations include:

# - Task automation
# - Computer-vision based logic implementations
# - Remote UI management

# and probably more.

# Note: There is a separate object detection script that is not included in this repository. It is not yet ready for publish, and creating your own stand-in script would # serve as a good exercise for anyone wishing to implement this code. Otherwise, it will be published in time.
# This script is based off of a YoloV5 object detection model. Images were collected with a custom screenshot script, labeled with ImageSense.ai, and trained for up to # 600 epochs. Every imported library is necessary, and should be installed to your pytorch or yolov5 version specs. Virtual environments are strongly recommended. 

# Two functions are defined: one for UI interaction and one for overlay generation. They are run concurrently with threading, in the form of crude while True: loops.    # They will eventually be updated to include higher logic control. Image processing is a key step in both functions, and can be leveraged to generate better model       # training results and improve object recognition. The click function assumes the input of a variable named coord in the form of an (x , y) ordered pair at the center of # the object's location on-screen, and executes simple mouse movement and click functions using pyautogui. Custom functions then demonstrate basic UI interaction using  # the defined screenshot and click functions.

# Threading is required for the visual overlay and click functions to run in parallel.

# This script forms the basis of a potentially vast number of UI interactions based on computer vision.
