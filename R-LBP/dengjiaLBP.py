import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np

# uniform_map为等价模式的58种特征值从小到大进行序列化编号得到的字典
uniform_map = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 6: 5, 7: 6, 8: 7, 12: 8,14: 9, 15: 10, 16: 11, 24: 12, 28: 13, 30: 14, 31: 15, 32: 16, 48: 17,
 56: 18, 60: 19, 62: 20, 63: 21, 64: 22, 96: 23, 112: 24,120: 25, 124: 26, 126: 27, 127: 28, 128: 29, 129: 30, 131: 31, 135: 32,143: 33,
 159: 34, 191: 35, 192: 36, 193: 37, 195: 38, 199: 39, 207: 40,223: 41, 224: 42, 225: 43, 227: 44, 231: 45, 239: 46, 240: 47, 241: 48,
243: 49, 247: 50, 248: 51, 249: 52, 251: 53, 252: 54, 253: 55, 254: 56,255: 57}
def cal_basic_lbp(img,i,j):#比中心像素大的点赋值为1，比中心像素小的赋值为0，返回得到的二进制序列
    sum = []
    if img[i - 1, j ] > img[i, j]:
        sum.append(1)
    else:
        sum.append(0)
    if img[i - 1, j+1 ] > img[i, j]:
        sum.append(1)
    else:
        sum.append(0)
    if img[i , j + 1] > img[i, j]:
        sum.append(1)
    else:
        sum.append(0)
    if img[i + 1, j+1 ] > img[i, j]:
        sum.append(1)
    else:
        sum.append(0)
    if img[i + 1, j ] > img[i, j]:
        sum.append(1)
    else:
        sum.append(0)
    if img[i + 1, j - 1] > img[i, j]:
        sum.append(1)
    else:
        sum.append(0)
    if img[i , j - 1] > img[i, j]:
        sum.append(1)
    else:
        sum.append(0)
    if img[i - 1, j - 1] > img[i, j]:
        sum.append(1)
    else:
        sum.append(0)
    return sum
def lbp_uniform(img):
    revolve_array = np.zeros(img.shape,np.uint8)
    width = img.shape[0]
    height = img.shape[1]
    for i in range(1,width-1):
        for j in range(1,height-1):
            sum_ = cal_basic_lbp(img,i,j) #获得二进制
            num_ = calc_sum(sum_)  #获得跳变次数
            if num_ <= 2:
                revolve_array[i,j] = uniform_map[bin_to_decimal(sum_)] #若跳变次数小于等于2，则将该二进制序列对应的十进制值就是邻域中心的LBP值，因为只有58种可能的值，但值得最大值可以是255，所以这里进行映射。
            else:
                revolve_array[i,j] = 58
    return revolve_array
def calc_sum(r):  # 获取值r的二进制中跳变次数
    sum_ = 0
    for i in range(0,len(r)-1):
        if(r[i] != r[i+1]):
            sum_ += 1
    return sum_
def show_uniform_hist(img_array):
    show_hist(img_array, [60], [0, 60])
def show_hist(img_array,im_bins,im_range):
    hist = cv.calcHist([img_array], [0], None, im_bins, im_range)
    hist = cv.normalize(hist, hist).flatten()
    plt.plot(hist, color='r')
    plt.xlim(im_range)
    plt.show()
def show_revolve_hist(img_array):
    show_hist(img_array, [36], [0, 36])

img = cv.imread("1.JPG")
uniform_array = lbp_uniform(img)
show_revolve_hist(uniform_array)
plt.imshow(uniform_array,cmap='Greys_r')
plt.show()
