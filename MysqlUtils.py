__author__ = 'xiechunhui'
__date__ = '2020/12/22 14:03'

import pymysql

# 打开数据库 此为JIRA问题库
def find_data_dic_2args(sql,arg1,arg2):
    '''
    通过传入两个参数，获取sql语句的检索结果
    :param sql:
    :param arg1:
    :param arg2:
    :return:
    '''
    config = {
        "host":"10.18.203.84",
        "user":"jiraview",
        "password":"viewjira",
        "database":"jiradb",
        "charset":"utf8",
    }
    db = pymysql.connect(**config)

    # 创建游标
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

    # 操作数据库
    cursor.execute(sql,(arg1,arg2))
    res = cursor.fetchall()
    return res

    # 关闭数据库连接
    cursor.close()
    db.close()

def find_data_dic_0args(sql):
    config = {
        "host":"10.18.203.84",
        "user":"jiraview",
        "password":"viewjira",
        "database":"jiradb",
        "charset":"utf8",
    }
    db = pymysql.connect(**config)

    # 创建游标
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

    # 操作数据库
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

    # 关闭数据库连接
    cursor.close()
    db.close()



if __name__ == '__main__':
    # sql = "select * from users_dep"
    sql1 = "select issueid from changegroup where ID in (select groupid from changeitem where OLDSTRING='Open' and \
           NEWSTRING='Resolved') and CREATED between '2020-12-01 10:00:00' and '2020-12-01 23:59:59'"
    a = find_data_dic_0args(sql1)
    print(a)
    # print(type(a[0]['issueid']))

