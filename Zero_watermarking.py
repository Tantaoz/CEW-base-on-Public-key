import sys
from osgeo import ogr
import numpy as np
import math
import cv2
import matplotlib.pyplot as plt

'''watermark processing'''


def Watermark_deal(img_deal):
    h, w = img_deal.shape
    for i in range(0, h):
        for j in range(0, w):
            if img_deal[i][j] < 100:
                img_deal[i][j] = 0
            else:
                img_deal[i][j] = 255
    return img_deal


'''Binarized watermark image'''


def Erzhi_watermark(Arnold_img):
    Erzhi_list = [y for x in Arnold_img for y in x]
    # Erzhi_list=Arnold_img.flatten()
    for i in range(0, len(Erzhi_list)):
        if Erzhi_list[i] == 255:
            Erzhi_list[i] = 1
        else:
            Erzhi_list[i] = 0
    return Erzhi_list


'''Scramble watermark'''


def Arnold_Encrypt(image):
    shuffle_times, a, b = 10, 1, 1
    arnold_image = np.zeros(shape=image.shape)
    h, w = image.shape
    N = h  # or N=w
    # 3：Traverse pixel coordinate transformation
    for time in range(shuffle_times):
        for ori_x in range(h):
            for ori_y in range(w):
                # According to the formula coordinate transformation
                new_x = (1 * ori_x + b * ori_y) % N
                new_y = (a * ori_x + (a * b + 1) * ori_y) % N
                arnold_image[new_x, new_y] = image[ori_x, ori_y]
    return arnold_image


'''Read in vector data (shp)'''


def Read_Shapfile(fn_ori):
    ds = ogr.Open(fn_ori, 0)
    if ds is None:
        sys.exit("Could not open {0}.".format(fn_ori))
    layer = ds.GetLayer(0)
    feature_num = layer.GetFeatureCount(0)
    X_Lst, Y_Lst = [], []
    for i in range(0, feature_num):
        feature = layer.GetFeature(i)
        geometry = feature.GetGeometryRef()
        if geometry.GetGeometryName() == 'POLYGON':
            geometry = geometry.GetGeometryRef(0)
        x, y = [0] * geometry.GetPointCount(), [0] * geometry.GetPointCount()
        for j in range(geometry.GetPointCount()):
            x[j] = geometry.GetX(j)
            y[j] = geometry.GetY(j)
        X_Lst.append(x), Y_Lst.append(y)
    ds.Destroy()
    return X_Lst, Y_Lst, feature_num


"""Feature matrix"""


def Construction(Xlist, feature_num, Lst_WaterMark):
    List_Fea = len(Lst_WaterMark) * [0]
    # Construct feature matrix through voting mechanism
    for i in range(0, feature_num):
        for j in range(i + 1, feature_num):
            Ni = len(Xlist[i])
            Nj = len(Xlist[j])
            ni = Ni % 2
            nj = Nj % 2
            index = (Ni * Nj) % len(Lst_WaterMark)  # watermark index
            if ni == nj:
                List_Fea[index] += 1
            else:
                List_Fea[index] += -1
    for p in range(0, len(List_Fea)):
        if List_Fea[p] > 0:
            List_Fea[p] = 255
        else:
            List_Fea[p] = 0
    return List_Fea


"""Construct zero watermark image"""


def XOR(List_Fea, Lst_WaterMark):
    List_Zero = len(Lst_WaterMark) * [0]
    for m in range(0, len(List_Zero)):
        if List_Fea[m] == Lst_WaterMark[m]:
            List_Zero[m] = 0
        else:
            List_Zero[m] = 255
    return List_Zero


if __name__ == '__main__':
    img = cv2.imread(r"D:\CEWcode\GISMAP.bmp", 0)  # Read watermarked image
    img_deal = Watermark_deal(img)  # Watermark image processing（0，255）
    Arnold_img = Arnold_Encrypt(img_deal)  # scramble image
    # Control shuffling times
    # for i in range(0, 9):
    #     Arnold_img = Arnold_Encrypt(Arnold_img)  # arnold_img置乱后水印
    Lst_WaterMark = Arnold_img.flatten()  # 降维
    fn_r = r"D:\CEWcode\Map\Boundaries.shp"
    XLst, YLst, feature_num = Read_Shapfile(fn_r)  # read raw vector data
    List_Fea = Construction(XLst, feature_num, Lst_WaterMark)
    List_Zero = XOR(List_Fea, Lst_WaterMark)
    Array_Z = np.array(List_Zero).reshape(int(math.sqrt(len(List_Zero))), int(math.sqrt(len(List_Zero))))
    # Store zero-watermarked images
    plt.subplot()
    plt.imshow(Array_Z, 'gray')
    plt.title("Zero_image")
    plt.show()
    cv2.imwrite("Zero_image.jpg", Array_Z)
