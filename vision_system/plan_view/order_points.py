import numpy as np


def order_points(pts):
    """Orders vertices of rectangle. 
    Takes in list of (X,Y) tuples.
    Writes result to vertices.txt file.
    """
    pts = np.array(pts, dtype="float32")

    # Sort by Y-axis (2 lowest Y points == top)
    sorted_pts = pts[np.argsort(pts[:, 1])]
    top = sorted_pts[:2]
    bottom = sorted_pts[2:]

    # Sort by X-axis (2 lowest X points == left)
    top = top[np.argsort(top[:, 0])]
    bottom = bottom[np.argsort(bottom[:, 0])]
	
	#saves coordinates in such order:
	#top left, top right, bottom right, bottom left
	#plan_view.py requires such an order
    with open('./plan_view/vertices.txt', 'w+') as file:
        file.write(
            f'[({top[0][0]}, {top[0][1]}), ({top[1][0]}, {top[1][1]}), ({bottom[1][0]}, {bottom[1][1]}), ({bottom[0][0]}, {bottom[0][1]})]\n')

    return


CORDS = [(309 , 503), (577 , 200), (32 , 179), (292,26)] 
pts = np.array(CORDS, dtype="float32")
order_points(pts)
