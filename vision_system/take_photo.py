import cv2
import os


def take_photo(DIR_PATH='./vision_system/', OUTPUT=False, OUTPUT_NAME='img.png'):
    
    OUTPUT_PATH = os.path.join(DIR_PATH, OUTPUT_NAME)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    ret, frame = cap.read()

    if OUTPUT:
        cv2.imwrite(image_path, frame)
    

    print("Photo taken")
    cap.release()
    cv2.destroyAllWindows()
    return frame
