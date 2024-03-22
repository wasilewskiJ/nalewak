#This script isn't used by default in project. You can use it to order vertices of rectangle.
import numpy as np


def order_points(pts):
    """
    Orders the vertices of a rectangle given as a list of (X, Y) tuples.
    The function arranges the vertices in the following order: top-left, top-right, bottom-right, bottom-left.
    
    The ordered points are saved to a 'vertices.txt' file in the './plan_view/' directory, formatted
    specifically for use in other parts of the system, such as 'plan_view.py'.

    Args:
        pts (list of tuples): List of four (X, Y) tuples representing the vertices of a rectangle.
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


if __name__ == "__main__":
    CORDS = [(309, 503), (577, 200), (32, 179), (292, 26)] #type here your cords
    pts = np.array(CORDS, dtype="float32")
    order_points(pts)
