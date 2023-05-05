import mss
import numpy as np
import cv2
import torch
import win32gui
import random

def detect(model):
    """
    Detect objects in a screenshot of the game window using the given YOLOv5 model.
    Args:
        model: A YOLOv5 model.
    Returns:
        A list of tuples containing the object name and its center coordinates.
    """

    # Get the handle of the game Window
    hwnd = win32gui.FindWindow(None, 'window_name')

    # Get the dimensions of the window
    # Establish non-specific window sizes defined by the edges of the window, allowing the window to be resized without issue.
    window_rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = window_rect
    width = right - left
    height = bottom - top

    # Set monitor region
    monitor = {"top": top, "left": left, "width": width, "height": height, "name": "window_name"}

    # Prepare the YOLOv5 model for inference
    model.cuda()
    model.conf = 0.4 # Set detection confidence threshold

    def get_screenshot_results():
        """
        Capture a screenshot of the game window and get object detection results.
        Returns:
            A pandas DataFrame containing the detection results.
        """

        # Create a screenshot object
        with mss.mss() as sct:
            # Screenshot monitor region
            img = np.array(sct.grab(monitor))

            # Convert the image from BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Pass the image to the model for inference
            results = model(img)

            # Extract detections
            # pandas().xyxy[0] returns the results from the located objects loaded into a panda dataframe, in an (xmin, ymin, xmax, ymax) format. Only working with 1 image, so index 0.
            detections = results.pandas().xyxy[0]

            return detections

    def analyze(detections):
        """
        Extract the objects and their centers, and bounding box coordinates.
        Args:
            detections: A Pandas DataFrame containing the detected objects' information.
        Returns:
            A list of tuples containing the object name, center coordinates, and bounding box coordinates.
        """

        objects = []
        # X coord of left edge, y coord of top edge, x coord of right edge, y coord of bottom edge
        for i, row in detections.iterrows():
            object_name = row['name']
            object_center = ((row['xmin'] + row['xmax']) / 2, (row['ymin'] + row['ymax']) / 2)
            bbox_coords = (row['xmin'], row['ymin'], row['xmax'], row['ymax'])
            objects.append((object_name, object_center, *bbox_coords))

        return objects

    def remove_duplicates(objects):
        """
        Remove duplicate object detections, keeping a random entry for each object type.
        Args:
            objects: A list of tuples containing the object name and its center coordinates.
        Returns:
            A list of tuples containing unique object names and their center coordinates.
        """
        
        # If the name isn't in the list, add it.
        unique_entries = {}
        for name, coords in objects:
            if name not in unique_entries:
                unique_entries[name] = coords
            else:
                # If a duplicate is found, keep a random entry and discard the rest. This should be modified to fit desired behavior.
                if random.random() < 0.5:
                    unique_entries[name] = coords
        return [(name, coords) for name, coords in unique_entries.items()]

    # Simple logic that runs the function.
    # Take a screenshot and get the results in a df.
    objects_onscreen = get_screenshot_results()

    # Analyze the df results and return centers.
    objects_and_centers = analyze(objects_onscreen)

    # Only keep the unique objects.
    unique_objects_onscreen = remove_duplicates(objects_and_centers)

    # And return them for viewing.
    return unique_objects_onscreen

def find_object(thing, objects):
    """
    Find the first occurrence of an object in a list of object detections.
    Args:
        thing: The object name to search for.
        objects: A list of tuples containing object names and their center coordinates.
    Returns:
        A tuple containing the object name, center coordinates, xmin, ymin, xmax, and ymax, or None if not found.
    """

    # Simple function that determines if a thing was found on-screen. If not, returns None. 
    for obj in objects:
        if obj[0] == thing:
            return obj
    return None

def find_center_coords(thing, model):
    """
    Find the center coordinates of a specified object.
    Args:
        thing: The object name to search for.
        model: A YOLOv5 model.
    Returns:
        A tuple containing the center coordinates of the object, or None if not found.
    """

    # Run detection using a model, return the results in a variable named objects.
    objects = detect(model) 
    
    # Determine if thing is in the detected objects. If so, return coordinates. Else, None.
    obj = find_object(thing, objects)
    return obj[1] if obj else None

def check_for(thing, model):
    """
    Check if a specified object is present in the detection results.
    Args:
        thing: The object name to search for.
        model: A YOLOv5 model.
    Returns:
        True if the object is found, False otherwise.
    """

    # Honestly almost redundant with find_object()
    objects = detect(model)
    obj = find_object(thing, objects)
    return obj is not None

def find_borders(thing, model):
    """
    Find the bounding box coordinates of a specified object.
    Args:
        thing: The object name to search for.
        model: A YOLOv5 model.
    Returns:
        A dictionary containing the xmin, ymin, xmax, and ymax of the object's bounding box, or None if not found.
    """

    objects = detect(model)
    obj = find_object(thing, objects)
    if obj:
        borders = {
            'xmin': obj[2],
            'ymin': obj[3],
            'xmax': obj[4],
            'ymax': obj[5]
        }
        return borders
    return None
