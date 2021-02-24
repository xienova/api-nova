__author__ = 'xiechunhui'
__date__ = '2020/12/28 15:07'

# 需要安装：
# pip install opencv-python
# pip install opencv-contrib-python

import cv2


def opencvTest(target, template):
    '''
    :param target: 目标图片
    :param template: 区域图片
    :return:opencv操作后得到的分值； 这里1为最大值；0为最小值；测试时0.8以上算为匹配成功
    '''
    # 读取目标图片,必须进入到目标目录使用;  这样可以防止中文路径
    # os.chdir(QtForm.path_use)

    target_ = cv2.imread(target)
    template_ = cv2.imread(template)

    # 执行模板匹配，采用的匹配方式cv2.TM_CCOEFF_NORMED
    result = cv2.matchTemplate(target_, template_, cv2.TM_CCOEFF_NORMED)
    # 寻找矩阵（一维数组当做向量，用Mat定义）中的最大值和最小值的匹配结果及其位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # 打印出当前的值
    return max_val

if __name__ == '__main__':
    target = "target.jpg"
    template = "template.jpg"
    score = opencvTest(target,template)
    print(score)