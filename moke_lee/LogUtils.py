# -*- coding: utf-8 -*-

"""
Log的相关处理
v0.30 lijiajiang 2021-02-03
    1）对于Log增加线程ID打印
v0.21 lijiajiang 2020-09-18
    1）增加disp函数
v0.20 lijiajiang 2020-08-26
    1）将Log输出更改为error/warning/info 3种类型，
v0.10 实现 Excel 打开/关闭文件，读/写 单元格/区域，删除行/列 等基本功能
"""

import datetime
from threading import currentThread


# 默认打印的消息级别
DebugInfoLv = 3
ThreadInfo = False
output_function = None


def set_output_function(func):
    """
    保存输入的需要调用的函数
    :param func:
    :return:
    """
    global output_function
    output_function = func


def set_default_lv(lv=3, thread_info=False):
    """
    设置默认的log级别
    :param lv:新的级别，默认为3
    :param thread_info: 是否需要输出thread id信息，在多线程处理时有用
    :return:无
    """
    global DebugInfoLv
    global ThreadInfo
    DebugInfoLv = lv
    ThreadInfo = thread_info


def time_print(tag, content, lv=-1):
    """
    基于时间显示输出的Log
    :param tag:
    :param content:
    :param lv:
    :return:
    """
    info = f"{str(datetime.datetime.now())[11:19]}: "
    global ThreadInfo
    global DebugInfoLv
    if ThreadInfo:
        info += f"{currentThread().ident} "

    if tag != '':
        info += f"{tag}! "

    info += f"{content}"

    if lv > DebugInfoLv+1:
        return

    if lv > DebugInfoLv:
        print(info)
        return

    print(info)
    # 是否有输出函数
    global output_function
    if output_function is not None:
        output_function(info)


def debug_print(content, lv=4):
    """
    增加时间信息的打印
    :param content:需要log输出的内容
    :param lv:需要log输出的级别
    :return: 无
    """
    time_print('', content, lv)


def info_print(content, lv=DebugInfoLv):
    """
    增加时间信息的打印
    :param content:需要log输出的内容
    :param lv:Log的级别，低于默认级别的才输出log
    :return: 无
    """
    time_print('', content, lv)


def error_print(content=''):
    """
    增加时间信息的打印
    :param content:需要error log输出的内容
    :return: 无
    """
    time_print('Error', content)


def warning_print(content=''):
    """
    增加时间信息的打印
    :param content:需要error log输出的内容
    :return: 无
    """
    time_print('Warning', content)


def display_print(content=''):
    """
    增加时间信息的打印
    :param content:需要error log输出的内容
    :return: 无
    """
    time_print('', content)
