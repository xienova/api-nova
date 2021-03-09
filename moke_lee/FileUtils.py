# -*- coding: utf-8 -*-

"""

完成文件相关的处理

v0.32 lijiajiang 2020-09-18
    1）增加读取配置文件的options的功能
v0.31 lijiajiang 2020-09-15
    1）修改创建文件是，判断是否有文件夹才创建文件，否则不创建文件夹
    2）修改配置文件的读写，将特殊的base64编码剥离
v0.20 lijiajiang 2020-08-26
    1）增加读写配置文件的功能（ini格式），使用 configparser
    2）将密码base64加密的文件使用ini文件格式，
v0.1 初始处理
"""

import os
import shutil
import configparser  # ini文件解析
from win32api import SetFileAttributes, GetFileAttributes
import Component.LogUtils as LogUtils
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
        LogUtils.debug_print(f"{path} 不存在，无需删除")
        return

    try:
        # os.rmdir(path)
        shutil.rmtree(path)
    except Exception as err:
        LogUtils.error_print(err)


def remove_file(file):
    if not is_file_exists(file):
        LogUtils.debug_print(f"file: {file} not exist", 5)
        return
    os.remove(file)


def rename_file(src_file, dst_file):
    if not is_file_exists(src_file):
        LogUtils.error_print(f"file: {src_file} not exist")
        return False
    remove_file(dst_file)
    os.rename(src_file, dst_file)
    return True


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
            LogUtils.info_print(f"{path} 创建成功!", 5)
        except Exception as err:
            LogUtils.error_print(err)
        return

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    is_exist = os.path.exists(path)

    # 判断结果
    if not is_exist:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        LogUtils.info_print(f" {path} 创建成功!", 5)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        LogUtils.debug_print(f" {path} 目录已存在!", 5)
        return False


def is_file_exists(filename):
    """
    判断文件是否存在
    :param filename:文件名
    :return: boolean，True：存在，False：不存在
    """
    return os.path.isfile(filename)


def create_file(file_path):
    """
    创建文件，如果不存在，则创建，如果没有文件夹，也创建文件夹
    :param file_path:文件全路径
    :return:无
    """

    parent_path = os.path.dirname(file_path)

    if not os.path.isdir(parent_path):  # 无文件夹时创建
        os.makedirs(parent_path)

    if not is_file_exists(file_path):  # 无文件时创建
        fd = open(file_path, mode="w", encoding="utf-8-sig")
        fd.close()


def get_file_attr(file_path):
    """
    获取文件/文件夹属性
    :param file_path:
    :return:
    """
    # attr = win32api.GetFileAttributes(file_path)
    attr = GetFileAttributes(file_path)
    return attr


def set_file_attr(file_path, attr):
    """
    设置文件的属性
    :param file_path:文件/文件夹路径
    :param attr: 具体的属性
        FILE_ATTRIBUTE_READONLY = 1 (0x1)  # 属性-只读
        FILE_ATTRIBUTE_HIDDEN = 2 (0x2)   # 属性-隐藏
        FILE_ATTRIBUTE_SYSTEM = 4 (0x4)   # 属性-系统文件
        FILE_ATTRIBUTE_DIRECTORY = 16 (0x10)
        FILE_ATTRIBUTE_ARCHIVE = 32 (0x20)
        FILE_ATTRIBUTE_NORMAL = 128 (0x80)   # 属性-正常
        FILE_ATTRIBUTE_TEMPORARY = 256 (0x100)
        FILE_ATTRIBUTE_SPARSE_FILE = 512 (0x200)
        FILE_ATTRIBUTE_REPARSE_POINT = 1024 (0x400)
        FILE_ATTRIBUTE_COMPRESSED = 2048 (0x800)
        FILE_ATTRIBUTE_OFFLINE = 4096 (0x1000)
        FILE_ATTRIBUTE_NOT_CONTENT_INDEXED = 8192 (0x2000)
        FILE_ATTRIBUTE_ENCRYPTED = 16384 (0x4000)
    :return:无
    """
    # win32api.SetFileAttributes(file_path, attr)
    SetFileAttributes(file_path, attr)


def write_file(file, info, write_mode='w+', encode='utf-8-sig'):
    """
    写txt文件
    :param file:文件路径
    :param info:写入内容
    :param write_mode:写入模式，默认增量写入
    :param encode:编码模式，默认utf8,代码编码
    :return:无
    """
    with open(file, write_mode, encoding=encode) as fd:
        fd.writelines(info)


def config_write_data(file, section, option, value: str, reset=False):
    # 先创建文件（如果文件存在，则不修改）
    create_file(file)

    parser = configparser.ConfigParser()
    if not reset:  # 先读取原有的配置，否则写的时候会直接将原内容清空
        parser.read(file, encoding="utf-8-sig")

    if section not in parser.sections():
        try:
            # 增加Section，如果原来有section ，则不会可能返回错误
            parser.add_section(section)
        except Exception as err:
            LogUtils.info_print(f"write config file:{file}, section={section},option={option},result:{err}")

    if option != '':
        try:
            # 写入value
            parser.set(section, option, value)

        except Exception as err:
            LogUtils.error_print(f"write config file:{file}, section={section},option={option},result:{err}")
            return False

    with open(file, "w+", encoding="utf-8-sig") as fd:
        parser.write(fd)
    return True


def config_read_data(file, section, option):
    """
    获取配置文件中的内容
    :param file:文件路径
    :param section:在配置文件中的章节
    :param option:在配置的文件中option名称
    :return:
    """
    if not os.path.isfile(file):  # 无文件时，返回空
        LogUtils.warning_print(f"no file,{file}")
        return ''

    parser = configparser.ConfigParser()

    LogUtils.info_print(f"read cfg file = {file}, section = {section}, option = {option}", 4)
    parser.read(file, encoding="utf-8-sig")
    raw_data = ''
    try:
        raw_data = parser.get(section=section, option=option)
    except Exception as err:
        LogUtils.error_print(f"get config file:{file}, section={section},option={option},result:{err}")
    return raw_data


def config_read_sections(file):
    """
    获取配置某个Fields下的全部Sections
    :param file:文件路径
    :return: sections
    """
    section_list = []
    if not os.path.isfile(file):  # 无文件时，返回空
        LogUtils.error_print(f"config_read_sections, no file{file}")
        return section_list

    parser = configparser.ConfigParser()
    parser.read(file, encoding="utf-8-sig")
    section_list = parser.sections()
    return section_list


def config_read_options(file, section):
    """
    获取配置某个Fields下的全部Options
    :param file:文件路径
    :param section:在配置文件中的章节
    :return: list 该section下的所有章节
    """
    option_list = []
    if not os.path.isfile(file):  # 无文件时，返回空
        LogUtils.error_print(f"no file: {file}")
        return option_list

    parser = configparser.ConfigParser()

    LogUtils.info_print(f"read cfg file = {file}, section = {section}", 4)
    parser.read(file, encoding="utf-8-sig")
    
    try:
        option_list = parser.options(section=section)
    except Exception as err:
        LogUtils.error_print(f"get config file:{file}, section:{section},result:{err}")
    return option_list


def walk_folder_files(home_path, suffix='.png'):
    file_list = []
    for root, dirs, files in os.walk(home_path):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            if not f.endswith(suffix):
                continue
            file_list.append(os.path.join(root, f))

    return file_list
