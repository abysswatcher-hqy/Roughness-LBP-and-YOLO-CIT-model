import cv2
import numpy as np


def calculate_average_difference(image, center_x, center_y, direction, pixel_count):
    height, width = image.shape
    differences = []

    directions = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1),
        "up_left": (-1, -1),
        "up_right": (-1, 1),
        "down_left": (1, -1),
        "down_right": (1, 1)
    }

    for dir_name, offset in directions.items():
        row, col = center_x, center_y
        values = []

        for _ in range(pixel_count):
            row += offset[0]
            col += offset[1]

            if 0 <= row < height and 0 <= col < width:
                values.append(image[row, col])

        if len(values) > 1:
            diff = np.abs(np.diff(values)).mean()
            differences.append(diff)

    return sum(differences)


def main():
    image_path = "stage4huidu.png"
    gray_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if gray_image is None:
        print("无法读取图像，请检查图像路径和文件是否存在。")
        return

    center_x, center_y = gray_image.shape[0] // 2, gray_image.shape[1] // 2
    pixel_count = 10

    x_points = np.linspace(0, gray_image.shape[0] - 1, 5, dtype=int)
    y_points = np.linspace(0, gray_image.shape[1] - 1, 5, dtype=int)

    total_differences = []

    for i in range(1, 4):
        for j in range(1, 4):
            point_x, point_y = x_points[i], y_points[j]

            total_diff = calculate_average_difference(gray_image, point_x, point_y, "all", pixel_count)
            total_differences.append(total_diff)

            print(f"点({point_x}, {point_y}) 每个方向均差的和: {total_diff}")

    average_diff = np.mean(total_differences)
    print(f"\n所有点每个方向均差的和的平均值: {average_diff}")


if __name__ == "__main__":
    main()
