import cv2
import numpy as np
# 计算序列跳变次数

# 证明旋转不变等价LBP模式只有9种
arr1 = []
P = 8
def cal_cnt(Str):
    cnt = 0 # 用来存放跳变次数的变量
    for i in range(1, len(Str)):
        if Str[i-1] != Str[i]: # 如果有变化，计数加1，如果跳变次数为0,1,2就归为等价模式，大于2归为混合模式
            cnt += 1

    return cnt

for i in range(pow(2, P)):
    seq = bin(i)[2:].rjust(P, '0')  # 二进制化
    cnt = cal_cnt(seq)  # 计算该P位二进制数的跳变次数
    if cnt <= 2:
        # 旋转不变性
        Min = int(seq, 2)  # 转换为十进制数
        for j in range(len(seq)):
            t = seq[j::] + seq[:j]
            # print(t, int(t, 2))
            Min = min(int(t, 2), Min)

        if Min not in arr1:
            arr1.append(Min)




# 旋转不变的等价LBP
def uniform_rotation_LBP(img, R, P):  # 参数: 原始图像img，半径R，采样点个数P
    h, w = img.shape
    img_LBP = np.zeros(img.shape, dtype=img.dtype)
    for row in range(R, h - R):
        for col in range(R, w - R):
            LBP_str = []
            for p in range(P):  # 遍历全部采样点
                # 计算采样点的坐标(浮点数)
                x_p = row + R * np.cos(2 * np.pi * p / P)
                y_p = col + R * np.sin(2 * np.pi * p / P)
                # print(x_p, y_p)

                x_1 = int(np.floor(x_p))
                y_1 = int(np.floor(y_p))  # floor是向下取整
                x_2 = min(x_1 + 1, h - 1)
                y_2 = min(y_1 + 1, w - 1)  # 防止超出原图的尺寸

                # 双线性插值求出这个采样点的像素值
                value0 = (x_2 - x_p) * img[x_1, y_1] + (x_p - x_1) * img[x_2, y_1]
                value1 = (x_2 - x_p) * img[x_1, y_2] + (x_p - x_1) * img[x_2, y_2,]
                temp = int((y_2 - y_p) * value0 + (y_p - y_1) * value1)

                # 与窗口中心坐标的像素值进行比较
                if temp >= img[row, col]:
                    LBP_str.append(1)
                else:
                    LBP_str.append(0)

            # print(LBP_str)
            LBP_str = ''.join('%s' % id for id in LBP_str)
            # print(LBP_str, int(LBP_str, 2))

            # 等价LBP
            count = cal_cnt(LBP_str)  # 计算跳变次数
            if count > 2:
                # 如果变化次数大于2，则该点的LBP值就为 P(P-1)+2，P=8时便是58，被归为混合模式类
                img_LBP[row, col] = P * (P - 1) + 2
            else:  # 符合等价模型
                # 旋转不变性
                Min = int(LBP_str, 2)  # 转换为十进制数
                for i in range(len(LBP_str)):
                    t = LBP_str[i::] + LBP_str[:i]
                    # print(t, int(t, 2))
                    Min = min(int(t, 2), Min)

                img_LBP[row, col] = arr1.index(Min)  # 查表找到该值的索引，便是该点的LBP值

    return img_LBP

lena = cv2.imread('../1.JPG')

gray = cv2.cvtColor(lena,cv2.COLOR_RGB2GRAY)
x = uniform_rotation_LBP(gray, 2, 8)

cv2.imwrite("1xzbbLBPresult.jpg",x)
cv2.waitKey(0)