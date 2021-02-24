import os
import traceback  # 上传附件使用

from jira import JIRA  # JIRA工具使用

import CommonUtils
import MysqlUtils
import ReUtils


# 类：创建jira task使用
class JiraQesTool:

    def __init__(self, user, password):
        self.server = 'http://dmtjira.hisense.com/'
        self.basic_auth = (user, password)
        self.jira_client = None

    def login(self):
        self.jira_client = JIRA(server=self.server, basic_auth=self.basic_auth)
        if self.jira_client != None:
            return True
        else:
            return False

    def create_issue(self, key, issue_type, summary, assignee, reporter, info_dict=None):
        '''

        :param key:
        :param issue_type:
        :param assignee:
        :param info_dict:
        :return:
        '''

        if info_dict is None:
            info_dict = {}
        issue_dict = {
            'project': {'key': key},
            'issuetype': {'name': issue_type},
            'summary': summary,
            'assignee': {'name': assignee},
            'reporter': {'name': reporter},
        }
        issue_dict.update(info_dict)

        if self.jira_client == None:
            self.login()
        return self.jira_client.create_issue(issue_dict)

    def create_sjzlgl_issue(self, summary, product_model, description, priority, source, duedate, probability, assignee,
                            reporter,
                            key='SJZLGL', issue_type='SW Bug',
                            product_line='内销', develop_class='自研'):

        # SJZLGL库需要的字段
        info_dict = {
            'customfield_10002': product_model,
            'description': description,
            'priority': {'name': priority},
            'customfield_19200': {'value': source},
            'duedate': duedate,
            'customfield_10109': {'value': product_line},  # 产品线：内销
            'customfield_10110': {'value': develop_class},  # 开发级别：自研
            'customfield_10005': {'value': probability},  # 概率是什么
        }
        if self.jira_client == None:
            self.login()
        return self.create_issue(key, issue_type, summary, assignee, reporter, info_dict)

    def get_all_prj(self):
        '''
        获取所有的项目
        :return:
        '''
        return self.jira_client.projects()

    def get_one_prj(self, prj_key):
        '''
        根据key获取此项目
        :return:
        '''
        return self.jira_client.project(prj_key)

    def get_issue(self, issue_key):
        '''
        根据issue_key获取issue信息
        :param issue_key:
        :return:
        '''
        return self.jira_client.issue(issue_key)

    def get_issue_resolutiondate(self, issue_key):
        '''
        根据issue_key获取resolution更新的日期，此日期为 closed的日期，也就是解决日期
        :param issue_key:
        :return:
        '''
        # return self.get_issue(issue_key).raw['fields']['resolutiondate'][0:10]
        return self.get_issue(issue_key).fields.resolutiondate[0:10]

    def get_issue_result_xinxianglian(self, issue_key):
        '''
        获取问题编号的 处理结果； 无法分析为63600 ；新增问题为63602 ；
        :param issue_key:
        :return:
        '''
        # if self.get_issue(issue_key).raw['fields']['customfield_18500'] == None:
        #     return self.get_issue(issue_key).raw['fields']['customfield_18500']
        # else:
        #     return self.get_issue(issue_key).raw['fields']['customfield_18500']['value']

        if self.get_issue(issue_key).fields.customfield_18500 == None:
            return self.get_issue(issue_key).fields.customfield_18500
        else:
            return self.get_issue(issue_key).fields.customfield_18500.value

    def get_issue_result(self, issue_key):
        '''
        获取问题编号的 处理结果； 无法分析为63600 ；新增问题为63602 ；
        :param issue_key:
        :return:
        '''
        # if self.get_issue(issue_key).raw['fields']['customfield_18500'] == None:
        #     return self.get_issue(issue_key).raw['fields']['customfield_18500']
        # else:
        #     return self.get_issue(issue_key).raw['fields']['customfield_18500']['value']

        if self.get_issue(issue_key).fields.resolution == None:
            return self.get_issue(issue_key).fields.resolution
        else:
            return self.get_issue(issue_key).fields.resolution.name

    def get_issue_source(self, issue_key):
        '''
        获取问题编号的 问题来源； 信相连63406； 网络信息
        :param issue_key:
        :return:
        '''
        # if
        # return self.get_issue(issue_key).raw['fields']['customfield_17300']['value']
        # if self.get_issue(issue_key).raw['fields']['customfield_17300'] == None:
        #     return self.get_issue(issue_key).raw['fields']['customfield_17300']
        # else:
        #     return self.get_issue(issue_key).raw['fields']['customfield_17300']['value']
        if self.get_issue(issue_key).fields.customfield_17300 == None:
            return self.get_issue(issue_key).fields.customfield_17300
        else:
            return self.get_issue(issue_key).fields.customfield_17300.value

    def get_issue_type(self, issue_key):
        '''
        获取问题编号的 类型
        :param issue_key:
        :return:
        '''
        # return self.get_issue(issue_key).raw['fields']['issuetype']['name']
        return self.get_issue(issue_key).fields.issuetype.name

    def get_issue_key(self, issue_id):
        '''
        由ID 获取其对应的key
        :param issue_id:
        :return:
        '''
        return self.get_issue(issue_id).key

    def get_issue_project(self, issue_key):
        '''
        获取问题编号对应的 库
        :param issue_key:
        :return:
        '''
        # return self.get_issue(issue_key).raw['fields']['project']['key']
        return self.get_issue(issue_key).fields.project.key

    def get_issue_description(self, issue_key):
        '''
        获取问题常规描述
        :param issue_key:
        :return:
        '''
        return self.get_issue(issue_key).fields.description

    def get_issue_feedback(self, issue_key):
        '''
        获取问题编码对应的 问题描述
        :param issue_key:
        :return:
        '''
        # return self.get_issue(issue_key).raw['fields']['customfield_10815']
        return self.get_issue(issue_key).fields.customfield_10815

    def get_issue_test_category(self, issue_key):
        '''
        获取问题编码对应的 测试类别，如验收Acceptance
        :param issue_key:
        :return:
        '''
        if self.get_issue(issue_key).fields.customfield_10014 == None:
            return self.get_issue(issue_key).fields.customfield_10014
        else:
            return self.get_issue(issue_key).fields.customfield_10014.value

    def get_issue_versions(self, issue_key):
        '''
        获取影响版本
        :return:
        '''
        return self.get_issue(issue_key).fields.versions[0].name

    def get_issue_summary(self, issue_key):
        '''
        获取问题编码对应的 主题
        :param issue_key:
        :return:
        '''
        # return self.get_issue(issue_key).raw['fields']['summary']
        return self.get_issue(issue_key).fields.summary

    def get_issue_priority(self, issue_key):
        '''
        获取问题编码对应的 优先级
        :param issue_key:
        :return:
        '''
        # return self.get_issue(issue_key).raw['fields']['priority']['name']
        return self.get_issue(issue_key).fields.priority.name

    def get_issue_status(self, issue_key):
        '''
        获取问题编码对应的 问题状态
        :param issue_key:
        :return:
        '''
        # return self.get_issue(issue_key).raw['fields']['priority']['name']
        return self.get_issue(issue_key).fields.status.name

    def get_issue_probability(self, issue_key):
        if self.get_issue(issue_key).fields.customfield_10005 == None:
            return self.get_issue(issue_key).fields.customfield_10005
        else:
            return self.get_issue(issue_key).fields.customfield_10005.value

    def get_issues_closed_yesterday(self, issue_type=("Market Problem", "Market Problem")):
        '''
        获取昨天close的 market problem 问题;  且问题处理类型必须为 无法分析 或是 新增问题
        :param issue_type: 问题类型
        :return: issues 的列表
        '''
        today = CommonUtils.get_date_others(0)
        yesterday = CommonUtils.get_date_others(-1)  # -1是昨天；-2是前天
        # resolved 字段对应 resolutiondate 字段
        jql = 'issuetype in {} and (resolved >{} and resolved < {})'.format(issue_type, yesterday, today)  # [昨天,今天)
        issues = self.jira_client.search_issues(jql)
        issues_list = []  # 列表元素为字典, 每个字典是检索到的issue的具体信息,用于以后操作
        issues_list_use = []
        for item in issues:
            issue_key = item.key
            issues_list.append({'key': issue_key})
            i = len(issues_list) - 1  # 获取当前列表的长度
            issues_list[i]['project'] = self.get_issue_project(issue_key)
            issues_list[i]['summary'] = self.get_issue_summary(issue_key)
            issues_list[i]['feedback'] = self.get_issue_feedback(issue_key)
            issues_list[i]['type'] = self.get_issue_type(issue_key)
            issues_list[i]['priority'] = self.get_issue_priority(issue_key)
            issues_list[i]['status'] = self.get_issue_status(issue_key)
            issues_list[i]['result'] = self.get_issue_result_xinxianglian(issue_key)
            issues_list[i]['source'] = self.get_issue_source(issue_key)
            issues_list[i]['resolutiondate'] = self.get_issue_resolutiondate(issue_key)
            issues_list[i]['probability'] = self.get_issue_probability(issue_key)

        # 　遍历列表，筛选出 新增问题 与 无法分析 的问题
        for item in issues_list:
            if ((item['result'] == '新增问题' or item['result'] == '无法分析')
                    and (item['source'] == '信相连' or item['source'] == '网络信息')):
                issues_list_use.append(item)

        return issues_list_use

    def get_issue_preuser2sw_yesterday(self):
        zero_yesterday = CommonUtils.get_date_time_others_zero(-1)
        last_yesterday = CommonUtils.get_date_time_others_last(-1)

        sql_preuser2sw = 'select issueid from changegroup where ID in (select groupid from changeitem where \
                         OLDSTRING="PreUser Bug" and NEWSTRING="SW Bug") and CREATED between %s and %s'
        issues = MysqlUtils.find_data_dic_2args(sql_preuser2sw, zero_yesterday, last_yesterday)
        issues_list = []  # 列表元素为字典, 每个字典是检索到的issue的具体信息,用于以后操作
        issues_list_use = []

        if issues:
            for item in issues:
                issue_key = str(item['issueid'])
                issues_list.append({'id': issue_key})
                i = len(issues_list) - 1  # 获取当前列表的长度
                issues_list[i]['project'] = self.get_issue_project(issue_key)
                issues_list[i]['summary'] = self.get_issue_summary(issue_key)
                issues_list[i]['description'] = self.get_issue_description(issue_key)
                issues_list[i]['type'] = self.get_issue_type(issue_key)
                issues_list[i]['priority'] = self.get_issue_priority(issue_key)
                issues_list[i]['status'] = self.get_issue_status(issue_key)
                issues_list[i]['source'] = self.get_issue_source(issue_key)
                issues_list[i]['probability'] = self.get_issue_probability(issue_key)
                issues_list[i]['versions'] = self.get_issue_versions(issue_key)
                issues_list[i]['key'] = self.get_issue_key(issue_key)

            # 　遍历列表，筛选出 版本号为6开头的
            for item in issues_list:
                if (ReUtils.bool_version_6(item['versions'])):
                    issues_list_use.append(item)
        else:
            issues_list_use = []

        return issues_list_use

    def get_issue_yanshou_yesterday(self):
        '''
        获取昨天 测试类别为 验收；由 open 变为 resolved ; 且解决结果为 fiexed 与 Pendings的问题
        :return:
        '''
        zero_yesterday = CommonUtils.get_date_time_others_zero(-1)
        last_yesterday = CommonUtils.get_date_time_others_last(-1)

        sql_preuser2sw = 'select issueid from changegroup where ID in (select groupid from changeitem where \
                         OLDSTRING="Open" and NEWSTRING="Resolved") and CREATED between %s and %s'
        issues = MysqlUtils.find_data_dic_2args(sql_preuser2sw, zero_yesterday, last_yesterday)
        issues_list = []  # 列表元素为字典, 每个字典是检索到的issue的具体信息,用于以后操作
        issues_list_use = []

        if issues:
            for item in issues:
                try:
                    issue_key = str(item['issueid'])
                    issues_list.append({'id': issue_key})
                    i = len(issues_list) - 1  # 获取当前列表的长度
                    issues_list[i]['project'] = self.get_issue_project(issue_key)
                    issues_list[i]['summary'] = self.get_issue_summary(issue_key)
                    issues_list[i]['description'] = self.get_issue_description(issue_key)
                    issues_list[i]['type'] = self.get_issue_type(issue_key)
                    issues_list[i]['priority'] = self.get_issue_priority(issue_key)
                    issues_list[i]['status'] = self.get_issue_status(issue_key)
                    issues_list[i]['probability'] = self.get_issue_probability(issue_key)
                    issues_list[i]['test_category'] = self.get_issue_test_category(issue_key)
                    issues_list[i]['key'] = self.get_issue_key(issue_key)
                    issues_list[i]['result'] = self.get_issue_result(issue_key)
                except:
                    # 有异常时不去考虑，继续下一个
                    continue

            # 　遍历列表，筛选出 版本号为6开头的
            for item in issues_list:
                if ('test_category' in item):
                    if (item['test_category'] == "验收Acceptance" or item['test_category'] == "市场反馈") and (
                            item['result'] == "Fixed" or item['result'] == "Pending"):
                        issues_list_use.append(item)
        else:
            issues_list_use = []

        return issues_list_use

    def change_summary(self, key, summary):
        '''
        修改主题
        :param key:
        :param summary:
        :return:
        '''
        issue = self.jira_client.issue(key)
        issue.update(summary=summary)

    def change_des(self, key, des):
        '''
        修改描述
        :param key:
        :param des:
        :return:
        '''
        issue = self.jira_client.issue(key)
        issue.update(description=des)

    def change_reporter(self, key, reporter):
        '''
        :param self: 修改报告人
        :param key:关键字
        :param reporter: 指定新的报告人
        :return:
        '''
        issue = self.jira_client.issue(key)
        issue.update(reporter={'key': reporter})

    def change_assignee(self, key, assignee):
        '''
        修改经办人
        :param key:
        :param assignee:
        :return:
        '''
        issue = self.jira_client.issue(key)
        issue.update(assignee=assignee)

    def upload_attachment(self, key, attachment):
        '''
        上传附件
        :param key:
        :param attachment:
        :return:
        '''
        if not os.path.exists(attachment):
            return False
        try:
            issue = self.jira_client.issue(key)
            self.jira_client.add_attachment(issue=issue, attachment=attachment)
        except:
            print(traceback.format_exc())
            return False


