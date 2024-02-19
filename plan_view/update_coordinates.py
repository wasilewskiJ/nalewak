def update_coordinates(x, y):
    new_y = (y - (y / 435 * 68)) * 1.48228882834
    new_x = (x + ((388 - x) / 448 * 60)) * 1.49226804124
    return new_x, new_y

