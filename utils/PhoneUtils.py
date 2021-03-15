# -*- coding: utf-8 -*-

"""
手机测试的相关处理
V0.1 2021-3-4
添加获取连接电脑的手机adb号 ， 存为list
"""

import os, subprocess
from utils.CommonUtils import get_date_time_style
from utils.PicUtils import opencv_xy


def get_devices():
    """
    返回连接电脑手机的adb号列表
    :return:
    """
    lists = (os.popen('adb devices').read())
    devices = (lists.strip().split('\n'))
    devices_list = []
    for i in range(1, len(devices)):
        device = (devices[i].split('\t')[0])
        devices_list.append(device)
    return devices_list


def get_cap(path, device_adb, info):
    """
    向指定目录传入手机截图
    :param info: 是双卡，还是通讯录
    :param device_adb:
    :param path:
    :return:成功返回1， 失败返回0
    """
    adb_device_tmp = "adb -s" + device_adb + " "
    pic_id = get_date_time_style() + "_" + info + ".png"
    pic_path = path + "/" + pic_id
    try:
        os.system(adb_device_tmp + "exec-out screencap -p > " + pic_path)
    except Exception as err:
        return 0
    return pic_path


def get_cap_xy(path, device_adb, info):
    """
    生成截图后，打开截图，获取坐标
    :param info: 是双卡，还是通讯录
    :param device_adb:
    :param path:
    :return:成功返回dic坐标， 失败返回0
    """
    adb_device_tmp = "adb -s" + device_adb + " "
    pic_id = get_date_time_style() + "_" + info + ".png"
    pic_path = path + "/" + pic_id
    try:
        os.system(adb_device_tmp + "exec-out screencap -p > " + pic_path)
    except Exception as err:
        return 0    # 截图有问题时，返回0
    result = opencv_xy(pic_path)
    return result



if __name__ == "__main__":
    pass
