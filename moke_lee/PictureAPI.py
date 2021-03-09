# -*- coding: utf-8 -*-
"""
脚本命令处理
v0.10 lijiajiang 2021-02-24
    1) 实现基于图片识别的命令封装，可以实现基本的图片比较，基于dist的图片比较等
"""

import cv2
import numpy as np
import os
import Component.LogUtils as LogUtils
import Component.FileUtils as FileUtils

from PIL import Image
import math
import operator
from functools import reduce


scale = 1


class PictureAPI(object):

    def multi_dst_single_result(self, src_file, dst_list=None, threshold=0.7):
        if not dst_list or not self._check_file(src_file):
            return None

        for file in dst_list:
            if not file.endswith('png'):  # 非图片，跳过
                continue
            if not FileUtils.is_file_exists(file):
                LogUtils.warning_print(f"dst file:{file} not exist!")
                continue
            pos = self.compare(src_file, file, threshold)
            if pos is None:
                continue
            return pos

    @staticmethod
    def image_contrast(img1, img2):
        image1 = Image.open(img1)
        image2 = Image.open(img2)

        h1 = image1.histogram()
        h2 = image2.histogram()

        result = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
        if result == 0.0:
            return True
        return False

    @staticmethod
    def _check_file(file_path):
        if file_path is None:
            return False
        if os.path.exists(file_path):
            return True
        return False

    @staticmethod
    def _find_base_pt(t_pos, cmp_size):
        sx = (t_pos[0] - cmp_size[0]/2) % cmp_size[0]
        sy = (t_pos[1] - cmp_size[1]/2) % cmp_size[1]
        if sx >= cmp_size[0] / 2 and sy >= cmp_size[1] / 2:
            sx -= cmp_size[0] / 2
            sy -= cmp_size[1] / 2
        return [sx, sy]

    def region_compare(self, src_file, box, dst_file, threshold=0.7):
        """
        在原图片的指定区域查找是否存在目标图片，并记录相同的位置的中心
        :param src_file:源文件
        :param box:源文件的指定区域
        :param dst_file:目标文件
        :param threshold:门限值
        :return:
        """
        src_path = os.path.dirname(src_file)
        tmp_file = src_path + '/tmp.png'
        # 将文件指定区域裁剪为新的文件
        im = Image.open(src_file)  # 用PIL打开一个图片
        ng = im.crop(box)  # 对im进行裁剪 保存为ng(这里im保持不变)
        ng.save(tmp_file)
        center_pt = self.compare(tmp_file, dst_file, threshold)
        os.remove(tmp_file)
        return center_pt

    def compare(self, src_file='', dst_file='', threshold=0.7):
        """
        比较图片
        :param src_file: 大图需要查找的图片内容
        :param dst_file:  小图，
        :param threshold: 门限
        :return:
        """

        if not FileUtils.is_file_exists(src_file) or not FileUtils.is_file_exists(dst_file):
            return None
        try:
            src_pic_data = self.read_file(src_file)
            dst_pic_data = self.read_file(dst_file)
            dst_pic_size = dst_pic_data.shape[:2]

            # 使用彩色进行比较
            point = self._compare(src_pic_data, dst_pic_data, threshold, False)
            if point is None:
                return None

            # 图片的长宽倒置
            center_pt = [point[0] + dst_pic_size[1]/2, point[1] + dst_pic_size[0]/2]
            LogUtils.info_print(f"图片：{os.path.basename(src_file)}找到图片{os.path.basename(dst_file)}，位置：{center_pt}", 5)
            return center_pt
        except Exception as err:
            LogUtils.debug_print(f"compare src pic：{src_file} and dst pic： {dst_file}error: {err}", 5)
        return None

    @staticmethod
    def get_pic_size(file):
        try:
            pic_data = cv2.imread(file)
            return pic_data.shape[:2]
        except Exception as err:
            print(err)
        return None

    @staticmethod
    def create_rgb_hist(t_img):
        h, w, c = t_img.shape
        # 创建一个（16*16*16,1）的初始矩阵，作为直方图矩阵
        # 16*16*16的意思为三通道每通道有16个bins
        rgb_hist = np.zeros([16 * 16 * 16, 1], np.float32)
        bsize = 256 / 16
        for row in range(h):
            for col in range(w):
                b = t_img[row, col, 0]
                g = t_img[row, col, 1]
                r = t_img[row, col, 2]
                # 人为构建直方图矩阵的索引，该索引是通过每一个像素点的三通道值进行构建
                index = int(b / bsize) * 16 * 16 + int(g / bsize) * 16 + int(r / bsize)
                # 该处形成的矩阵即为直方图矩阵
                rgb_hist[int(index), 0] += 1
        # plt.ylim([0, 10000])
        # plt.grid(color='r', linestyle='--', linewidth=0.5, alpha=0.3)
        return rgb_hist

    def hist_compare(self, src, dst, threshold=0.6):
        src_data = self.read_file(src)
        dst_data = self.read_file(dst)
        """直方图比较函数"""
        # 创建第一幅图的rgb三通道直方图（直方图矩阵）

        hist1 = self.create_rgb_hist(src_data)
        # 创建第二幅图的rgb三通道直方图（直方图矩阵）
        hist2 = self.create_rgb_hist(dst_data)
        # 进行三种方式的直方图比较
        match1 = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
        if match1 < threshold:
            result = True
        else:
            result = False
        return result
        # print(f"{os.path.basename(src)}:{os.path.basename(dst)}:{result}")

    @staticmethod
    def _compare(src_data, dst_data, threshold=0.7, gray_mode=True):
        if gray_mode:
            # 使用灰度图像中的坐标对原始RGB图像进行标记
            img_gray = cv2.cvtColor(src_data, cv2.COLOR_BGR2GRAY)
            template_ = cv2.cvtColor(dst_data, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(img_gray, template_, cv2.TM_CCOEFF_NORMED)
        else:
            result = cv2.matchTemplate(src_data, dst_data, cv2.TM_CCOEFF_NORMED)

        loc = np.where(result >= threshold)

        point = ()
        for pt in zip(*loc[::-1]):
            point = pt
        if point == ():
            return None
        return point

    @staticmethod
    def read_file(file_path):
        pic = cv2.imread(file_path)  # 读取图片
        return pic

    @staticmethod
    def cut_sub_region(src_file, box, dst_file):
        try:
            if src_file is None or dst_file is None or box is None:
                LogUtils.warning_print(f"裁剪原文件：{src_file} 图片区域：{box} ,目标文件：{dst_file}异常.")
                return False
            # FileUtils.mkdir(os.path.dirname(dst_file))
            im = Image.open(src_file)  # 用PIL打开一个图片
            ng = im.crop(box)  # 对im进行裁剪 保存为ng(这里im保持不变)
            ng.save(dst_file)
            return True
        except Exception as error:
            LogUtils.error_print(f"裁剪 {os.path.basename(src_file)} 图片box={box} 异常，{error}")
        return False
