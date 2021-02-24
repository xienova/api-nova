__author__ = 'xiechunhui'
__date__ = '2020/12/22 14:02'


import re

def bool_version_6(version_str):
    '''
    根据版本字符串，获取版本是否为6开头，为6开头则说明是量产版本；
    :param version_str:
    :return:
    '''
    pattern = re.compile(r'.+\.6\..+')                  # . 匹配>=1;
    if pattern.match(version_str) == None:
        return False
    else:
        return True

if __name__ == '__main__':
    version_try = '【HNR320T.6【黑白水墨屏】量产验证版本】N1761.0.01.19.00(20201216)'
    print(bool_version_6(version_try))