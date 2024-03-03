import cv2 
import pickle
import os


def correct_photo(img, DIR_PATH='./vision_system/correct', CALIBRATOR_NAME='dist_pickle.p', OUTPUT=False,  OUTPUT_NAME='corrected_img.png'):
    """ 
    Correct the distortion in an image using calibration parameters.
    """
    CALIBRATION_PATH = os.path.join(DIR_PATH, CALIBRATOR_NAME)
    OUTPUT_PATH = os.path.join(DIR_PATH, OUTPUT_NAME)

	 
    # Check if the calibration file exists and load the calibration parameters
    try:
        with open(CALIBRATION_PATH, 'rb') as f:
            calibration_params = pickle.load(f)
        mtx = calibration_params['mtx']
        dist = calibration_params['dist']
    except FileNotFoundError:
        print(f"Calibration file {CALIBRATION_PATH} not found.")
        return

	
	#check if image exists
    try:
        if img is None:
            raise FileNotFoundError(f"Image for distortion correction hasn't been found.")
    except FileNotFoundError as e:
        print(e)
        return

	
    # Correct the distortion
    undistorted_img = cv2.undistort(img, mtx, dist, None, mtx)


    # Save the corrected image if asked
    if OUTPUT:
    	cv2.imwrite(OUTPUT_PATH, undistorted_img)
    
	
    print(f"Image has been corrected.")
    return undistorted_img
