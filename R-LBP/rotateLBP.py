import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np

# revolve_map为旋转不变模式的36种特征值从小到大进行序列化编号得到的字典
revolve_map = {0: 0, 1: 1, 3: 2, 5: 3, 7: 4, 9: 5, 11: 6, 13: 7, 15: 8, 17: 9, 19: 10, 21: 11, 23: 12, 25: 13, 27: 14,
               29: 15, 31: 16, 37: 17,
               39: 18, 43: 19, 45: 20, 47: 21, 51: 22, 53: 23, 55: 24, 59: 25, 61: 26, 63: 27, 85: 28, 87: 29, 91: 30,
               95: 31, 111: 32, 119: 33, 127: 34,
               255: 35}


def lbp_revolve(img):  # 图像旋转不变LBP特征
    revolve_array = np.zeros(img.shape, np.uint8)
    width = img.shape[0]
    height = img.shape[1]
    for i in range(1, width - 1):
        for j in range(1, height - 1):
            sum = cal_basic_lbp(img, i, j)
            revolve_key = get_min_for_revolve(sum)  # 得到各个旋转的LBP二进制串中的最小值
            revolve_array[i, j] = revolve_map[revolve_key]  # 将值范围映射到0~35
    return revolve_array


def cal_basic_lbp(img, i, j):  # 比中心像素大的点赋值为1，比中心像素小的赋值为0，返回得到的二进制序列
    sum = []
    if img[i - 1, j] > img[i, j]:
        sum.append(1)
    else:
        sum.append(0)
    if img[i - 1, j + 1] > img[i, j]:
        sum.append(1)
    else:
        sum.append(0)
    if img[i, j + 1] > img[i, j]:
        sum.append(1)
    else:
        sum.append(0)
    if img[i + 1, j + 1] > img[i, j]:
        sum.append(1)
    else:
        sum.append(0)
    if img[i + 1, j] > img[i, j]:
        sum.append(1)
    else:
        sum.append(0)
    if img[i + 1, j - 1] > img[i, j]:
        sum.append(1)
    else:
        sum.append(0)
    if img[i, j - 1] > img[i, j]:
        sum.append(1)
    else:
        sum.append(0)
    if img[i - 1, j - 1] > img[i, j]:
        sum.append(1)
    else:
        sum.append(0)
    return sum


def get_min_for_revolve(arr):  # 获取二进制序列进行不断环形旋转得到新的二进制序列的最小十进制值
    values = []  # 存放每次移位后的值，最后选择值最小那个
    circle = arr * 2  # 用于循环移位，分别计算其对应的十进制
    for i in range(0, 8):
        j = 0
        sum = 0
        bit_sum = 0
        while j < 8:
            sum += circle[i + j] << bit_sum
            bit_sum += 1
            j += 1
        values.append(sum)
    return min(values)


# 绘制图像旋转不变LBP特征的归一化统计直方图
def show_revolve_hist(img_array):
    show_hist(img_array, [36], [0, 36])


def show_hist(img_array, im_bins, im_range):
    hist = cv.calcHist([img_array], [0], None, im_bins, im_range)
    hist = cv.normalize(hist, hist).flatten()
    plt.plot(hist, color='r')
    plt.xlim(im_range)
    plt.show()


def save_image_with_filename(img, filename):
    # 根据文件名保存图像
    cv.imwrite(f"{filename}_result.png", img)


img = cv.imread("1.JPG")
img1 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
re_arr = lbp_revolve(img1)
show_revolve_hist(re_arr)
plt.imshow(re_arr, cmap='Greys_r')
plt.show()

# 保存结果图像
save_image_with_filename(re_arr, "001_lbp_revolve_result")
