# -*- coding: utf-8 -*-

"""
手机测试的相关处理
V0.1 2021-3-4
添加获取连接电脑的手机adb号 ， 存为list
"""

import os, subprocess
from CommonUtils import get_date_now, get_date_time_style


def get_devices():
    """
    返回连接电脑手机的adb号列表
    :param self:
    :return:
    """
    lists = (os.popen('adb devices').read())
    devices = (lists.strip().split('\n'))
    devices_list = []
    for i in range(1, len(devices)):
        device = (devices[i].split('\t')[0])
        devices_list.append(device)
    return devices_list


def get_cap(path, device_id, ):
    """
    向指定目录传入手机截图
    :param path:
    :param device_id:
    :return:
    """
    adb_device_tmp = "adb -s" + device_id + " "
    pic_id = get_date_time_style() + ".png"
    try:
        subprocess.run(adb_device_tmp + "exec-out screencap -p > " + path + "/" + pic_id, shell=True)
    except Exception as err:
        return 0
    return 1


if __name__ == "__main__":
    print(get_date_now())
