import allure, jsonpath, requests, time, re
from test_case_auth_iaas import logger, global_data_iaas
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class BaseTestCaseIaas:

    url = global_data_iaas.get("url")
    request_id = []
    image_count = 0
    backup_count = 0
    count = 0

    def postSign(self, data):
        """
        post请求鉴权
        :param data: {}格式
        :return:
        """
        global_data_iaas["header"]["Sign"] = "111111"
        url = self.url + "/openApi/post/sign"
        res = requests.post(url=url, headers=global_data_iaas.get("header"), json=data, verify=False)
        try:
            res_text = res.text
            if res.status_code != 200:
                Sign = re.findall(r'serverSign\\":\\"(\w+)\\",', res_text)[0]
            else:
                Sign = global_data_iaas.get("header")["Sign"]
            # print(Sign)
        except Exception as e:
            Sign = "111111"
            logger.error(f"鉴权请求发生错误：postSign--{res.text}")
        return Sign

    def getSign(self, params=None):
        """
        get请求鉴权
        :param params: {}格式
        :return:
        """
        global_data_iaas["header"]["Sign"] = "111111"
        url = self.url + "/openApi/get/sign"
        res = requests.get(url=url, headers=global_data_iaas.get("header"), params=params, verify=False)
        try:
            res_text = res.text
            if res.status_code != 200:
                Sign = re.findall(r'serverSign\\":\\"(\w+)\\",', res_text)[0]
            else:
                Sign = global_data_iaas.get("header")["Sign"]
            # print(Sign)
        except Exception as e:
            Sign = "111111"
            logger.error(f"鉴权请求发生错误：getSign--{res.text}")
        return Sign

    # @timeout_decorator(300)
    def checkProgressIaas(self, request_id, time_sleep=5):
        """
        任务进度查询，将同步返回的request_id列表传入，查询每个任务的状态
        :param request_id: List格式
        :param time_sleep: 默认5秒查询一次
        :return:
        """
        self.count += 1
        time.sleep(time_sleep)
        if request_id != self.request_id:
            logger.info(f"""查询中的任务id--{str(request_id).replace("'", '"')}""")
            self.request_id = request_id
            sign = self.postSign({"request_id": request_id})
            global_data_iaas["header"]["Sign"] = sign
            logger.info(f"""请求headers--{str(global_data_iaas.get("header")).replace("'", '"')}""")
        url = self.url + "/openApi/CheckProgress"
        data = {"request_id": request_id}
        res = requests.post(url=url, headers=global_data_iaas.get("header"), json=data, verify=False)
        if self.count == 90:
            assert False, logger.error(f'任务执行超时,res == {res.text}')
        res.raise_for_status()  # 抛出HTTP错误
        res_json = res.json()
        code = jsonpath.jsonpath(res_json, "$.status_code")[0]
        if str(code) == '0':
            task_codes = jsonpath.jsonpath(res_json, "$..code")
            # 判断任务是否全部执行完成
            if 2 not in task_codes and 3 not in task_codes:
                taskFailCount = task_codes.count(0)
                # logger.info(f'任务查询')
                # logger.info(f'任务查询为全部执行完毕,res == {res.text}')
                # return taskFailCount
                # 判断子任务是否有失败
                if taskFailCount != 0:
                    allure.attach(f"任务查询详情--失败数量:{taskFailCount}-- {res.text}", name="异步任务失败信息")
                    assert False, logger.error(f'任务执行存在失败,失败数量:{taskFailCount},res == {res.text}')
                else:
                    assert True
                    allure.attach(f"任务查询详情--失败数量:{taskFailCount}-- {res.text}", name="异步任务成功信息")
                    logger.info(f'断言任务查询为全部执行成功,失败数量:{taskFailCount},res == {res.text}')
            else:
                self.checkProgressIaas(request_id, time_sleep)
        else:
            assert False, logger.error(f'断言任务查询接口status_code失败,status_code为{code},res == {res.text}')

    # @timeout_decorator(300)
    # def checkProgressIaas(self, request_id, time_sleep=5):
    #     """
    #     任务进度查询，将同步返回的request_id列表传入，查询每个任务的状态
    #     :param request_id: List格式
    #     :param time_sleep: 默认5秒查询一次
    #     :return:
    #     """
    #     logger.info(f"""查询中的任务id--{str(request_id).replace("'", '"')}""")
    #     sign = self.postSign({"request_id": request_id})
    #     global_data["header"]["Sign"] = sign
    #     logger.info(f"""请求headers--{str(global_data.get("header")).replace("'", '"')}""")
    #     url = self.url + "/openApi/CheckProgress"
    #     data = {"request_id": request_id}
    #     try:
    #         while True:
    #             res = requests.post(url=url, headers=global_data.get("header"), json=data)
    #             res.raise_for_status()  # 抛出HTTP错误
    #             res_json = res.json()
    #             code = jsonpath.jsonpath(res_json, "$.status_code")[0]
    #             if str(code) == '0':
    #                 task_codes = jsonpath.jsonpath(res_json, "$..code")
    #                 # 判断任务是否全部执行完成
    #                 if 2 not in task_codes and 3 not in task_codes:
    #                     subTaskFailCount = task_codes.count(0)
    #                     # 判断子任务是否有失败
    #                     if subTaskFailCount != 0:
    #                         assert subTaskFailCount == 0, logger.error(f'任务执行存在失败,失败数量:{subTaskFailCount},res == {res.text}')
    #                         break
    #                     else:
    #                         assert True
    #                         logger.info(f'断言任务查询为全部执行成功,res == {res.text}')
    #                         break
    #                 else:
    #                     time.sleep(time_sleep)
    #                     continue
    #             else:
    #                 assert str(code) == '0', logger.error(f'断言任务查询接口status_code失败,status_code为{code},res == {res.text}')
    #                 break
    #     except Exception as e:
    #         logger.error(f"任务进度查询接口发生错误：{e}")
    #         assert False, logger.error(f'断言任务查询接口发生错误,res == {res.text}')

    def async_run_iaas(self, uri, data, method="post", time_sleep=5):
        """
        异步接口,做status_code和request_id断言
        :param uri:
        :param data:
        :param method: 默认使用post请求，另外支持delete（可以添加其他）
        :param time_sleep: 默认5秒，传给查询进度接口
        :return:
        """
        allure.attach(f"""{str(data).replace("'",'"')}""", "传参")
        sign = self.postSign(data)
        global_data_iaas["header"]["Sign"] = sign
        if method == "delete":
            res = requests.delete(url=self.url + uri, json=data, headers=global_data_iaas.get("header"), verify=False)
        else:
            res = requests.post(url=self.url + uri, json=data, headers=global_data_iaas.get("header"), verify=False)
        logger.info(f'请求url--{res.url}')
        logger.info(f"""请求headers--{str(global_data_iaas.get("header")).replace("'", '"')}""")
        allure.attach(f"{res.text}", "返回值")
        res.raise_for_status()  # 抛出HTTP错误
        res_json = res.json()
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        # 同步返回的断言
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        # request_id = list(res_json.get("data").get("task_map").values())
        task_map = jsonpath.jsonpath(res_json, "$..task_map")
        assert task_map != [], logger.error(f'断言task_map失败,task_map为{task_map}')
        request_id = list(task_map[0].values())
        # logger.info(f'提取的request_id为 {request_id}')
        logger.info(f'断言成功,status_code == {status_code},request_id == {request_id}')
        # 异步任务的断言
        self.checkProgressIaas(request_id, time_sleep)
        # taskFailCount = self.checkProgressIaas(request_id, time_sleep)
        # # 判断子任务是否有失败
        # if taskFailCount != 0:
        #     assert False, logger.error(f'任务执行存在失败,失败数量:{taskFailCount},res == {res.text}')
        # else:
        #     assert True
        #     logger.info(f'任务查询为全部执行成功')

    def sync_get_run_iaas(self, uri, data=None):
        """
        同步接口,get请求,只返回res_json,用例里面自定义断言
        :param uri:
        :param data:
        :return: 返回json格式的接口返回值
        """
        allure.attach(f"""{str(data).replace("'",'"')}""", "传参")
        sign = self.getSign(data)
        global_data_iaas["header"]["Sign"] = sign
        res = requests.get(url=self.url + uri, params=data, headers=global_data_iaas.get("header"), verify=False)
        logger.info(f'请求url--{res.url}')
        logger.info(f"""请求headers--{str(global_data_iaas.get("header")).replace("'", '"')}""")
        allure.attach(f"{res.text}", "返回值")
        res.raise_for_status()  # 抛出HTTP错误
        return res.json()

    def sync_post_run_iaas(self, uri, data):
        """
        同步接口,post请求,只返回res_json,用例里面自定义断言
        :param uri:
        :param data:
        :return: 返回json格式的接口返回值
        """
        allure.attach(f"""{str(data).replace("'",'"')}""", "传参")
        sign = self.postSign(data)
        global_data_iaas["header"]["Sign"] = sign
        # logger.info(f'sign 为{sign}')
        res = requests.post(url=self.url + uri, json=data, headers=global_data_iaas.get("header"), verify=False)
        logger.info(f"请求url--{res.url}")
        logger.info(f"""请求headers--{str(global_data_iaas.get("header")).replace("'", '"')}""")
        # logger.info(f'test_instance_list res为{res.text}')
        allure.attach(f"{res.text}", "返回值")
        res.raise_for_status()  # 抛出HTTP错误
        return res.json()

    # @timeout_decorator(180)
    def check_image_upload_status_iaas(self):
        """
        查询镜像上传状态，在实例镜像上传接口中调用
        :return:
        """
        self.image_count += 1
        if self.image_count == 60:
            assert False, logger.error(f'镜像上传超时')
        time.sleep(10)
        uri = "/openApi/ListImage"
        data = {
            "image_id": global_data_iaas.get("image_id")
        }
        sign = self.postSign(data)
        global_data_iaas["header"]["Sign"] = sign
        res = requests.post(url=self.url + uri, json=data, headers=global_data_iaas.get("header"), verify=False)
        logger.info(f'第{self.image_count}次查询镜像上传状态返回值为 {res.text}')
        res.raise_for_status()  # 抛出HTTP错误
        res_json = res.json()
        status = jsonpath.jsonpath(res_json, "$..status")[0]
        if status != 0:
            allure.attach(f"--0 初始化 1 可用 2 不可用--{res.text}", "镜像上传结果")
            logger.info(f'镜像上传完成,status为{status} --0 初始化 1 可用 2 不可用')
            assert status == 1, logger.error(f'镜像上传失败,断言status失败,status为{status}')
        else:
            logger.info(f'镜像上传中,status为{status} --0 初始化 1 可用 2 不可用')
            self.check_image_upload_status_iaas()

    # @timeout_decorator(180)
    def check_backup_status_iaas(self):
        """
        查询实例备份状态，在实例备份接口中调用
        :return:
        """
        self.backup_count += 1
        if self.backup_count == 60:
            assert False, logger.error(f'实例备份超时')
        time.sleep(10)
        uri = "/openApi/DescribeBackup"
        data = {
            "backup_ids": [global_data_iaas.get("backup_id")]
        }
        sign = self.postSign(data)
        global_data_iaas["header"]["Sign"] = sign
        res = requests.post(url=self.url + uri, json=data, headers=global_data_iaas.get("header"), verify=False)
        logger.info(f'第{self.backup_count}次查询实例备份状态返回值为 {res.text}')
        res.raise_for_status()  # 抛出HTTP错误
        res_json = res.json()
        state = jsonpath.jsonpath(res_json, "$..state")[0]
        if state != "PROCESSING":
            allure.attach(f"--状态：PROCESSING、SUCCESS、FAIL--{res.text}", "实例备份结果")
            logger.info(f'实例备份完成,state为{state} --状态：PROCESSING、SUCCESS、FAIL')
            assert state == "SUCCESS", logger.error(f'实例备份失败,断言state失败,state为{state}')
        else:
            logger.info(f'实例备份中,state为{state} --状态：PROCESSING、SUCCESS、FAIL')
            self.check_backup_status_iaas()

    def check_app_upload_status_iaas(self):
        """
        查询应用上传状态，10秒一次
        :return:
        """
        self.count += 1
        if self.count == 60:
            assert False, logger.error('应用上传超时')
        time.sleep(10)
        uri = "/openApi/AppDetail"
        data = {
            "app_id": global_data_iaas.get("app_id")
        }
        sign = self.postSign(data)
        global_data_iaas["header"]["Sign"] = sign
        res = requests.post(self.url + uri, headers=global_data_iaas.get("header"), json=data, verify=False)
        res.raise_for_status()  # 抛出HTTP错误
        res_json = res.json()
        logger.info(f'第{self.count}次查询应用上传状态返回值为 {res.text}')
        app_status = jsonpath.jsonpath(res_json, "$..app_status")[0]
        if app_status != 0:
            allure.attach(f"--0.初始化 1.成功 2.失败--{res.text}", "应用上传结果")
            logger.info(f'应用上传完成,app_status为{app_status} --0.初始化 1.成功 2.失败')
            assert app_status == 1, logger.error(f'应用上传失败,断言app_status失败,app_status为{app_status}')
        else:
            logger.info(f'应用上传中,app_status为{app_status} --0.初始化 1.成功 2.失败')
            self.check_app_upload_status_iaas()

    def check_file_upload_status_iaas(self):
        """
        查询文件上传状态，10秒一次
        :return:
        """
        self.count += 1
        if self.count == 60:
            assert False, logger.error(f'文件上传超时')
        time.sleep(10)
        uri = "/openApi/FileDetail"
        data = {
            "file_ids": [global_data_iaas.get("file_id")]
        }
        sign = self.postSign(data)
        global_data_iaas["header"]["Sign"] = sign
        res = requests.post(self.url + uri, headers=global_data_iaas.get("header"), json=data, verify=False)
        res.raise_for_status()  # 抛出HTTP错误
        res_json = res.json()
        logger.info(f'第{self.count}次查询文件上传状态返回值为 {res.text}')
        status = jsonpath.jsonpath(res_json, f"$..[?(@.idc==\"{global_data_iaas.get('idc')}\")].status")[0]
        if status != 0 and status != 3:
            allure.attach(f"--0 下载中，1.成功，2.失败，3.未开始--{res.text}", "文件上传结果")
            logger.info(f'文件上传完成,status为{status} --0 下载中，1.成功，2.失败，3.未开始')
            assert status == 1, logger.error(f'文件上传失败,断言status失败,status为{status}')
        else:
            logger.info(f'文件上传中,status为{status} --0 下载中，1.成功，2.失败，3.未开始')
            self.check_file_upload_status_iaas()