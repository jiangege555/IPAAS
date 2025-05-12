# # from myutils.logformat import MyLogger
# from test_case_auth_paas import global_data_paas as paas_global_data
# from test_case_auth_iaas import global_data_iaas as iaas_global_data
# from test_case_auth_paas import logger as paas_logger
# from test_case_auth_iaas import logger as iaas_logger
# import requests, jsonpath, re
# from main import platform_global
import time
# logger = MyLogger("main").logger

# def pytest_addoption(parser):
#     parser.addoption("--batch", action="store", default="1", help="Set batch label")

def pytest_configure(config):
    # 每轮测试使用不同的时间戳作为 historyId 后缀
    config.option.allure_history_id_suffix = str(int(time.time()))


def pytest_collection_modifyitems(items):
    for item in items:
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode_escape')

# def pytest_sessionstart(session):
#     """
#    接口测试开始前的操作，查询IAAS和PAAS平台对应ak下的实例和板卡信息
#    :param session:
#    :return:
#    """
#     pass
    # if iaas_global_data.get("instance_ids") != [] and paas_global_data.get("instance_ids") != []:
    #     return
    # if platform_global.lower() == 'iaas':
    #     # 初始化iaas参数
    #     url_iaas = iaas_global_data.get("url")
    #     header_iaas = iaas_global_data.get("header")
    #     data_iaas = {}
    #     # IAAS鉴权请求
    #     res_iaas_sign = requests.post(url=url_iaas + "/openApi/post/sign", headers=header_iaas, json=data_iaas)
    #     res_text = res_iaas_sign.text
    #     if res_iaas_sign.status_code != 200:
    #         Sign = re.findall(r'serverSign\\":\\"(\w+)\\",', res_text)[0]
    #         header_iaas["Sign"] = Sign
    #     res_iaas = requests.post(url=url_iaas + "/openApi/ListInstanceInfo", headers=header_iaas, json=data_iaas)
    #     res_iaas_json = res_iaas.json()
    #     iaas_logger.info(f'iaas查询结果为{res_iaas_json}')
    #     # with lock:
    #     iaas_instance = list(set(jsonpath.jsonpath(res_iaas_json, "$..instance_id")))
    #     iaas_sns = list(set(jsonpath.jsonpath(res_iaas.json(), "$..sn")))
    #     iaas_global_data["instance_ids"] = iaas_instance
    #     iaas_global_data["card_sns"] = iaas_sns
    #     iaas_logger.info(f'提取的iaas instance_ids: {iaas_instance}, 提取的iaas card_sns: {iaas_sns}')
# elif platform_global.lower() == 'paas':
#     # 初始化paas参数
#     url_paas = paas_global_data.get("url")
#     header_paas = paas_global_data.get("header")
#     data_paas = {
#         "idcs": [paas_global_data.get("idc_init")],
#         "vendor": paas_global_data.get("vendor"),
#         "instanceType": paas_global_data.get("instance_type")
#     }
#     # PAAS鉴权请求
#     res_paas_sign = requests.post(url=url_paas + "/v1/post/sign", headers=header_paas, json=data_paas)
#     res_text = res_paas_sign.text
#     if res_paas_sign.status_code != 200:
#         Sign = re.findall(r'serverSign\\":\\"(\w+)\\",', res_text)[0]
#         header_paas["Sign"] = Sign
#     res_paas = requests.post(url=url_paas + "/v1/instance/list", headers=header_paas, json=data_paas)
#     res_paas_json = res_paas.json()
#     paas_logger.info(f'paas查询结果为{res_paas_json}')
#     # with lock:
#     paas_instance = jsonpath.jsonpath(res_paas_json, "$..instanceId")
#     paas_global_data["instance_ids"] = paas_instance
#     paas_logger.info(f'提取的paas instance_ids: {paas_instance}')
    # elif platform_global.lower() == 'all':
    #     # 初始化iaas参数
    #     url_iaas = iaas_global_data.get("url")
    #     header_iaas = iaas_global_data.get("header")
    #     data_iaas = {}
    #     # IAAS鉴权请求
    #     res_iaas_sign = requests.post(url=url_iaas + "/openApi/post/sign", headers=header_iaas, json=data_iaas)
    #     res_text = res_iaas_sign.text
    #     if res_iaas_sign.status_code != 200:
    #         Sign = re.findall(r'serverSign\\":\\"(\w+)\\",', res_text)[0]
    #         header_iaas["Sign"] = Sign
    #     res_iaas = requests.post(url=url_iaas + "/openApi/ListInstanceInfo", headers=header_iaas, json=data_iaas)
    #     res_iaas_json = res_iaas.json()
    #     iaas_logger.info(f'iaas查询结果为{res_iaas_json}')
    #     # with lock:
    #     iaas_instance = list(set(jsonpath.jsonpath(res_iaas_json, "$..instance_id")))
    #     iaas_sns = list(set(jsonpath.jsonpath(res_iaas.json(), "$..sn")))
    #     iaas_global_data["instance_ids"] = iaas_instance
    #     iaas_global_data["card_sns"] = iaas_sns
    #     iaas_logger.info(f'提取的iaas instance_ids: {iaas_instance}, 提取的iaas card_sns: {iaas_sns}')
    #     # 初始化paas参数
    #     url_paas = paas_global_data.get("url")
    #     header_paas = paas_global_data.get("header")
    #     data_paas = {
    #         "idcs": [paas_global_data.get("idc_init")],
    #         "vendor": paas_global_data.get("vendor"),
    #         "instanceType": paas_global_data.get("instance_type")
    #     }
    #     # PAAS鉴权请求
    #     res_paas_sign = requests.post(url=url_paas + "/v1/post/sign", headers=header_paas, json=data_paas)
    #     res_text = res_paas_sign.text
    #     if res_paas_sign.status_code != 200:
    #         Sign = re.findall(r'serverSign\\":\\"(\w+)\\",', res_text)[0]
    #         header_paas["Sign"] = Sign
    #     res_paas = requests.post(url=url_paas + "/v1/instance/list", headers=header_paas, json=data_paas)
    #     res_paas_json = res_paas.json()
    #     paas_logger.info(f'paas查询结果为{res_paas_json}')
    #     # with lock:
    #     paas_instance = jsonpath.jsonpath(res_paas_json, "$..instanceId")
    #     paas_global_data["instance_ids"] = paas_instance
    #     paas_logger.info(f'提取的paas instance_ids: {paas_instance}')

    # iaas_logger.info("**************iaas接口测试开始***************")
    # paas_logger.info("**************paas接口测试开始***************")


