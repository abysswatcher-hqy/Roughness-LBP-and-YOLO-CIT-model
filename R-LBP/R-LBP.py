import numpy as np
from scipy.ndimage import convolve


def calculate_cv(arr):
    mean = np.mean(arr)
    std_dev = np.std(arr)
    return std_dev / mean


def rlbp_encode(target_pixel, reference_pixels):
    cv_a = calculate_cv(reference_pixels)

    reference_pixels_with_target = np.append(reference_pixels, target_pixel)
    cv_b = calculate_cv(reference_pixels_with_target)

    if (cv_b - cv_a) > 0.15 * cv_a:
        return 1
    else:
        return 0


def apply_rlbp(image):
    height, width = image.shape
    result_image = np.zeros((height, width), dtype=np.uint8)

    # Apply R-LBP algorithm to each pixel in the image, excluding the image borders
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            target_pixel = image[i, j]
            reference_pixels = [
                image[i - 1, j - 1], image[i - 1, j], image[i - 1, j + 1],
                image[i, j + 1], image[i + 1, j + 1], image[i + 1, j],
                image[i + 1, j - 1], image[i, j - 1]
            ]

            binary_encoding = 0
            for k in range(8):
                binary_encoding += rlbp_encode(target_pixel, reference_pixels)

                # Rotate the reference pixels
                reference_pixels = reference_pixels[1:] + [reference_pixels[0]]

            # Convert binary encoding to decimal
            decimal_value = int(''.join(map(str, binary_encoding)), 2)

            result_image[i, j] = decimal_value

    return result_image


# Example usage:
# Assuming you have an image stored in a NumPy array called 'input_image'
processed_image = apply_rlbp(input_image)
