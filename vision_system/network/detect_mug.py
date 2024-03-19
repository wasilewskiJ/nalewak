import os
import cv2
import numpy as np
import sys
import glob
import importlib.util
import pickle



# Import TensorFlow libraries
pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime.interpreter import Interpreter
else:
    from tensorflow.lite.python.interpreter import Interpreter

def detect_objects(image, DIR_PATH='./vision_system/network/', MODEL_NAME='model', GRAPH_NAME='detect.tflite', LABELMAP_NAME='labelmap.txt', OUTPUT=True, OUTPUT_DIR='results', OUTPUT_NAME='img_network_result.png', CENTERS_OUTPUT_PATH='./vision_system/plan_view/centers.pkl', VERTICES_NAME='../plan_view/vertices.txt'):
    min_conf_threshold = 0.5
    show_results = False  # Change to true if want to show detection results

    if OUTPUT:
        OUTPUT_PATH = os.path.join(DIR_PATH, OUTPUT_DIR)
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)

    PATH_TO_CKPT = os.path.join(DIR_PATH, MODEL_NAME, GRAPH_NAME)

    PATH_TO_LABELS = os.path.join(DIR_PATH, MODEL_NAME, LABELMAP_NAME)
    with open(PATH_TO_LABELS, 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    # deleting first '???' label if present. (it's a mistake in the labelmap.txt file)
    if labels[0] == '???':
        del (labels[0])

    # loading tensorflowlite and alocate tensors
    interpreter = Interpreter(model_path=PATH_TO_CKPT)
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

    if ('StatefulPartitionedCall' in outname):  # This is a TF2 model
        boxes_idx, classes_idx, scores_idx = 1, 3, 0
    else:  # This is a TF1 model
        boxes_idx, classes_idx, scores_idx = 0, 1, 2
	    # Load image and resize to expected shape [1xHxWx3]
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imH, imW, _ = image.shape
    image_resized = cv2.resize(image_rgb, (width, height))
    input_data = np.expand_dims(image_resized, axis=0)

    # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Retrieve detection results
    boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[
        0]  # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[classes_idx]['index'])[
        0]  # Class index of detected objects
    scores = interpreter.get_tensor(output_details[scores_idx]['index'])[
        0]  # Confidence of detected objects

    detections = []


    VERTICES_PATH = os.path.join(DIR_PATH, VERTICES_NAME)

    with open(VERTICES_PATH) as f:
        pts = eval(f.readline())
    pts = np.array(pts, dtype="float32")

    # Loop over all detections and draw detection box if confidence is above minimum threshold
    centers = []
    for i in range(len(scores)):
        if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):

            # Get bounding box coordinates and draw box
            # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
            ymin = int(max(1, (boxes[i][0] * imH)))
            xmin = int(max(1, (boxes[i][1] * imW)))
            ymax = int(min(imH, (boxes[i][2] * imH)))
            xmax = int(min(imW, (boxes[i][3] * imW)))

            cv2.rectangle(image_rgb, (xmin, ymin),
                            (xmax, ymax), (10, 255, 0), 2)
            
            # Searching for mug/cup center based on location in photo
            center_x = (xmin + xmax) // 2
            center_y = (ymin + ymax) // 2
            height = ymax - ymin
            width = xmax - xmin
            cup_center_y = int(center_y + height / 3.1 * (imH - center_y + 100) / imH)
            cup_center_x = int(center_x + width / 2 * (imW/2 - center_x) / imW)

            # Check if the center of the mug is inside the area of interest
            if cv2.pointPolygonTest(pts, (cup_center_x, cup_center_y), False) < 0:
                print(f'Center of mug at: ({cup_center_x} , {cup_center_y} ) is outside the area of interest')
                continue

            # Draw circle in the center of mug
            cv2.circle(image_rgb, (cup_center_x, cup_center_y), 3, (0, 0, 255), -1)

            print(f'Found center of mug at: ({cup_center_x} , {cup_center_y} )')
            centers.append((cup_center_x, cup_center_y))
            # Draw label
            # Look up object name from "labels" array using class index
            object_name = labels[int(classes[i])]
            label = '%s: %d%%' % (object_name, int(
                scores[i]*100))  # Example: 'person: 72%'
            labelSize, baseLine = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)  # Get font size
            # Make sure not to draw label too close to top of window
            label_ymin = max(ymin, labelSize[1] + 10)
            # Draw white box to put label text in
            cv2.rectangle(image_rgb, (xmin, label_ymin-labelSize[1]-10), (
                xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED)
            cv2.putText(image_rgb, label, (xmin, label_ymin-7),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)  # Draw label text

            detections.append(
                [object_name, scores[i], xmin, ymin, xmax, ymax])

    # All the results have been drawn on the image, now display the image
    if show_results:
        cv2.imshow('Object detector', image_rgb)

        # Press any key to continue to next image, or press 'q' to quit
        if cv2.waitKey(0) == ord('q'):
            exit()

    # Save the labeled image to results folder if desired
    if OUTPUT:

        # Get filenames and paths
        image_savepath = os.path.join(DIR_PATH, OUTPUT_DIR, OUTPUT_NAME)

        base_fn, ext = os.path.splitext(OUTPUT_NAME)
        txt_result_fn = base_fn + '.txt'
        txt_savepath = os.path.join(DIR_PATH, OUTPUT_DIR, txt_result_fn)

        # Save image
        cv2.imwrite(image_savepath, image_rgb)

        # Write results to text file
        # (Using format defined by https://github.com/Cartucho/mAP, which will make it easy to calculate mAP)
        with open(txt_savepath, 'w') as f:
            for detection in detections:
                f.write('%s %.4f %d %d %d %d\n' % (
                    detection[0], detection[1], detection[2], detection[3], detection[4], detection[5]))
    with open(CENTERS_OUTPUT_PATH, 'wb') as file:
        pickle.dump(centers, file)
        print(f'Recognized centers saved at{CENTERS_OUTPUT_PATH}')
    # Clean up
    cv2.destroyAllWindows()
    return
