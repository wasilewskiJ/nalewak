import cv2
import pickle

def correct_photo(image_path='./img.png', calibration_file='./correct/dist_pickle.p', output_path='./corrected_img.png'):
    """
    Correct the distortion in an image using calibration parameters.

    Parameters:
    - image_path: Path to the image to be corrected.
    - calibration_file: Path to the pickle file containing calibration parameters.
    - output_path: Path where the corrected image will be saved.
    """
    # Check if the calibration file exists and load the calibration parameters
    try:
        with open(calibration_file, 'rb') as f:
            calibration_params = pickle.load(f)
        mtx = calibration_params['mtx']
        dist = calibration_params['dist']
    except FileNotFoundError:
        print(f"Calibration file {calibration_file} not found.")
        return

    # Try to load the image
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Image {image_path} not found.")
    except FileNotFoundError as e:
        print(e)
        return

    # Correct the distortion
    undistorted_img = cv2.undistort(img, mtx, dist, None, mtx)

    # Save the corrected image
    cv2.imwrite(output_path, undistorted_img)
    print(f"Image has been corrected and saved as '{output_path}'.")

# If you want to test the function directly, uncomment the line below
# correct_photo()
