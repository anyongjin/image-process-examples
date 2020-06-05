#  idea from :https://github.com/bornreddy/smart-thresholds/blob/master/otsu.py

import numpy as np
from PIL import Image

def histogramify(image):
    img_arr = np.array(image, dtype=np.int)
    img_histogram = np.histogram(img_arr, range(0, 257))
    return img_histogram


def get_otsu_threshold(image):
    '''
    使用otsu方法得到图片的二值化最佳阈值
    :param image:
    :return:
    '''
    image = image.convert('L')
    hist = histogramify(image)
    total = image.size[0] * image.size[1]
    current_max, threshold = 0, 0
    sumT, sumF, sumB = 0, 0, 0
    for i in range(0, 256):
        sumT += i * hist[0][i]
    weightB, weightF = 0, 0
    for i in range(0, 256):
        weightB += hist[0][i]
        weightF = total - weightB
        if weightF == 0:
            break
        sumB += i * hist[0][i]
        sumF = sumT - sumB
        meanB = sumB / weightB
        meanF = sumF / weightF
        varBetween = weightB * weightF
        varBetween *= (meanB - meanF) * (meanB - meanF)
        if varBetween > current_max:
            current_max = varBetween
            threshold = i
    return threshold

def binary_img(image, gray_thres):
    image = image.convert('L')
    look_tbl = [0] * (gray_thres - 1) + [1] * (256 - gray_thres + 1)
    return image.point(look_tbl, '1')

if __name__ == '__main__':
    img = Image.open('img1.jpg')
    # get the best threshold using otsu
    thres = get_otsu_threshold(img)
    gray_img = binary_img(img, thres)
    gray_img.save('img_gray.jpg')
