import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np

img = cv.imread("1.JPG")

def lbp_basic(img):
    basic_array = np.zeros(img.shape, np.uint8)
    for i in range(1, basic_array.shape[0]-1):
        for j in range(1, basic_array.shape[1]-1):
            basic_array[i, j] = bin_to_decimal(cal_basic_lbp(img, i, j))
    return basic_array

def cal_basic_lbp(img, i, j):
    # 比中心像素大的点赋值为1，比中心像素小的赋值为0，返回得到的二进制序列
    sum = []
    if img[i - 1, j] > img[i, j]:
        sum.append(1)
    else:
        sum.append(0)
    if img[i - 1, j+1] > img[i, j]:
        sum.append(1)
    else:
        sum.append(0)
    if img[i, j + 1] > img[i, j]:
        sum.append(1)
    else:
        sum.append(0)
    if img[i + 1, j+1] > img[i, j]:
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

def bin_to_decimal(bin):
    # 二进制转十进制
    res = 0
    bit_num = 0  # 左移位数
    for i in bin[::-1]:
        res += i << bit_num   # 左移n位相当于乘以2的n次方
        bit_num += 1
    return res

def show_basic_hist(a):
    # 画原始lbp的直方图
    hist = cv.calcHist([a], [0], None, [256], [0, 256])
    hist = cv.normalize(hist, hist)
    plt.figure(figsize=(8, 4))
    plt.plot(hist, color='r')
    plt.xlim([0, 256])
    plt.show()

def save_image_with_filename(img, filename):
    # 根据文件名保存图像
    cv.imwrite(f"{filename}_result.png", img)

img1 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
basic_array = lbp_basic(img1)
show_basic_hist(basic_array)

plt.figure(figsize=(11, 11))
plt.subplot(1, 2, 1)
plt.imshow(img1)
plt.subplot(1, 2, 2)
plt.imshow(basic_array, cmap='Greys_r')
plt.show()

# 保存结果图像
save_image_with_filename(basic_array, "001_lbp_result")
