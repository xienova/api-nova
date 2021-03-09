# -*- coding: utf-8 -*-

"""
完成文件相关的处理
v0.1 初始处理 2021-3-5 17:05:18
"""

import os
import shutil
import time


def rmdir(path):
    """
    删除目录，同时删除目录下的文件夹和文件
    :param path: 文件目录
    :return: None
    """
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    is_exist = os.path.exists(path)

    if not is_exist:
        return

    try:
        shutil.rmtree(path)
    except Exception as err:
        pass


def mkdir(path, reset=False):
    """
    创建文件夹
    :param path:文件夹路径
    :param reset:如果存在，需要先删除
    :return:
    """
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\").rstrip('/')

    # 需要复位，则先删除
    if reset:
        try:
            rmdir(path)
            time.sleep(1)
            os.makedirs(path)
        except Exception as err:
            pass
        return

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    is_exist = os.path.exists(path)

    # 判断结果
    if not is_exist:
        # 如果不存在则创建目录
        # 创建目录操作函数
        try:
            os.makedirs(path)
        except Exception as err:
            return -1
        return 1
    else:
        return 0
