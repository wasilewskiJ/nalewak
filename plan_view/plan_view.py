from .transform import four_point_transform
import numpy as np
import cv2
import pickle
import os


X_FACTOR = 1.35915493
Y_FACTOR = 1.346534653

def transform_points(pts, M):
    """Transform points using the transformation matrix M."""
    transformed_pts = []
    for pt in pts:
        pt_array = np.array([pt[0], pt[1], 1]).reshape(-1, 1)
        transformed_pt = M.dot(pt_array)
        transformed_pt = transformed_pt / transformed_pt[2]
        transformed_pts.append((transformed_pt[0, 0], transformed_pt[1, 0]))
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


def plan_view(image, DIR_PATH='./vision_system/plan_view/', CENTERS_NAME='centers.pkl', VERTICES_NAME='vertices.txt', OUTPUT=False, OUTPUT_NAME='plan_view.png'):
    CENTERS_PATH = os.path.join(DIR_PATH, CENTERS_NAME)
    VERTICES_PATH = os.path.join(DIR_PATH, VERTICES_NAME)
    OUTPUT_PATH = os.path.join(DIR_PATH, OUTPUT_NAME)

    with open(VERTICES_PATH) as f:
        pts = eval(f.readline())
    pts = np.array(pts, dtype="float32")

    # Apply the four point transform to obtain a "birds eye view" of the image
    warped, M = four_point_transform(image, pts)
    if OUTPUT:
        cv2.imwrite(OUTPUT_PATH, warped)

    #calculate centers of mugs after transformation
    with open(CENTERS_PATH, 'rb') as f:
        centers = pickle.load(f)
    transformed_pts = transform_points(centers, M)

    #we need to reverse axis and calculate real-coordinates
    physical_pts = []
    for pt in transformed_pts:
        transformed_pt = (pt[1] * X_FACTOR, pt[0] * Y_FACTOR)
        physical_pts.append((transformed_pt))
    print(f'SRODKI KUBKOW           : {physical_pts}')
