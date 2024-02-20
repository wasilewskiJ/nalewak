import cv2
import os


def take_photo(image_path='img.png'):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    ret, frame = cap.read()

    cv2.imwrite(image_path, frame)
    print("Photo saved as img.png")
    cap.release()
    cv2.destroyAllWindows()
    return
