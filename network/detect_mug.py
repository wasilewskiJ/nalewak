######## Webcam Object Detection Using Tensorflow-trained Classifier #########
#
# Author: Evan Juras
# Date: 11/11/22
# Description:
# This program uses a TensorFlow Lite object detection model to perform object
# detection on an image or a folder full of images. It draws boxes and scores
# around the objects of interest in each image.
#
# This code is based off the TensorFlow Lite image classification example at:
# https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/examples/python/label_image.py
#
# I added my own method of drawing boxes and labels using OpenCV.

# Import packages
import os
import cv2
import numpy as np
import sys
import glob
import importlib.util
import pickle

def detect_objects():
    # Stałe wartości dla ścieżek do modelu i obrazu
    MODEL_NAME = './network/model'
    GRAPH_NAME = 'detect.tflite'
    LABELMAP_NAME = 'labelmap.txt'
    min_conf_threshold = 0.5
    use_TPU = False  # Zaktualizuj tę wartość zgodnie z potrzebami

    save_results = True  # Zaktualizuj tę wartość zgodnie z potrzebami
    show_results = False  # Zaktualizuj tę wartość zgodnie z potrzebami

    IM_NAME = './ready_img.png'  # Nazwa obrazu do analizy
    IM_DIR = None  # Zaktualizuj tę wartość, jeśli chcesz przetwarzać folder

    # Import TensorFlow libraries
    pkg = importlib.util.find_spec('tflite_runtime')
    if pkg:
        from tflite_runtime.interpreter import Interpreter
        if use_TPU:
            from tflite_runtime.interpreter import load_delegate
    else:
        from tensorflow.lite.python.interpreter import Interpreter
        if use_TPU:
            from tensorflow.lite.python.interpreter import load_delegate

    # Jeśli korzystamy z TPU, przypisujemy nazwę pliku modelu dla TPU
    if use_TPU:
        GRAPH_NAME = 'edgetpu.tflite'

    # Ścieżka do bieżącego katalogu roboczego
    CWD_PATH = os.getcwd()

    # Definiowanie ścieżki do obrazów i pobieranie nazw plików obrazów
    if IM_DIR:
        PATH_TO_IMAGES = os.path.join(CWD_PATH, IM_DIR)
        images = glob.glob(PATH_TO_IMAGES + '/*.jpg') + glob.glob(PATH_TO_IMAGES + '/*.png') + glob.glob(PATH_TO_IMAGES + '/*.bmp')
        if save_results:
            RESULTS_DIR = IM_DIR + '_results'
    else:
        PATH_TO_IMAGES = os.path.join(CWD_PATH, IM_NAME)
        images = glob.glob(PATH_TO_IMAGES)
        if save_results:
            RESULTS_DIR = './network/results'

    # Tworzenie katalogu wyników, jeśli użytkownik chce zapisać wyniki
    if save_results:
        RESULTS_PATH = os.path.join(CWD_PATH, RESULTS_DIR)
        if not os.path.exists(RESULTS_PATH):
            os.makedirs(RESULTS_PATH)

    # Ścieżka do pliku .tflite, który zawiera model używany do wykrywania obiektów
    PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, GRAPH_NAME)

    # Ścieżka do pliku z mapą etykiet
    PATH_TO_LABELS = os.path.join(CWD_PATH, MODEL_NAME, LABELMAP_NAME)

    # Wczytywanie mapy etykiet
    with open(PATH_TO_LABELS, 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    # Usuwanie pierwszej etykiety '???', jeśli jest obecna
    if labels[0] == '???':
        del(labels[0])

    # Wczytywanie modelu TensorFlow Lite i alokowanie tensorów
    interpreter = Interpreter(model_path=PATH_TO_CKPT) if not use_TPU else Interpreter(model_path=PATH_TO_CKPT, experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
    interpreter.allocate_tensors()


    # Get model details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    floating_model = (input_details[0]['dtype'] == np.float32)

    input_mean = 127.5
    input_std = 127.5

    # Check output layer name to determine if this model was created with TF2 or TF1,
    # because outputs are ordered differently for TF2 and TF1 models
    outname = output_details[0]['name']

    if ('StatefulPartitionedCall' in outname): # This is a TF2 model
        boxes_idx, classes_idx, scores_idx = 1, 3, 0
    else: # This is a TF1 model
        boxes_idx, classes_idx, scores_idx = 0, 1, 2

    # Loop over every image and perform detection
    for image_path in images:

        # Load image and resize to expected shape [1xHxWx3]
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        imH, imW, _ = image.shape
        image_resized = cv2.resize(image_rgb, (width, height))
        input_data = np.expand_dims(image_resized, axis=0)

        # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
        if floating_model:
            input_data = (np.float32(input_data) - input_mean) / input_std

        # Perform the actual detection by running the model with the image as input
        interpreter.set_tensor(input_details[0]['index'],input_data)
        interpreter.invoke()

        # Retrieve detection results
        boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[0] # Bounding box coordinates of detected objects
        classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0] # Class index of detected objects
        scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0] # Confidence of detected objects

        detections = []

        # Loop over all detections and draw detection box if confidence is above minimum threshold
        centers = []
        for i in range(len(scores)):
            if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):

                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                ymin = int(max(1,(boxes[i][0] * imH)))
                xmin = int(max(1,(boxes[i][1] * imW)))
                ymax = int(min(imH,(boxes[i][2] * imH)))
                xmax = int(min(imW,(boxes[i][3] * imW)))

                cv2.rectangle(image, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)
                center_x = (xmin + xmax) // 2
                center_y = (ymin + ymax) // 2
                print(f'Found center of mug at: ({center_x} , {center_y} )')
                centers.append((center_x, center_y))
                # Draw label
                object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
                label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                cv2.rectangle(image, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                cv2.putText(image, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text

                detections.append([object_name, scores[i], xmin, ymin, xmax, ymax])

        # All the results have been drawn on the image, now display the image
        if show_results:
            cv2.imshow('Object detector', image)

            # Press any key to continue to next image, or press 'q' to quit
            if cv2.waitKey(0) == ord('q'):
                break

        # Save the labeled image to results folder if desired
        if save_results:

            # Get filenames and paths
            image_fn = os.path.basename(image_path)
            image_savepath = os.path.join(CWD_PATH,RESULTS_DIR,image_fn)

            base_fn, ext = os.path.splitext(image_fn)
            txt_result_fn = base_fn +'.txt'
            txt_savepath = os.path.join(CWD_PATH,RESULTS_DIR,txt_result_fn)

            # Save image
            cv2.imwrite(image_savepath, image)

            # Write results to text file
            # (Using format defined by https://github.com/Cartucho/mAP, which will make it easy to calculate mAP)
            with open(txt_savepath,'w') as f:
                for detection in detections:
                    f.write('%s %.4f %d %d %d %d\n' % (detection[0], detection[1], detection[2], detection[3], detection[4], detection[5]))
    with open('centers.pkl', 'wb') as file:
        pickle.dump(centers, file)
    # Clean up
    cv2.destroyAllWindows()
    return
