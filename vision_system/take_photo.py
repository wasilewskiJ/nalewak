import cv2
import os


def take_photo(DIR_PATH='./vision_system/', OUTPUT=False, OUTPUT_NAME='img.png'):
    """
    Capture and optionally save a photo using the system's default camera.

    Args:
        DIR_PATH (str): Directory to save the photo. Defaults to './vision_system/'.
        OUTPUT (bool): Whether to save the photo. Defaults to False.
        OUTPUT_NAME (str): Filename for the saved photo. Defaults to 'img.png'.

    Returns:
        The captured image frame.
    """
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
