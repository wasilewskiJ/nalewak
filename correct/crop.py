import cv2 
import os

def crop_photo(img, DIR_PATH='./vision_system/correct', OUTPUT=False, OUTPUT_NAME='ready_img.png'):
    
    OUTPUT_PATH = os.path.join(DIR_PATH, OUTPUT_NAME) 
    
    # Amount of pixels to crop: [top, bottom, left, right]
    crop_pixels = [330, 200, 710, 590]
    # Load the image
    if img is None:
        print(f"Cannot load image for cropping")
        return

    # Image dimensions
    h, w = img.shape[:2]

    # Crop the image
    cropped_img = img[crop_pixels[0]:h - crop_pixels[1], crop_pixels[2]:w - crop_pixels[3]]

    # Save the cropped image if asked
    if OUTPUT:
    	cv2.imwrite(output_path, cropped_img)
    
    print(f"Cropped image correctly")

    return cropped_img


