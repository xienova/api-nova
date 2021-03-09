# -*- coding: utf-8 -*-
"""
二次封装Xlwings操作excel表的函数，打开，读，写等过程
打开：增加如果已经打开的文件，不再打开，关闭的时候也不关闭。

v0.50 lijiajiang 2021-02-03
    1) 重新整合优化显示方面的处理，优化log输出
    2) 增加精确获取excel非空的行/列表，包括制定列/行的最大行/列
v0.31  lijiajiang 2020-09-18
    1）修改第一次赋值默认sheet页的流程，检查sheet页是否存在
    2）优化内部处理流程
v0.30 lijiajiang 2020-08-26
    1）打开文件时，同步设置默认sheet页
    2）增加写入超链接的功能
v0.20 修改注释相关内容
v0.10 实现 Excel 打开/关闭文件，读/写 单元格/区域，删除行/列 等基本功能
"""

import os
import Component.LogUtils as LogUtils
import xlwings as xw


class ExcelXlwAPI(object):
    app = None
    wb = None  # 保存book的信息
    dft_sh = ''  # 默认的sheet表
    file_path = ''  # 文件全路径
    auto_open = False  # 保存是否通过python打开的文件，还是用户手动打开的文件

    def __init__(self, visible=False):
        """
        初始化，默认为不显示界面
        """
        self.app = xw.App(visible=visible, add_book=False)
        # 禁用显示及提示，加快处理速度
        self.set_display_mode(visible)

    def __del__(self):
        """
        对象删除时，恢复显示及提示处理
        如果文件通过程序自动打开，则再自动关闭
        :return:
        """
        if self.app is None:
            return

        if self.auto_open and self.wb is not None:
            LogUtils.debug_print(f"File {self.file_path} opened by Python, begin to close... ", 5)
            self.wb.close()
            self.wb = None

        try:
            self.app.display_alerts = True
            self.app.screen_updating = True
            self.app.quit()
        except Exception as err:
            LogUtils.error_print(err)
        self.app = None

    def set_display_mode(self, display_mode=False):
        self.app.display_alerts = display_mode
        self.app.screen_updating = display_mode

    def open_file(self, file_path):
        """
        打开文件
        先检查需要打开的文件当前是否已经打开，
            若已打开，则获取句柄。置为不需要程序自动关闭
            若未打开，则判断文件是否存在，置为需要程序自动关闭
                若已存在：则打开文件，置为需要程序自动关闭
        :param file_path:具体的文件全路径
        # :param sht_name:设置本地保存的默认sheet页，默认为空
        :return: True：文件已经被打开  False： 文件打开失败
        """

        self.wb = None
        try:
            cnt = xw.books.count
            if cnt > 0:
                for idx in range(xw.books.count):
                    """
                    此处只判定文件名，不判定全路径，由于路径可能使用'\\'或者'/'
                    路径上字母可能大小写，都会导致识别失败。
                    """
                    if os.path.basename(xw.books[idx].fullname).lower() == os.path.basename(file_path).lower():
                        self.wb = xw.books[idx]
                        LogUtils.debug_print(f"The file '{file_path}' has been opened！", 5)
                        return True
        except AttributeError:
            LogUtils.debug_print(f"The file '{file_path}' has not been opened！", 5)

        if os.path.exists(file_path):
            try:
                self.wb = self.app.books.open(file_path)
                return self.wb is not None
            except Exception as err:
                LogUtils.debug_print(f"The file '{file_path}' open failed':{err}")
        else:
            LogUtils.debug_print(f"{file_path} not exist!")

        return False

    def set_default_sheet(self, sht_name):
        """
        设置默认需要操作的sheet页，对于部分操作一般会在一个sheet页操作时比较有用
        :param sht_name: sheet页的名称
        :return:True：设置成功，False：设置失败
        """
        if self.wb == '':
            LogUtils.debug_print(f"No file opened by python")
            return False

        for idx in range(self.wb.sheets.count):
            if self.wb.sheets[idx].name == sht_name:
                self.dft_sh = sht_name
                return True

        LogUtils.debug_print(f"File '{self.file_path}' has no '{sht_name}' sheet")
        return False

    @staticmethod
    def get_active_workbook():
        """
        获取当前激活的excel文件的全路径文件名
        :return:文件名
        """
        active_book = None
        try:
            active_book = xw.books.active.fullname
        except Exception as err:
            LogUtils.debug_print(f"not find active book:{err}", 5)
        return active_book

    @staticmethod
    def get_active_sheet():
        """
        获取当前激活的excel文件的激活的sheet表
        :return:
        """
        active_sheet = None
        try:
            active_sheet = xw.sheets.active.name
        except Exception as err:
            LogUtils.debug_print(f"not find active sheet:{err}")
        return active_sheet

    def save_file(self):
        """
        强制保存文件
        :return: None
        """
        self.wb.save()

    def close_file(self, save_wb=True, force_close=False):
        """
        关闭文件，默认保存，如果强制关闭，则不论是否程序自动打开，都关闭文件
        :param save_wb: 是否保存，默认保存
        :param force_close:默认不强制关闭（非程序打开的也关闭），
        :return:无
        """
        if save_wb:
            self.wb.save()
        if force_close:
            self.wb.close()
            self.wb = None
            return

        if not self.auto_open:
            LogUtils.debug_print(f"文件： {self.file_path} 不是程序自动打开，不自动关闭，待用户手动关闭！")
            self.wb = None
            return

        LogUtils.debug_print(f"关闭Excel文件:{self.file_path}")
        self.wb.close()
        self.wb = None

    def create_file(self, file_path):
        """
        创建excel表，并保存在指定路径
        :param file_path:需要保存的文件的全路径
        :return:
        """
        self.wb = self.app.books.add()
        self.wb.save(file_path)
        self.auto_open = True

    def get_op_sheet(self, sht_name=''):
        """
        获取需要操作的sheet的变量
        :param sht_name:sheet的名称，如果未空则为之前设置的默认名称
        :return:成功返回指定值，不成功则返回空
        """
        if sht_name == '':
            sht_name = self.dft_sh

        try:
            return self.wb.sheets[sht_name]
        except Exception as err:
            LogUtils.debug_print(f"Try get file {self.file_path} no '{sht_name}' error={err}!")
            return ''

    def add_sheet(self, sht_name):
        """
        新增sheet页，如果已经存在，则不需要处理
        :param sht_name:sheet页名称，没有检查是否特殊的字符串
        :return:True：添加sheets成功或不需要添加，False：添加不成功
        """
        if sht_name == '':
            return False
        # TODO： 后续增加在哪一个sheet页后面添加
        for idx in range(self.wb.sheets.count):
            if self.wb.sheets[idx].name == sht_name:
                return True

        return xw.sheets.add(name=sht_name, after=self.wb.sheets.count)

    def read_cell(self, sht_name, row, col):
        """
        读取指定单元格的内容
        :param sht_name: sheet页名称
        :param row: 行号
        :param col: 列号
        :return:返回的值，读取出错，返货None
        """
        try:
            return self.get_op_sheet(sht_name).range(row, col).value
        except AttributeError:
            LogUtils.debug_print(f"read cell error, sheet = {sht_name} ,row = {row}, col = {col} error!")
            return None

    def read_range(self, sht_name, row, col, row_e=-1, col_e=-1):
        """
        读取指定区域的内容
        结束行 -1：表示选择最后一行
        结束列 -1：表示选择最后一列
        :param sht_name:sheet页名称
        :param row:开始行号
        :param col:开始的列号
        :param row_e:结束的行号，为-1时，获取最大行
        :param col_e:结束的列号，为-1时，获取最大列
        :return:返回读取的值
        """
        if row_e == -1:
            row_e = max(self.get_max_row(sht_name), row)
        if col_e == -1:
            col_e = max(self.get_max_col(sht_name), col)
        try:
            return self.get_op_sheet(sht_name).range((row, col), (row_e, col_e)).options(transpot=True).value
        except AttributeError:
            LogUtils.debug_print(f"read range error! sheet = {sht_name} ,"
                                 f"row = {row}, col = {col} ,row_end = {row_e}, col_end = {col_e} error!")
            return None

    def read_range_list(self, sht_name, row, col, row_e, col_e):
        """
        强制读取必须返回list格式，通过多读取两行的方式，保证读取的是list，然后返回值中再去掉2行数据
        :param sht_name:sheet页名称
        :param row:开始行号
        :param col:开始的列号
        :param row_e:结束的行号，为-1时，获取最大行
        :param col_e:结束的列号，为-1时，获取最大列
        :return:返回读取的值
        """
        if row_e == -1:
            row_e = max(self.get_max_row(sht_name), row)+2
        else:
            row_e += 2
        if col_e == -1:
            col_e = max(self.get_max_col(sht_name), col)
        try:
            info_list = self.get_op_sheet(sht_name).range((row, col), (row_e, col_e)).options(transpot=True).value
            return info_list[:-2]
        except AttributeError:
            LogUtils.debug_print(f"read range error! sheet = {sht_name} ,"
                                 f"row = {row}, col = {col} ,row_end = {row_e}, col_end = {col_e} error!")
            return None

    def write_cell(self, sht_name, row, col, value):
        """
        写指定单元格的内容
        :param sht_name: sheet页名称
        :param row: 行号
        :param col: 列号
        :param value: 具体的值
        :return: True：成功，False：失败
        """
        try:
            self.get_op_sheet(sht_name).range(row, col).value = value
            return True
        except AttributeError:
            LogUtils.debug_print(f"write cell error! sheet = {sht_name} ,row = {row}, col = {col} error!")
            return False

    def write_hyperlink(self, sht_name, row, col, hyperlink, disp):
        """
        写指定单元格的内容
        :param sht_name: sheet页名称
        :param row: 行号
        :param col: 列号
        :param hyperlink: 超链接的地址
        :param disp: 显示的内容
        :return: True：成功，False：失败
        """
        try:
            self.get_op_sheet(sht_name).range(row, col).add_hyperlink(hyperlink, disp)
            return True
        except AttributeError:
            LogUtils.debug_print(f"write cell error! sheet = {sht_name} ,row = {row}, col = {col} error!")
            return False

    def write_range(self, sht_name, row, col, value):
        """
        写指定区域的内容，数组以一行内容为第二维数据
        :param sht_name: sheet页名称
        :param row: 行号
        :param col: 列号
        :param value:具体值
        :return:True：成功，False：失败
        """
        try:
            self.get_op_sheet(sht_name).range(row, col).options(expand='table').value = value
            return True
        except AttributeError:
            LogUtils.debug_print(f"write range error! sheet = {sht_name} ,"
                                 f"row = {row}, col = {col} error! \nvalue:{value}")
            return False

    def write_range_formula(self, sht_name, row, col, row_e, col_e, form):
        """
        写指定区域的内容为公式
        :param sht_name:sheet页名称
        :param row:开始行号
        :param col:开始的列号
        :param row_e:结束的行号，为-1时，获取最大行
        :param col_e:结束的列号，为-1时，获取最大列
        :param form:公式的内容
        :return:True：成功，False：失败
        """
        if row_e == -1:
            row_e = max(self.get_max_row(sht_name), row)
        if col_e == -1:
            col_e = max(self.get_max_col(sht_name), col)
        try:
            self.get_op_sheet(sht_name).range((row, col), (row_e, col_e)).formula = form
            return True
        except AttributeError:
            LogUtils.debug_print(f"write range error! sheet = {sht_name} ,"
                                 f"row = {row}, col = {col} error! \nform:{form}")
            return False

    def write_col_range(self, sht_name, row, col, value):
        """
        写指定区域的内容，数组以一列内容为第二维数据
        :param sht_name: sheet页名称
        :param row: 行号
        :param col: 列号
        :param value:具体的值
        :return:True：成功，False：失败
        """
        try:
            self.get_op_sheet(sht_name).range(row, col).options(transpose=True, expand='table').value = value
            return True
        except AttributeError:
            LogUtils.debug_print(f"write col range error! sheet = {sht_name} ,"
                                 f"row = {row}, col = {col} error! \nvalue:{value}")
            return False

    def get_sheets(self):
        """
        获取sheets列表
        :return:sheets列表
        """
        sh_list = list()
        for idx in range(self.wb.sheets.count):
            sh_list.append(self.wb.sheets[idx].name)
        return sh_list

    def sheet_rename(self, old_name, new_name):
        """
        更改sheet表名称
        :param old_name:原sheet表名称
        :param new_name:新sheet表名称
        :return:
        """
        try:
            self.get_op_sheet(old_name).name = new_name
        except AttributeError:
            LogUtils.debug_print(f"sheet_rename error, old_name = {old_name}, new_name = {new_name}!")
            return False

    def insert_row(self, sht_name, row, cnt=1):
        """
        插入行
        :param sht_name:sheet页名称
        :param row:需要在哪一行前面插入行
        :param cnt:插入的行数
        :return:True：成功，False：失败
        """

        if cnt < 1:
            print(f"cnt:{cnt} <1, no need insert")
            return False

        row_e = row + cnt - 1
        try:
            self.get_op_sheet(sht_name).api.Rows(str(row) + ':' + str(row_e)).Insert()
            return True
        except AttributeError:
            LogUtils.debug_print(f"insert_row error! sheet = {sht_name} ,row = {row} cnt ={cnt}!")
            return False

    def del_row(self, sht_name, row, cnt=-1):
        """
        删除行
        :param sht_name:sheet页名称
        :param row:删除的起始行
        :param cnt:删除的行数，-1表示删除从row开始到结束的所有行
        :return:True：成功，False：失败
        """
        if row < 1:
            LogUtils.debug_print(f"{row} <1 return")
            return False

        if cnt == -1:
            row_e = max(self.get_max_row(sht_name), row)
        else:
            row_e = row+cnt-1

        if row > row_e:
            tmp = row
            row = row_e
            row_e = tmp

        try:
            self.get_op_sheet(sht_name).range((row, 1), (row_e, 1)).api.EntireRow.Delete()
            return True
        except AttributeError:
            LogUtils.debug_print(f"del_row error! sheet = {sht_name} ,row = {row}  row_e ={row_e}!")
            return False

    def insert_col(self, sht_name, col, cnt=1):
        """
        插入列
        :param sht_name:sheet页名称
        :param col:在哪一列后面插入
        :param cnt:插入多少列
        :return:True：成功，False：失败
        """

        if cnt < 1:
            print(f"cnt:{cnt} <1, no need insert")
            return False

        col_e = col + cnt - 1
        try:
            self.get_op_sheet(sht_name).api.Rows(str(col) + ':' + str(col_e)).Insert()
            return True
        except AttributeError:
            LogUtils.debug_print(f"insert_col error! sheet = {sht_name} ,col = {col} cnt ={cnt}!")
            return False

    def del_col(self, sht_name, col, cnt=-1):
        """
        删除列
        :return:
        :param sht_name:sheet页名称
        :param col:删除的；；列数
        :param cnt:删除的列数，-1表示删除从col开始到结束的所有列
        :return:True：成功，False：失败
        """
        if col < 1:
            print(f"{col} <1 return")
            return False

        if cnt == -1:
            col_e = max(self.get_max_row(sht_name), col)
        else:
            col_e = col + cnt - 1

        if col > col_e:
            tmp = col
            col = col_e
            col_e = tmp

        try:
            self.get_op_sheet(sht_name).range((col, 1), (col_e, 1)).api.EntireColumn.Delete()
            return True
        except AttributeError:
            LogUtils.debug_print(f"del_row error! sheet = {sht_name} ,row = {col}  row_e ={col_e}!")
            return False

    def get_max_row_accurate(self, sht_name='', col=-1):
        """
        精确获取当前excel sheet页非空的最大行号（只是边框格式不计算）
        :param sht_name:sheet页名称
        :param col:指定特定的列的最大行，默认为所有列的最大行
        :return:最大的行数
        """
        act_sh = self.get_op_sheet(sht_name)
        row_max = act_sh.used_range.last_cell.row
        if col == -1:
            col_begin = 1
            col_end = act_sh.used_range.last_cell.column
        else:
            col_begin = col
            col_end = col

        # 从最后一行找到非空单元格则返回
        for row_idx in range(row_max, 0, -1):
            for col_idx in range(col_begin, col_end+1, 1):
                if act_sh.range(row_idx, col_idx).value is not None:
                    return row_idx

        # 全空，返回-1
        return -1

    def get_max_col_accurate(self, sht_name='', row=-1):
        """
        获取当前excel sheet页的非空最大列数（只是边框格式不计算）
        :param sht_name:sheet页名称
        :param row:指定特定的行的最大列，默认为所有行的最大列
        :return:最大列数
        """
        act_sh = self.get_op_sheet(sht_name)
        col_max = act_sh.used_range.last_cell.row
        if row == -1:
            row_begin = 1
            row_end = act_sh.used_range.last_cell.column
        else:
            row_begin = row
            row_end = row

        # 从最后一列向前，找到内容不为空的单元格的列号
        for col_idx in range(col_max, 0, -1):
            for row_idx in range(row_begin, row_end+1, 1):
                if act_sh.range(row_idx, col_idx).value is not None:
                    return col_idx

        # 全空，返回-1
        return -1

    def get_max_row(self, sht_name=''):
        """
        获取当前excel sheet也的最大行号
        :param sht_name:sheet页名称
        :return:最大的行数
        """
        try:
            return self.get_op_sheet(sht_name).used_range.last_cell.row
        except AttributeError:
            print(f"read sheet{sht_name} used_range.last_cell.row error!")
            return -1

    def get_max_col(self, sht_name=''):
        """
        获取当前excel sheet也的最大列数
        :param sht_name:sheet页名称
        :return:最大列数
        """
        try:
            return self.get_op_sheet(sht_name).used_range.last_cell.column
        except AttributeError:
            LogUtils.debug_print(f"read sheet{sht_name} used_range.last_cell.column error!")
            return -1
