
#%% hello

import pytesseract
import pyautogui
import time
import numpy as np
import mss
from PIL import Image
import cv2
from difflib import SequenceMatcher
from pytesseract import Output
import ctypes

# If on Windows, tell pytesseract where to find the .exe:
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\wfloyd\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"


#base_path = 'C:\\Users\\wfloyd\\OneDrive - The Kleingers Group\\Documents\\Python Scripts\\MiscellaneousPython\\ScreenShots'
#image_path = 'C:\\Users\\wfloyd\\OneDrive - The Kleingers Group\\Documents\\Python Scripts\\MiscellaneousPython\\ScreenShots\\Images'
#group_path = base_path + '\\GroupNames'
click_time = 0.02




def determine_center_monitor():
    sct = mss.mss()
    monitors = sct.monitors
    for i in range(len(monitors)):
        if monitors[i]['left'] == 0:
            return i


center_monitor_index = determine_center_monitor()


#%% 

def invert_bw_image(bw_image):
    #Might seem unnecessary, but just wanted a cleaner wrapper
    return cv2.bitwise_not(bw_image)



def preprocess_bw(image,stretch=2,cutoff=200):
    #Convert to grayscale if needed
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    
    #Resize to help OCR resolution
    gray = cv2.resize(gray, None, fx=stretch, fy=stretch, interpolation=cv2.INTER_CUBIC)

    #Apply binary thresholding
    _, bw = cv2.threshold(gray, cutoff, 255, cv2.THRESH_BINARY)

    #Invert if dark mode
    if bw.mean() < 127:
        '''
        We need to flip the cutoff if we do this.  I'll spare too much detail, 
        but the cutoff is generally tuned to work better in light mode.  If it's 
        in dark mode you need to go the other way
        '''
        gray = cv2.bitwise_not(gray)
        _, bw = cv2.threshold(gray, 255-cutoff, 255, cv2.THRESH_BINARY)

    return bw

#Make a separate function to blow up the original photo
#This sort of transformation is common for thiese purposes
def resize_image(image,ratio):  
    # Resize to help OCR resolution
    new_img = cv2.resize(image, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_CUBIC)
    return new_img


def show_image(image):
    #takes a cv2 image object and displays it
    #I feel like I occasionally want to see these images and can't remember how
    cv2.imshow("Gray image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


#basic like type search
def like(fragment: str, target: str) -> bool:
    return fragment.lower() in target.lower()


def move_and_click(x,y,duration=0.5):
    pyautogui.moveTo(x, y, duration=duration)
    pyautogui.click()
    time.sleep(1)



def click_n_times(n=1):
    for i in range(n):
        pyautogui.click()



#This is the definitive final image click function.  Works well
def find_image_and_click(image_name,image_path, region=None, confidence=0.85, click=True, double_click = False):
    """
    Finds an image on screen and optionally clicks it.
    
    Parameters:
        image_path (str): Path to the image to locate.
        region (tuple or None): (left, top, width, height) to restrict the search area.
        confidence (float): Match confidence (requires OpenCV).
        click (bool): Whether to click the found location.

    Returns:
        Box or None: The located box if found, else None.
    """
    location = pyautogui.locateOnScreen(image_path + '\\' + image_name + '.png', region=region, confidence=confidence)
    
    if location:
        x, y = pyautogui.center(location)
        if click:
            pyautogui.moveTo(x, y, duration=click_time)
            n = 1
            if double_click:
                n = 2

            #This handles double click instances
            click_n_times(n)
        return location
    else:
        print(f"Image '{image_path}' not found.")
        return None



#This is a very crude "couldn't find it try again" type of function
def repeat_find_click(image,path,retry_time=2,wait_after=0.5,alt_image=None,**kwargs):
    for i in range(10):
        try:
            find_image_and_click(image,path,**kwargs)
            time.sleep(wait_after)
            return 0
        except:
            if alt_image: #Indicates a second image has been entered
                find_image_and_click(alt_image,path,**kwargs)
                time.sleep(wait_after)
                return 0
            print("image hasn't loaded yet, waiting")
            time.sleep(retry_time) #take a 5 second pause then try again
    return 0







#Alright here's the find text function.  It's a bit trickier than 
#the image one.  
def find_text_candidates(target_word, stretch = 2,cutoff = 200,threshold=0.8, monitor_index = center_monitor_index, show_bw = False,show_annotate = False):
    """
    Find candidate matches for a word in an image using OCR.
    
    Args:
        target_word: Word to match.
        stretch: factor to stretch image by to increase searchability
        cutoff: This is an argument to denote the cutoff value for binary image changing higher means make things darker
        threshold: Similarity threshold (0 - 1) for fuzzy matching.
        draw: If True, draw boxes on a copy of the image.

    Returns:
        List of matched words with their bounding boxes: [(word, x, y, w, h), ...]
        Optionally displays an annotated image.
    """
    #This gets our initial screen shot, conver to an array then a cv2 object
    sct = mss.mss()
    monitors = sct.monitors
    monitor = monitors[monitor_index]

    # Grab screenshot of the selected monitor
    raw_img = sct.grab(monitor)

    #Convert it to an array then cv2 object
    img = np.array(raw_img)
    image = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    #Need to do some preprocessing to help with search. 
    gray = preprocess_bw(image,stretch=stretch,cutoff=cutoff)
    
    #This shows the black and white image should you want to see it.  It can be helpful
    #to tune the function for certain words
    if show_bw:
        temp = resize_image(gray,1/stretch)
        show_image(temp)

    #This is a very raw output of essentially everything the OCR engine finds
    data = pytesseract.image_to_data(gray, output_type=Output.DICT)
    
    #This is where we track candidate words
    matches = []
    for i in range(len(data['text'])):
        word = data['text'][i].strip() #Take the i-th candidate word
        if word: #Many are blank so this only does the ones that are words

            #This is a function that does a fuzze match
            score = SequenceMatcher(None, word.upper(), target_word.upper()).ratio()
            
            if score >= threshold:
                #Take the pertinent info and add it to matches
                x, y, w, h = data ['left'][i], data['top'][i], data['width'][i], data['height'][i]
                matches.append((word, x, y, w, h))
    



    #Copy initial image and scale it up
    annotated = image.copy()
    annotated = resize_image(annotated,stretch)
    final_spots = []
    
    if matches:
        for word, x, y, w, h in matches:
            if like(target_word,word): #Here we check if the words are similar.  
                cv2.rectangle(annotated, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(annotated, word, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 1)
                
                #Add the spots for clicking.  Note, the image hasn't been resized yet, I'm hoping
                #we can get away with dividing by the stretch
                temp_x,temp_y = x+w//2, y+h//2
                final_spots.append((temp_x//stretch,temp_y//stretch)) #Add these spots for clicking
        
        annotated = resize_image(annotated,1/stretch)

        if show_annotate:
            cv2.imshow("Matches", annotated)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


    '''
    It returns words left to right, top to bottom in order.  It will be a bit
    manual but this will allow you to pick out individual words if you don't want to
    click them all
    '''
    
    return final_spots


#It's a bit cleaner to do it this way instead
#It can let you pick out individual words
def find_all_and_click(target_word,**kwargs):

    candidates = find_text_candidates(target_word=target_word,**kwargs)
    for x,y in candidates:
        move_and_click(x,y)

#a = find_all_and_click('PDF',show_annotate = False)

