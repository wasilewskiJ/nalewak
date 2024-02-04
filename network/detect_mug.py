import cv2
import numpy as np
import os
import pickle
from tflite_runtime.interpreter import Interpreter
from tflite_runtime.interpreter import load_delegate

# Configuration constants
MODEL_DIR = './model'
GRAPH_NAME = 'detect.tflite'
LABELMAP_NAME = 'labelmap.txt'
MIN_CONF_THRESHOLD = 0.5
IMAGE_NAME = '../ready_img.png'
USE_TPU = False
SAVE_RESULTS = True
SHOW_RESULTS = True

# Path definitions
CWD_PATH = os.getcwd()
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_DIR, GRAPH_NAME)
PATH_TO_LABELS = os.path.join(CWD_PATH, MODEL_DIR, LABELMAP_NAME)
PATH_TO_IMAGE = os.path.join(CWD_PATH, IMAGE_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]
if labels[0] == '???':
    del(labels[0])

# Configure TensorFlow Lite interpreter
if USE_TPU:
    interpreter = Interpreter(model_path=PATH_TO_CKPT,
                              experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
else:
    interpreter = Interpreter(model_path=PATH_TO_CKPT)
interpreter.allocate_tensors()

# Model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

floating_model = (input_details[0]['dtype'] == np.float32)
input_mean = 127.5
input_std = 127.5

# Load and process the image
image = cv2.imread(PATH_TO_IMAGE)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
imH, imW, _ = image.shape 
image_resized = cv2.resize(image_rgb, (width, height))
input_data = np.expand_dims(image_resized, axis=0)

if floating_model:
    input_data = (np.float32(input_data) - input_mean) / input_std

interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()

# Retrieve detection results
boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects

# Process detections
centers = []  # List to store centers of detected mugs

# Loop through all detections
for i in range(len(scores)):
    if scores[i] > MIN_CONF_THRESHOLD:
        ymin, xmin, ymax, xmax = boxes[i]
        ymin = int(max(1, (ymin * imH)))
        xmin = int(max(1, (xmin * imW)))
        ymax = int(min(imH, (ymax * imH)))
        xmax = int(min(imW, (xmax * imW)))
        
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)
        
        # Calculate center
        center_x = (xmin + xmax) // 2
        center_y = (ymin + ymax) // 2
        centers.append((center_x, center_y))

        # Draw label
        object_name = labels[int(classes[i])]
        label = '%s: %d%%' % (object_name, int(scores[i] * 100))
        cv2.putText(image, label, (xmin, ymin-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Display the image with detections
if SHOW_RESULTS:
    cv2.imshow('Object detector', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Save detection results
if SAVE_RESULTS:
    cv2.imwrite('detected_' + IMAGE_NAME, image)
    with open('centers.pkl', 'wb') as f:
        pickle.dump(centers, f)