class JiraTaskTool:

    def __init__(self, user, password):
        self.server = 'http://jiratask.hisense.com/'
        self.basic_auth = (user, password)
        self.jira_client = None

    def login(self):
        self.jira_client = JIRA(server=self.server, basic_auth=self.basic_auth)
        if self.jira_client != None:
            return True
        else:
            return False

    def create_issue(self, key, issue_type, summary, assignee, reporter, info_dict=None):
        '''

        :param key:
        :param issue_type:
        :param assignee:
        :param info_dict:
        :return:
        '''

        if info_dict is None:
            info_dict = {}
        issue_dict = {
            'project': {'key': key},
            'issuetype': {'name': issue_type},
            'summary': summary,
            'assignee': {'name': assignee},
            'reporter': {'name': reporter},
        }
        issue_dict.update(info_dict)

        if self.jira_client == None:
            self.login()
        return self.jira_client.create_issue(issue_dict)

    def create_sjzlgl_issue(self, summary, product_model, description, priority, source, duedate, probability, assignee,
                            reporter,
                            key='SJZLGL', issue_type='SW Bug',
                            product_line='内销', develop_class='自研'):

        # SJZLGL库需要的字段
        info_dict = {
            'customfield_10002': product_model,
            'description': description,
            'priority': {'name': priority},
            'customfield_19200': {'value': source},
            'duedate': duedate,
            'customfield_10109': {'value': product_line},  # 产品线：内销
            'customfield_10110': {'value': develop_class},  # 开发级别：自研
            'customfield_10005': {'value': probability},  # 概率是什么
        }
        if self.jira_client == None:
            self.login()
        return self.create_issue(key, issue_type, summary, assignee, reporter, info_dict)

    def get_all_prj(self):
        '''
        获取所有的项目
        :return:
        '''
        return self.jira_client.projects()

    def get_one_prj(self, prj_key):
        '''
        根据key获取此项目的所有信息
        :return:
        '''
        return self.jira_client.project(prj_key)

    def get_issue(self, issue_key):
        '''
        根据issue_key获取issue信息
        :param issue_key:
        :return:
        '''
        return self.jira_client.issue(issue_key)

    def get_issue_subtasks(self, issue_key):
        '''
        根据issue_key获取子TASK信息
        :param issue_key:
        :return:
        '''
        return self.get_issue(issue_key).fields.subtasks

    def get_issue_subtasks_case_nums(self, issue_key):
        '''
        根据issue_key获取子TASK信息
        :param issue_key:
        :return:
        '''
        sub_tasks = self.get_issue(issue_key).fields.subtasks
        for i in sub_tasks:
            pass

    def get_issue_resolutiondate(self, issue_key):
        '''
        根据issue_key获取resolution更新的日期，此日期为 closed的日期，也就是解决日期
        :param issue_key:
        :return:
        '''
        # return self.get_issue(issue_key).raw['fields']['resolutiondate'][0:10]
        return self.get_issue(issue_key).fields.resolutiondate[0:10]

    def get_issue_result_xinxianglian(self, issue_key):
        '''
        获取问题编号的 处理结果； 无法分析为63600 ；新增问题为63602 ；
        :param issue_key:
        :return:
        '''
        # if self.get_issue(issue_key).raw['fields']['customfield_18500'] == None:
        #     return self.get_issue(issue_key).raw['fields']['customfield_18500']
        # else:
        #     return self.get_issue(issue_key).raw['fields']['customfield_18500']['value']

        if self.get_issue(issue_key).fields.customfield_18500 == None:
            return self.get_issue(issue_key).fields.customfield_18500
        else:
            return self.get_issue(issue_key).fields.customfield_18500.value

    def get_issue_result(self, issue_key):
        '''
        获取问题编号的 处理结果； 无法分析为63600 ；新增问题为63602 ；
        :param issue_key:
        :return:
        '''
        # if self.get_issue(issue_key).raw['fields']['customfield_18500'] == None:
        #     return self.get_issue(issue_key).raw['fields']['customfield_18500']
        # else:
        #     return self.get_issue(issue_key).raw['fields']['customfield_18500']['value']

        if self.get_issue(issue_key).fields.resolution == None:
            return self.get_issue(issue_key).fields.resolution
        else:
            return self.get_issue(issue_key).fields.resolution.name

    def get_issue_source(self, issue_key):
        '''
        获取问题编号的 问题来源； 信相连63406； 网络信息
        :param issue_key:
        :return:
        '''
        # if
        # return self.get_issue(issue_key).raw['fields']['customfield_17300']['value']
        # if self.get_issue(issue_key).raw['fields']['customfield_17300'] == None:
        #     return self.get_issue(issue_key).raw['fields']['customfield_17300']
        # else:
        #     return self.get_issue(issue_key).raw['fields']['customfield_17300']['value']
        if self.get_issue(issue_key).fields.customfield_17300 == None:
            return self.get_issue(issue_key).fields.customfield_17300
        else:
            return self.get_issue(issue_key).fields.customfield_17300.value

    def get_issue_type(self, issue_key):
        '''
        获取问题编号的 类型
        :param issue_key:
        :return:
        '''
        # return self.get_issue(issue_key).raw['fields']['issuetype']['name']
        return self.get_issue(issue_key).fields.issuetype.name

    def get_issue_key(self, issue_id):
        '''
        由ID 获取其对应的key
        :param issue_id:
        :return:
        '''
        return self.get_issue(issue_id).key

    def get_issue_project(self, issue_key):
        '''
        获取问题编号对应的 库
        :param issue_key:
        :return:
        '''
        # return self.get_issue(issue_key).raw['fields']['project']['key']
        return self.get_issue(issue_key).fields.project.key

    def get_issue_description(self, issue_key):
        '''
        获取问题常规描述
        :param issue_key:
        :return:
        '''
        return self.get_issue(issue_key).fields.description

    def get_issue_feedback(self, issue_key):
        '''
        获取问题编码对应的 问题描述
        :param issue_key:
        :return:
        '''
        # return self.get_issue(issue_key).raw['fields']['customfield_10815']
        return self.get_issue(issue_key).fields.customfield_10815

    def get_issue_test_category(self, issue_key):
        '''
        获取问题编码对应的 测试类别，如验收Acceptance
        :param issue_key:
        :return:
        '''
        if self.get_issue(issue_key).fields.customfield_10014 == None:
            return self.get_issue(issue_key).fields.customfield_10014
        else:
            return self.get_issue(issue_key).fields.customfield_10014.value

    def get_issue_versions(self, issue_key):
        '''
        获取影响版本
        :return:
        '''
        return self.get_issue(issue_key).fields.versions[0].name

    def get_issue_summary(self, issue_key):
        '''
        获取问题编码对应的 主题
        :param issue_key:
        :return:
        '''
        # return self.get_issue(issue_key).raw['fields']['summary']
        return self.get_issue(issue_key).fields.summary

    def get_issue_priority(self, issue_key):
        '''
        获取问题编码对应的 优先级
        :param issue_key:
        :return:
        '''
        # return self.get_issue(issue_key).raw['fields']['priority']['name']
        return self.get_issue(issue_key).fields.priority.name

    def get_issue_status(self, issue_key):
        '''
        获取问题编码对应的 问题状态
        :param issue_key:
        :return:
        '''
        # return self.get_issue(issue_key).raw['fields']['priority']['name']
        return self.get_issue(issue_key).fields.status.name

    def get_issue_probability(self, issue_key):
        if self.get_issue(issue_key).fields.customfield_10005 == None:
            return self.get_issue(issue_key).fields.customfield_10005
        else:
            return self.get_issue(issue_key).fields.customfield_10005.value

    def get_issues_closed_yesterday(self, issue_type=("Market Problem", "Market Problem")):
        '''
        获取昨天close的 market problem 问题;  且问题处理类型必须为 无法分析 或是 新增问题
        :param issue_type: 问题类型
        :return: issues 的列表
        '''
        today = CommonUtils.get_date_others(0)
        yesterday = CommonUtils.get_date_others(-1)  # -1是昨天；-2是前天
        # resolved 字段对应 resolutiondate 字段
        jql = 'issuetype in {} and (resolved >{} and resolved < {})'.format(issue_type, yesterday, today)  # [昨天,今天)
        issues = self.jira_client.search_issues(jql)
        issues_list = []  # 列表元素为字典, 每个字典是检索到的issue的具体信息,用于以后操作
        issues_list_use = []
        for item in issues:
            issue_key = item.key
            issues_list.append({'key': issue_key})
            i = len(issues_list) - 1  # 获取当前列表的长度
            issues_list[i]['project'] = self.get_issue_project(issue_key)
            issues_list[i]['summary'] = self.get_issue_summary(issue_key)
            issues_list[i]['feedback'] = self.get_issue_feedback(issue_key)
            issues_list[i]['type'] = self.get_issue_type(issue_key)
            issues_list[i]['priority'] = self.get_issue_priority(issue_key)
            issues_list[i]['status'] = self.get_issue_status(issue_key)
            issues_list[i]['result'] = self.get_issue_result_xinxianglian(issue_key)
            issues_list[i]['source'] = self.get_issue_source(issue_key)
            issues_list[i]['resolutiondate'] = self.get_issue_resolutiondate(issue_key)
            issues_list[i]['probability'] = self.get_issue_probability(issue_key)

        # 　遍历列表，筛选出 新增问题 与 无法分析 的问题
        for item in issues_list:
            if ((item['result'] == '新增问题' or item['result'] == '无法分析')
                    and (item['source'] == '信相连' or item['source'] == '网络信息')):
                issues_list_use.append(item)

        return issues_list_use

    def get_issue_preuser2sw_yesterday(self):
        zero_yesterday = CommonUtils.get_date_time_others_zero(-1)
        last_yesterday = CommonUtils.get_date_time_others_last(-1)

        sql_preuser2sw = 'select issueid from changegroup where ID in (select groupid from changeitem where \
                         OLDSTRING="PreUser Bug" and NEWSTRING="SW Bug") and CREATED between %s and %s'
        issues = MysqlUtils.find_data_dic_2args(sql_preuser2sw, zero_yesterday, last_yesterday)
        issues_list = []  # 列表元素为字典, 每个字典是检索到的issue的具体信息,用于以后操作
        issues_list_use = []

        if issues:
            for item in issues:
                issue_key = str(item['issueid'])
                issues_list.append({'id': issue_key})
                i = len(issues_list) - 1  # 获取当前列表的长度
                issues_list[i]['project'] = self.get_issue_project(issue_key)
                issues_list[i]['summary'] = self.get_issue_summary(issue_key)
                issues_list[i]['description'] = self.get_issue_description(issue_key)
                issues_list[i]['type'] = self.get_issue_type(issue_key)
                issues_list[i]['priority'] = self.get_issue_priority(issue_key)
                issues_list[i]['status'] = self.get_issue_status(issue_key)
                issues_list[i]['source'] = self.get_issue_source(issue_key)
                issues_list[i]['probability'] = self.get_issue_probability(issue_key)
                issues_list[i]['versions'] = self.get_issue_versions(issue_key)
                issues_list[i]['key'] = self.get_issue_key(issue_key)

            # 　遍历列表，筛选出 版本号为6开头的
            for item in issues_list:
                if (ReUtils.bool_version_6(item['versions'])):
                    issues_list_use.append(item)
        else:
            issues_list_use = []

        return issues_list_use

    def get_issue_yanshou_yesterday(self):
        '''
        获取昨天 测试类别为 验收；由 open 变为 resolved ; 且解决结果为 fiexed 与 Pendings的问题
        :return:
        '''
        zero_yesterday = CommonUtils.get_date_time_others_zero(-1)
        last_yesterday = CommonUtils.get_date_time_others_last(-1)

        sql_preuser2sw = 'select issueid from changegroup where ID in (select groupid from changeitem where \
                         OLDSTRING="Open" and NEWSTRING="Resolved") and CREATED between %s and %s'
        issues = MysqlUtils.find_data_dic_2args(sql_preuser2sw, zero_yesterday, last_yesterday)
        issues_list = []  # 列表元素为字典, 每个字典是检索到的issue的具体信息,用于以后操作
        issues_list_use = []

        if issues:
            for item in issues:
                try:
                    issue_key = str(item['issueid'])
                    issues_list.append({'id': issue_key})
                    i = len(issues_list) - 1  # 获取当前列表的长度
                    issues_list[i]['project'] = self.get_issue_project(issue_key)
                    issues_list[i]['summary'] = self.get_issue_summary(issue_key)
                    issues_list[i]['description'] = self.get_issue_description(issue_key)
                    issues_list[i]['type'] = self.get_issue_type(issue_key)
                    issues_list[i]['priority'] = self.get_issue_priority(issue_key)
                    issues_list[i]['status'] = self.get_issue_status(issue_key)
                    issues_list[i]['probability'] = self.get_issue_probability(issue_key)
                    issues_list[i]['test_category'] = self.get_issue_test_category(issue_key)
                    issues_list[i]['key'] = self.get_issue_key(issue_key)
                    issues_list[i]['result'] = self.get_issue_result(issue_key)
                except:
                    # 有异常时不去考虑，继续下一个
                    continue

            # 　遍历列表，筛选出 版本号为6开头的
            for item in issues_list:
                if ('test_category' in item):
                    if (item['test_category'] == "验收Acceptance" or item['test_category'] == "市场反馈") and (
                            item['result'] == "Fixed" or item['result'] == "Pending"):
                        issues_list_use.append(item)
        else:
            issues_list_use = []

        return issues_list_use

    def change_summary(self, key, summary):
        '''
        修改主题
        :param key:
        :param summary:
        :return:
        '''
        issue = self.jira_client.issue(key)
        issue.update(summary=summary)

    def change_des(self, key, des):
        '''
        修改描述
        :param key:
        :param des:
        :return:
        '''
        issue = self.jira_client.issue(key)
        issue.update(description=des)

    def change_reporter(self, key, reporter):
        '''
        :param self: 修改报告人
        :param key:关键字
        :param reporter: 指定新的报告人
        :return:
        '''
        issue = self.jira_client.issue(key)
        issue.update(reporter={'key': reporter})

    def change_assignee(self, key, assignee):
        '''
        修改经办人
        :param key:
        :param assignee:
        :return:
        '''
        issue = self.jira_client.issue(key)
        issue.update(assignee=assignee)

    def upload_attachment(self, key, attachment):
        '''
        上传附件
        :param key:
        :param attachment:
        :return:
        '''
        if not os.path.exists(attachment):
            return False
        try:
            issue = self.jira_client.issue(key)
            self.jira_client.add_attachment(issue=issue, attachment=attachment)
        except:
            print(traceback.format_exc())
            return False


