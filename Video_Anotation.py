from google.cloud import vision
from google.cloud.vision import types
client = vision.ImageAnnotatorClient()

def process_Image():
    # [START vision_quickstart]
    import io
    import os
    # Imports the Google Cloud client library
    # [START vision_python_migration_import]
    from google.cloud import vision
    from google.cloud.vision import types
    # [END vision_python_migration_import]
    # Instantiates a client
    # [START vision_python_migration_client]
    client = vision.ImageAnnotatorClient()
    # [END vision_python_migration_client]
    # The name of the image file to annotate
    file_name = os.path.join(
        os.path.dirname(__file__),
        'people.jpg')
    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')
    for label in labels:
        print(label.description)
    # [END vision_quickstart]



OUTPUT_VIDEO = 'output3.avi' # Output as AVI file
INPUT_VIDEO  = 'human.mp4'     # Input video (mov, avi, mp4, etc)

##
# Process video
##
import cv2
import io
import os
import requests
import base64
import json
import sys

# Function to make output text more readable
def makeLikelyText(i):
    if i == "VERY_LIKELY":
        return "absolutly"
    elif i == "LIKELY":
        return "probably"
    elif i == "POSSIBLE":
        return "maybe"
    elif i == "UNLIKELY":
        return "probably not"
    else:
        return "not"

# Load the input video
vidcap = cv2.VideoCapture(INPUT_VIDEO)

# Set output codec
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

# Create the output video
outputvid = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, int(vidcap.get(cv2.CAP_PROP_FPS)), (int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))), True)

# Count the number of frames
count = 0

# Load succes?
success = True

# Run through all frames
while success:
    success, image = vidcap.read()

    # Print current status
    print('Process frame: ', count, ' of ', int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)))

    # Save image to temp jpg file
    cv2.imwrite("__tmp.jpg", image)
    image2 = image

    # Remove the file, it is not needed anymore
    
    # # Do the API callable for faces when even
    if (count % 2 == 0):
        file_name = os.path.join(
        os.path.dirname(__file__),
        '__tmp.jpg')
        # Loads the image into memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations
        try:
            if(len(labels)!= 0):
                #print("Labels is Running")
                print(labels)
                for label in labels:
                    label_final = label['description'] + ' (' + str(int((label['score']*100))) + '%) - '
                    labels.append(label_final[:-2])
            
                # Sort 
                labels.sort()

                cv2.putText(image2, ' '.join(labels), (4, 42), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
        except:
            pass # pass if something misses in this frame
        outputvid.write(image2)
    count += 1

    os.remove("__tmp.jpg")
    # flush outputvid
    sys.stdout.flush()

    # Set this if you want the video to render prematurely
    if count == 3341:
        break

# Wrap everything up
#cv2.destroyAllWindows()
outputvid.release()
