# -*- coding: utf-8 -*-

"""
图片的相关操作
V0.1 2021-3-9 14:48:41
打开图片，通过鼠标左右键选择坐标
"""

from PIL import Image  # 图像处理库，用于对比图片
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import numpy as np
import time
from bokeh.plotting import figure, show, output_file

from utils.CommonUtils import get_date_time_style


def select_pic(file_path, dir_template):
    """
    通过 matplot获取图片坐标使用，在django中无法使用，提示：RuntimeError: main thread is not in main loop
Tcl_AsyncDelete: async handler deleted by the wrong thread
    :param dir_template:
    :param file_path:
    :return:
    """

    dic_xy = {}

    # 当鼠标点击图片时，显示对应的坐标点
    def on_press(event):
        # 当左键单击时为1
        if event.button == 1:
            # 当为浮点数时：
            if isinstance(event.xdata, float):
                dic_xy['pic_1x'] = int(event.xdata)
                dic_xy['pic_1y'] = int(event.ydata)
        # 当右键单击时为3
        elif event.button == 3:
            # 当为浮点数时：
            if isinstance(event.xdata, float):
                dic_xy['pic_2x'] = int(event.xdata)
                dic_xy['pic_2y'] = int(event.ydata)
        else:
            pass

    def show_pic_box(pic_1x, pic_1y, pic_2x, pic_2y):
        """
        保存裁剪后的区域，并展示
        :param pic_1x:
        :param pic_1y:
        :param pic_2x:
        :param pic_2y:
        :return:
        """
        box_tmp = (pic_1x, pic_1y, pic_2x, pic_2y)
        im = Image.open(file_path)
        region = im.crop(box_tmp)
        region_path = dir_template + get_date_time_style() + "-box.png"
        region.save(region_path)
        time.sleep(0.5)

        # 将region保存后，打开之
        plt.figure("预览")
        region_tmp = Image.open(region_path)
        plt.imshow(region_tmp, animated=True)
        # show之后才可以显示
        plt.show()

    if file_path == "":
        pass
    else:
        img = mpimg.imread(file_path)
        plt.figure()
        plt.imshow(img)
        plt.show()
        show_pic_box(dic_xy['pic_1x'], dic_xy['pic_1y'], dic_xy['pic_2x'], dic_xy['pic_2y'])

    return dic_xy


def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    return cv_img


def opencv_xy(path, info):
    """
    通过点击图片，获取对应的坐标
    :param info:
    :param path:
    :return:
    """
    dic_xy = {}
    img = cv_imread(path)
    dic_xy['info'] = info
    dic_xy['pic_1x'] = 0
    dic_xy['pic_1y'] = 0
    dic_xy['pic_2x'] = 0
    dic_xy['pic_2y'] = 0

    def on_mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            xy = "%d,%d" % (x, y)
            dic_xy['pic_1x'] = x
            dic_xy['pic_1y'] = y
            cv2.circle(img, (x, y), 1, (255, 0, 0), thickness=-1)
            cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                        1.0, (0, 0, 0), thickness=1)
            cv2.imshow("image", img)
            print(type(x))
            print(dic_xy)

        if event == cv2.EVENT_RBUTTONDOWN:
            xy = "%d,%d" % (x, y)
            dic_xy['pic_2x'] = x
            dic_xy['pic_2y'] = y
            cv2.circle(img, (x, y), 1, (255, 0, 0), thickness=-1)
            cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                        1.0, (0, 0, 0), thickness=1)
            cv2.imshow("image", img)

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", on_mouse)
    cv2.imshow("image", img)

    while True:
        try:
            cv2.waitKey(100)
            break
        except Exception:
            cv2.destroyWindow("image")
            break

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return dic_xy


def opencv_imread_mini(path):
    """
    读取图像，支持 bmp、jpg、png、tiff 等常用格式
    :param path:
    :return:
    """
    img = cv2.imread(path)
    # 创建窗口并显示图像
    cv2.namedWindow("Image")
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    # 释放窗口
    cv2.destroyAllWindows()


if __name__ == "__main__":
    opencv_xy("D:/ON_OFF_TEST_DATA/dsf_fds_dsa/pic_template/2021-03-15_13-15-31_双卡.png")
