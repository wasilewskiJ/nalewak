import cv2


def crop_photo(image_path='./corrected_img.png', output_path='../ready_img.png'):
    # Paths for input and output images

    # Pixels to crop: [top, bottom, left, right]
    crop_pixels = [330, 200, 710, 590]  # Example values

    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Cannot load image from {image_path}")
        return

    # Image dimensions
    h, w = img.shape[:2]

    # Crop the image
    cropped_img = img[crop_pixels[0]:h - crop_pixels[1],
                      crop_pixels[2]:w - crop_pixels[3]]

    # Save the cropped image
    cv2.imwrite(output_path, cropped_img)
    print(f"Cropped image saved as {output_path}")


if __name__ == "__main__":
    crop_photo()
