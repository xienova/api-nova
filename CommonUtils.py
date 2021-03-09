__author__ = 'xiechunhui'
__date__ = '2020/12/15 17:48'

import datetime, time


def get_date_now():
    '''
    获取当前日期
    :return: 字符串
    '''
    return str(datetime.date.today())


def get_date_time_now():
    return str(datetime.datetime.now())[0:19]


def get_date_time_style():
    """
    获取特定格式：如2012-08-08_2021-08-08
    :return:
    """
    return time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))


def get_date_others(positive_negative):
    '''
    获取当前日期将来的n天(正); 当前日期过去的n天 (负)
    :param positive_negative:
    :return:字符串
    '''
    return str(datetime.date.today() + datetime.timedelta(days=positive_negative))


def get_date_time_others_zero(positive_negative):
    '''
    获取其他天零点
    :param positive_negative:
    :return:
    '''
    now = datetime.datetime.now()
    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond) + datetime.timedelta(days=positive_negative)
    return str(zero_today)


def get_date_time_others_last(positive_negative):
    '''
    获取其他天的最后一秒
    :param positive_negative:
    :return:
    '''
    now = datetime.datetime.now()
    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)
    last_day = zero_today + datetime.timedelta(hours=23, minutes=59, seconds=59) + datetime.timedelta(
        days=positive_negative)
    return str(last_day)


def get_length_list(list_use):
    return len(list_use)


if __name__ == "__main__":
    print(get_date_time_style())
    print(get_date_time_others_zero(-12))