if __name__ == '__main__':
    JIRA_USER = 'jenkinsserver'
    JIRA_DMT_PASSWORD = 'a*505408'  # 问题库
    JIRA_TASK_PASSWORD = 'hisense123'  # 任务库

    mytask = JiraTaskTool(JIRA_USER, JIRA_TASK_PASSWORD)
    mytask.login()
    issue_key = "691657"
    ss = mytask.get_issue(issue_key)
    sub_ = mytask.get_issue_subtasks(issue_key)
    # issue = myjira.get_issue(issue_key)
    # myjira = JiraQesTool(JIRA_USER, JIRA_DMT_PASSWORD)
    # myjira.login()
    # # 以下是一些尝试操作
    # issue_key = "HNR320T-8345"
    # issue = myjira.get_issue(issue_key)
    # print(myjira.get_issue_versions(issue_key))
    # print(myjira.get_issue_description(issue_key))
    # print(myjira.get_issue_key(issue_key))
    # print(myjira.get_issue_type(issue_key))
    # print(myjira.get_issue_source(issue_key))
    # print(myjira.get_issue_description(issue_key))
    # print(myjira.get_issue_priority(issue_key))
    # print(myjira.get_issue_project(issue_key))
    # print(myjira.get_issue_result(issue_key))
    # print(myjira.get_issue_summary(issue_key))
    # print(myjira.get_issue_status(issue_key))
    # print(myjira.get_issue_preuser2sw_yesterday())
    # print(myjira.get_issues_closed_yesterday())

    # print(type(myjira.get_issues()))
    # for i in sub_:
    #     print(mytask.get_issue(i['key']).fields.customfield_16100)
    ll = sub_[0].key
    case_dict = {}
    case_pass = 0
    case_fail = 0
    case_undone = 0
    case_block = 0
    case_auto = 0
    defect_major = 0
    defect_all = 0
    case_unsupported = 0
    for i in sub_:
        if mytask.get_issue(i.key).fields.customfield_16100 == None:
            pass
        else:
            case_pass = case_pass + mytask.get_issue(i.key).fields.customfield_16100  # 用例通过数量

        if mytask.get_issue(i.key).fields.customfield_16101 == None:
            pass
        else:
            case_fail = case_fail + mytask.get_issue(i.key).fields.customfield_16101  # 用例失败数量

        if mytask.get_issue(i.key).fields.customfield_16102 == None:
            pass
        else:
            case_undone = case_undone + mytask.get_issue(i.key).fields.customfield_16102  # 用例通过数量

        if mytask.get_issue(i.key).fields.customfield_18500 == None:
            pass
        else:
            case_block = case_block + mytask.get_issue(i.key).fields.customfield_18500  # 用例失败数量

        if mytask.get_issue(i.key).fields.customfield_18501 == None:
            pass
        else:
            case_unsupported = case_unsupported + mytask.get_issue(i.key).fields.customfield_18501  # 不支持用例数量

        if mytask.get_issue(i.key).fields.customfield_18505 == None:
            pass
        else:
            case_auto = case_auto + mytask.get_issue(i.key).fields.customfield_18505

        if mytask.get_issue(i.key).fields.customfield_18502 == None:
            pass
        else:
            defect_major = defect_major + mytask.get_issue(i.key).fields.customfield_18502

        if mytask.get_issue(i.key).fields.customfield_18503 == None:
            pass
        else:
            defect_all = defect_all + mytask.get_issue(i.key).fields.customfield_18503

    case_dict['case_pass'] = case_pass
    case_dict['case_fail'] = case_fail
    case_dict['case_undone'] = case_undone
    case_dict['case_block'] = case_block
    case_dict['case_unsupported'] = case_unsupported
    case_dict['case_auto'] = case_auto
    case_dict['defect_major'] = defect_major
    case_dict['defect_all'] = defect_all

    print(case_dict)
