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


def plan_view(image_path='../ready_img.png', centers_path='./centers.pkl'):
	image = cv2.imread(image_path)
	with open('./vertices.txt') as f:
		pts = eval(f.readline())
	pts = np.array(pts, dtype="float32")

    # Apply the four point transform to obtain a "birds eye view" of the image
	warped, M = four_point_transform(image, pts)
	cv2.imwrite('../rzucik.png', warped)
	
	#calculate centers of mugs after transformation
	with open(centers_path, 'rb') as f:
		centers = pickle.load(f)
	transformed_pts = transform_points(centers, M)
	
	#we need to reverse axis and calculate real-coordinates
	print(transformed_pts)
	physical_pts = []
	for pt in transformed_pts:
		physical_pts.append((pt[1] * X_FACTOR, pt[0] * Y_FACTOR))
	print(f'srodki: {physical_pts}')