# def pytest_sessionfinish(session):
#     """
#     接口测试结束后的操作
#     :param session:
#     :return:
#     """
#     # iaas_logger.info("**************iaas接口测试结束***************")
#     # paas_logger.info("**************paas接口测试结束***************")
#     pass
#     CR = CheckResult()
#     paas_task = paas_global_data.get("taskIds")
#     logger.info(f"**********{paas_task}*********")
#     for i in paas_task:
#         logger.info(f"**********{i}*********")
#         CR.check_progress_paas(i)


"""
"""
# class CheckResult:
#
#     # instance_id = global_data.get("instance_id")
#     # url = global_data.get("url")
#     # header = global_data.get("header")
#     task_id = ""
#     request_id = ""
#     # Sign = global_data.get("Sign")
#     # file_id = global_data.get("file_id")
#     # app_id = global_data.get("app_id")
#     # app_package = global_data.get("app_package")
#
#     def get_auth_paas(self, data=None):
#         url = paas_global_data.get("url") + "/v1/get/sign"
#         paas_global_data["header"]["Sign"] = "111111"
#         res = requests.get(url=url, headers=paas_global_data.get("header"), params=data)
#         try:
#             res_text = res.text
#             if res.status_code != 200:
#                 Sign = re.findall(r'serverSign\\":\\"(\w+)\\",', res_text)[0]
#             else:
#                 Sign = paas_global_data.get("header")["Sign"]
#         except Exception as e:
#             Sign = "111111"
#             logger.error(f"鉴权请求发生错误：postSign--{res.text}")
#         return Sign
#
#     def post_auth_paas(self, data):
#         url = paas_global_data.get("url") + "/v1/post/sign"
#         paas_global_data["header"]["Sign"] = "111111"
#         res = requests.post(url=url, headers=paas_global_data.get("header"), json=data)
#         try:
#             res_text = res.text
#             if res.status_code != 200:
#                 Sign = re.findall(r'serverSign\\":\\"(\w+)\\",', res_text)[0]
#             else:
#                 Sign = paas_global_data.get("header")["Sign"]
#             # print(Sign)
#         except Exception as e:
#             Sign = "111111"
#             logger.error(f"鉴权请求发生错误：postSign--{res.text}")
#         return Sign
#
#     def check_progress_paas(self, taskIds):
#         # print(task_ids)
#         task_id = taskIds.get("task_id")
#         task_name = taskIds.get("task_name")
#         time.sleep(5)
#         logger.info(f'查询中的任务为--{task_name},任务id--{task_id}')
#         uri = f"/v1/task/list"
#         if task_id != self.task_id:
#             self.task_id = task_id
#             sign = self.get_auth_paas({"taskId": task_id})
#             paas_global_data["header"]["Sign"] = sign
#         logger.info(f'header为{paas_global_data.get("header")}')
#         res = requests.get(url=paas_global_data.get("url") + uri, params={"taskId": task_id}, headers=paas_global_data.get("header"))
#         logger.info(res.text)
#         res.raise_for_status()  # 抛出HTTP错误
#         res_json = res.json()
#         # print(res_json)
#         code = jsonpath.jsonpath(res_json, "$.status")[0]
#         if str(code) == '0':
#             status = jsonpath.jsonpath(res_json, "$..taskStatus")[0]
#             if str(status) == "1":
#                 subTaskFailCount = jsonpath.jsonpath(res_json, "$..subTaskFailCount")[0]
#                 # 判断是否有失败，有失败调用子任务查询接口，打印详细信息
#                 if subTaskFailCount != 0:
#                     res_detail = requests.get(url=paas_global_data.get("url") + f"/v1/subtask/list", params={"taskId": task_id},
#                                               headers=paas_global_data.get("header"))
#                     logger.error(f'{task_name}任务执行存在失败，失败数量:{subTaskFailCount}，res == {res_detail.text}')
#                 else:
#                     logger.info(f'断言{task_name}任务查询为全部执行成功，res == {res.text}')
#             else:
#                 # time.sleep(10)
#                 self.check_progress_paas(taskIds)
#         else:
#             logger.error(f'断言{task_name}任务查询接口status失败，status为{code}，res == {res.text}')
