from transform import four_point_transform
import numpy as np
import cv2
import pickle

def transform_points(pts, M):
    """Transform points using the transformation matrix M."""
    transformed_pts = []
    for pt in pts:
        pt_array = np.array([pt[0], pt[1], 1]).reshape(-1, 1)
        transformed_pt = M.dot(pt_array)
        transformed_pt = transformed_pt / transformed_pt[2]
        transformed_pts.append((transformed_pt[0,0], transformed_pt[1,0]))
    return transformed_pts

def adjust_point(pt, max_width, max_height, threshold=55):
    """Adjust point to be within the image bounds."""
    x, y = int(pt[0]), int(pt[1])
    if x < 0:
        x = 0
    elif x >= max_width:
        x = max_width - 1

    if y < 0:
        y = 0
    elif y >= max_height:
        y = max_height - 1

    return (x, y)

#cords kolejnosc : lewo gora, prawo gora, prawo dol, lewo dol
def plan_view(image_path = './ready_img.png', additional_points_path = './centers.pkl',  cords = [(35, 178), (274,31), (533, 184), (291, 470)]):
    image = cv2.imread(image_path)
    pts = np.array(cords, dtype = "float32")

    # Apply the four point transform to obtain a "birds eye view" of the image
    warped, M = four_point_transform(image, pts)

    # Load additional points
    with open(additional_points_path, 'rb') as f:
        additional_points = pickle.load(f)

    # Transform additional points
    transformed_points = transform_points(additional_points, M)

    # Visualize the points on the warped image, adjust if necessary
    for pt in transformed_points:
        adjusted_pt = adjust_point(pt, warped.shape[1], warped.shape[0])
        cv2.circle(warped, adjusted_pt, 5, (0, 255, 0), -1)
        print(f'Srodek kubka po transformacji w: {pt}')
    # Save the warped image
    cv2.imwrite("projected.png", warped)

