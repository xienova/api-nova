# -*- coding: utf-8 -*-
"""
uiautomator命令处理
v0.10 lijiajiang 2021-02-24
    1) 封装最基础的uiautomator命令
"""

import uiautomator2 as u2
import time
import Component.LogUtils as LogUtils
from typing import Optional

MAX_CNT = 120

APP_ACTION_WAIT = 2


class UiautomatorAPI(object):
    dev = None
    phone_id = None

    def ph_connect(self, ph_id):
        try:
            self.dev = u2.connect(ph_id)
            self.phone_id = ph_id
            LogUtils.debug_print(self.dev.info)

            return True
        except Exception as error:
            LogUtils.debug_print(error)
        return False

    def stop_app(self, app_name):
        try:
            self.dev.app_stop(app_name)
            time.sleep(APP_ACTION_WAIT)
            return True
        except Exception as error:
            LogUtils.debug_print(error)
        return False

    def start_app(self, package_name: str, activity: Optional[str] = None, wait: bool = False,
                  stop: bool = False, use_monkey: bool = False):
        try:
            if package_name is None or package_name == '':
                return False
            if self.dev.info['currentPackageName'] == package_name:
                return True
            self.dev.app_start(package_name, activity, wait, stop, use_monkey)
            return True
        except Exception as error:
            LogUtils.debug_print(error)
        return False

    def pinch_in(self, percent=20, steps=100):
        try:

            LogUtils.info_print(f"缩小{percent}", 4)
            self.dev().pinch_in(percent=percent, steps=steps)
            return True
        except Exception as error:
            LogUtils.debug_print(error)
        return False

    def pinch_out(self, percent=30, steps=100):
        try:
            LogUtils.info_print(f"放大{percent}", 4)
            self.dev().pinch_out(percent=percent, steps=steps)
            return True
        except Exception as error:
            LogUtils.debug_print(error)
        return False

    def press_home(self):
        try:
            # 点击back
            self.dev.press("home")
            # 点击提示框
            # self.dev.click(0.443, 0.673)
            return True
        except Exception as error:
            LogUtils.debug_print(error)
        return False

    def press_back(self):
        try:
            # 点击back
            self.dev.press("back")
            # 点击提示框
            self.dev.click(0.443, 0.673)
            return True
        except Exception as error:
            LogUtils.debug_print(error)
        return False

    def click(self, pos):
        try:
            self.dev.click(pos[0], pos[1])
            return True
        except Exception as error:
            LogUtils.debug_print(error)
        return False

    def long_click(self, pos, duration: float = 3):
        try:
            self.dev.long_click(pos[0], pos[1], duration)
            return True
        except Exception as error:
            LogUtils.debug_print(error)
        return False

    def double_click(self, click_pos: [], duration=0.05):
        try:
            self.dev.double_click(click_pos[0], click_pos[1], duration)
            return True
        except Exception as error:
            LogUtils.debug_print(error)
        return False

    def screen_shot(self, file_path):
        try:
            self.dev.screenshot(file_path)
            return True
        except Exception as error:
            LogUtils.debug_print(error)
        return False

    def swipe(self, fx, fy, tx, ty):
        try:
            self.dev.swipe(fx, fy, tx, ty)
            return True
        except Exception as error:
            LogUtils.debug_print(error)
        return False

    def dual_finger_swipe(self, pos1, pos2, pos3, pos4):
        self.dev().gesture(pos1, pos2, pos3, pos4, steps=100)
        return True

    def drag(self, fx, fy, tx, ty):
        try:
            self.dev.drag(fx, fy, tx, ty)
            return True
        except Exception as error:
            LogUtils.debug_print(error)
        return False

    def screen_off(self):
        try:
            self.dev.screen_off()
            return True
        except Exception as err:
            LogUtils.debug_print(err)
        return False

    def screen_on(self):
        try:
            self.dev.screen_on()
            return True
        except Exception as err:
            LogUtils.debug_print(err)
        return False
