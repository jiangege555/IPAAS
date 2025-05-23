import allure, jsonpath, time, re, random, json
from test_case_auth_paas import logger, global_data_paas
from myutils.my_request import my_request
from myutils.my_request import session
from string import Template
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# # 禁用安全请求警告
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class BaseTestCasePaas:

    url = global_data_paas.get("url")
    task_id = ""
    count = 0

    def get_auth(self, data=None):
        """
        get请求鉴权
        :param data: {}格式
        :return:
        """
        url = self.url + "/v1/get/sign"
        global_data_paas["header"]["Sign"] = "111111"
        res = session.get(url=url, headers=global_data_paas.get("header"), params=data, verify=False)
        try:
            res_text = res.text
            if res.status_code != 200:
                Sign = re.findall(r'serverSign\\":\\"(\w+)\\",', res_text)[0]
            else:
                Sign = global_data_paas.get("header")["Sign"]
        except Exception as e:
            Sign = "111111"
            logger.error(f"鉴权请求发生错误：postSign--{res.text}")
        return Sign

    def post_auth(self, data):
        """
        post请求鉴权
        :param data: {}格式
        :return:
        """
        url = self.url + "/v1/post/sign"
        global_data_paas["header"]["Sign"] = "111111"
        res = session.post(url=url, headers=global_data_paas.get("header"), json=data, verify=False)
        try:
            res_text = res.text
            if res.status_code != 200:
                Sign = re.findall(r'serverSign\\":\\"(\w+)\\",', res_text)[0]
            else:
                Sign = global_data_paas.get("header")["Sign"]
            # print(Sign)
        except Exception as e:
            Sign = "111111"
            logger.error(f"鉴权请求发生错误：postSign--{res.text}")
        return Sign

    def checkProgressPaas(self, task_id, time_sleep=5):
        """
        任务进度查询，先查询总任务状态，完成后再查询子任务是否存在失败
        :param task_id: 总任务id，int格式
        :param time_sleep: 默认5秒查询一次
        :return:
        """
        # print(task_ids)
        self.count += 1
        time.sleep(time_sleep)
        uri = f"/v1/task/list"
        if task_id != self.task_id:
            logger.info(f'查询中的任务id--{task_id}')
            self.task_id = task_id
            sign = self.get_auth({"taskId": task_id})
            global_data_paas["header"]["Sign"] = sign
            logger.info(f"""请求headers--{str(global_data_paas.get("header")).replace("'", '"')}""")
        res = session.get(url=self.url + uri, params={"taskId": task_id}, headers=global_data_paas.get("header"), verify=False)
        if self.count == 90:
            assert False, logger.error(f'任务执行超时,已查询{self.count}次任务结果,res == {res.text}')
        res.raise_for_status()  # 抛出HTTP错误
        res_json = res.json()
        # print(res_json)
        code = jsonpath.jsonpath(res_json, "$.status")[0]
        if str(code) == '0':
            status = jsonpath.jsonpath(res_json, "$..taskStatus")[0]
            # 判断主任务是否执行成功
            if str(status) == "1":
                subTaskFailCount = jsonpath.jsonpath(res_json, "$..subTaskFailCount")[0]
                # logger.info(f'任务执行')
                # return subTaskFailCount
                # 判断子任务是否有失败，有失败调用子任务查询接口，打印详细信息
                if subTaskFailCount != 0:
                    res_detail = session.get(url=self.url + f"/v1/subtask/list", params={"taskId": task_id},
                                              headers=global_data_paas.get("header"), verify=False)
                    # logger.error(f'任务执行失败数量:{subTaskFailCount}')
                    allure.attach(f"子任务查询详情--失败数量:{subTaskFailCount}-- {res_detail.text}", name="异步任务失败信息")
                    assert False, logger.error(f'任务执行存在失败,失败数量:{subTaskFailCount},res == {res_detail.text}')
                else:
                    assert True
                    allure.attach(f"任务查询详情--失败数量:{subTaskFailCount}-- {res.text}", name="异步任务成功信息")
                    logger.info(f'断言任务查询为全部执行成功,失败数量:{subTaskFailCount},res == {res.text}')
            else:
                # 主任务未成功继续查询
                self.checkProgressPaas(task_id)
        else:
            assert False, logger.error(f'断言任务查询接口status失败,status为{code},res == {res.text}')

    def async_run_paas(self, uri, data, time_sleep=5):
        """
        异步接口,做status和task_id断言
        :param uri:
        :param data:
        :param time_sleep: 默认5秒，传给查询进度接口
        :return:
        """
        allure.attach(f"""{str(data).replace("'",'"')}""", "传参")
        sign = self.post_auth(data)
        global_data_paas["header"]["Sign"] = sign
        res = session.post(url=self.url + uri, json=data, headers=global_data_paas.get("header"), verify=False)
        logger.info(f'请求url--{res.url}')
        logger.info(f"""请求headers--{str(global_data_paas.get("header")).replace("'", '"')}""")
        allure.attach(f"{res.text}", "返回值")
        res.raise_for_status()  # 抛出HTTP错误
        res_json = res.json()
        status = jsonpath.jsonpath(res_json, "status")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        taskId = jsonpath.jsonpath(res_json, "$..taskId")
        assert taskId != False, logger.error(f'断言taskId失败,taskId为{taskId}')
        logger.info(f'断言成功,status == {status},taskId == {taskId[0]}')
        self.checkProgressPaas(taskId[0], time_sleep)

    def sync_get_run_paas(self, uri, data=None):
        """
        同步接口,get请求,只返回res_json,用例里面自定义断言
        :param uri:
        :param data:
        :return: 返回json格式的接口返回值
        """
        allure.attach(f"""{str(data).replace("'",'"')}""", "传参")
        sign = self.get_auth(data)
        global_data_paas["header"]["Sign"] = sign
        res = session.get(url=self.url + uri, params=data, headers=global_data_paas.get("header"), verify=False)
        logger.info(f'请求url--{res.url}')
        logger.info(f"""请求headers--{str(global_data_paas.get("header")).replace("'", '"')}""")
        allure.attach(f"{res.text}", "返回值")
        res.raise_for_status()  # 抛出HTTP错误
        return res.json()

    def sync_post_run_paas(self, uri, data):
        """
        同步接口,post请求,只返回res_json,用例里面自定义断言
        :param uri:
        :param data:
        :return: 返回json格式的接口返回值
        """
        allure.attach(f"""{str(data).replace("'",'"')}""", "传参")
        sign = self.post_auth(data)
        global_data_paas["header"]["Sign"] = sign
        # logger.info(f'sign 为{sign}')
        res = session.post(url=self.url + uri, json=data, headers=global_data_paas.get("header"), verify=False)
        logger.info(f'请求url--{res.url}')
        logger.info(f"""请求headers--{str(global_data_paas.get("header")).replace("'", '"')}""")
        # logger.info(f'test_instance_list res为{res.text}')
        allure.attach(f"{res.text}", "返回值")
        res.raise_for_status()  # 抛出HTTP错误
        return res.json()

    def app_list(self):
        """
        查询ak下的可用app，返回id和package列表
        :return:
        """
        uri = "/v1/app/list"
        data = {
        }
        sign = self.post_auth(data)
        global_data_paas["header"]["Sign"] = sign
        res = session.post(self.url + uri, headers=global_data_paas.get("header"), json=data, verify=False)
        res.raise_for_status()  # 抛出HTTP错误
        logger.info(f'应用列表返回值--{res.text}')
        res_json = res.json()
        appIds = jsonpath.jsonpath(res_json, "$.data.records[?(@.status==2)].appId")
        appPackages = jsonpath.jsonpath(res_json, "$.data.records[?(@.status==2)].packageName")
        l = len(appIds)
        i = random.randint(0, l - 1)
        global_data_paas["app_id"] = appIds[i]
        global_data_paas["app_package"] = appPackages[i]
        logger.info(f'本次安装的app_id:{global_data_paas.get("app_id")}, app_package:{global_data_paas.get("app_package")}')
        return appIds, appPackages

    def file_list(self):
        """
        查询ak下的可用file，返回id列表
        :return:
        """
        uri = "/v1/file/list"
        data = {
        }
        sign = self.post_auth(data)
        global_data_paas["header"]["Sign"] = sign
        res = session.post(self.url + uri, headers=global_data_paas.get("header"), json=data, verify=False)
        res.raise_for_status()  # 抛出HTTP错误
        logger.info(f'文件列表返回值--{res.text}')
        res_json = res.json()
        fileIds = jsonpath.jsonpath(res_json, "$.data.records[?(@.fileStatus==2)].fileId")
        return fileIds

    def instance_list(self):
        """
        查询ak下指定机房和供应商的实例，返回实例id列表
        :return:
        """
        uri = "/v1/instance/list"
        data = {
            "idcs": [global_data_paas.get("idc")],
            "vendor": global_data_paas.get("vendor")
            }
        sign = self.post_auth(data)
        global_data_paas["header"]["Sign"] = sign
        res = session.post(self.url + uri, headers=global_data_paas.get("header"), json=data, verify=False)
        res.raise_for_status()  # 抛出HTTP错误
        res_json = res.json()
        instanceIds = jsonpath.jsonpath(res_json, "$..instanceId")
        return instanceIds

    def get_machine_list(self):
        """
        查询平台可用的机型列表，返回列表
        :return:
        """
        uri = "/v1/instance/machine/get"
        sign = self.get_auth()
        global_data_paas["header"]["Sign"] = sign
        res = session.get(self.url + uri, headers=global_data_paas.get("header"), verify=False)
        logger.info(f'查询设备机型返回值--{res.text}')
        res.raise_for_status()  # 抛出HTTP错误
        res_json = res.json()
        datas = jsonpath.jsonpath(res_json, "$.data")
        if datas:
            logger.info(f'平台支持的设备类型为 {datas[0]}')
            machine = random.choice(datas[0])
            global_data_paas["brand"] = machine.get("brand")
            global_data_paas["model"] = random.choice(machine.get("models"))
            logger.info(f'本次换肤的brand:{global_data_paas.get("brand")}, model:{global_data_paas.get("model")}')
        else:
            dataset = {'brand': 'OnePlus', 'models': ['PHK110', 'PJA110', 'PHB110']}
            logger.info(f'平台平台没找到设备类型,自定义设备类型为 {dataset}')
            global_data_paas["brand"] = dataset.get("brand")
            global_data_paas["model"] = random.choice(dataset.get("models"))

    def case_handle(self, case_info, time_sleep=5):
        """
        参数化执行测试用例时，yaml测试用例的处理
        :param case_info:
        :return:
        """
        name = case_info.get("name")
        allure.dynamic.title(name)
        url = self.url + case_info.get("request").get("url")
        data = case_info.get("request").get("data")
        method = case_info.get("request").get("method")
        is_async = case_info.get("request").get("async")
        before_request = case_info.get("before_request")
        if before_request:
            for func in before_request:
                if hasattr(self, func):
                    func = getattr(self, func)
                    func()
                    temp = Template(json.dumps(data))
                    data = json.loads(temp.safe_substitute(global_data_paas))
        after_request = case_info.get("after_request")
        extract = case_info.get("extract")
        validate = case_info.get("validate")
        if not data:
            data = {}
        allure.attach(f"""{str(data).replace("'", '"')}""", "传参")
        sign = self.post_auth(data)
        global_data_paas["header"]["Sign"] = sign
        res = my_request(url=url, data=data, method=method, headers=global_data_paas.get("header"), verify=False)
        logger.info(f'请求url--{res.url}')
        logger.info(f"""请求headers--{str(global_data_paas.get("header")).replace("'", '"')}""")
        allure.attach(f"{res.text}", "返回值")
        res.raise_for_status()  # 抛出HTTP错误
        res_json = res.json()
        if extract:
            for item in extract:
                if list(item.values())[0].get("type") == "json":
                    self.extract_json(res=res_json, **item)
        if after_request:
            for func in after_request:
                if hasattr(self, func):
                    func = getattr(self, func)
                    func()
        if validate:
            for item in validate:
                if list(item.values())[0].get("type") == "json":
                    self.validate_json(res=res_json, **item)
        if is_async:
            taskId = jsonpath.jsonpath(res_json, "$..taskId")
            assert taskId != False, logger.error(f'断言taskId失败,taskId为{taskId}')
            logger.info(f'断言taskId成功,taskId == {taskId[0]}')
            self.checkProgressPaas(taskId[0], time_sleep)

    def extract_json(self, res, **kwargs):
        try:
            for k, v in kwargs.items():
                path = v.get("path")
                index = v.get("index")
                value = jsonpath.jsonpath(res, path)
                if value != False:
                    if index == -1:
                        global_data_paas[k] = value
                    else:
                        value = value[index]
                        global_data_paas[k] = value
                    logger.info(f'提取的变量为{k},值为{value}')
                else:
                    logger.error(f'提取value失败,值为{value}')
        except Exception as e:
            logger.error(f'提取value异常,{repr(e)}')

    def validate_json(self, res, **kwargs):
        try:
            for k, v in kwargs.items():
                path = v.get("path")
                index = v.get("index")
                sign = v.get("sign")
                value_expect = v.get("value")
                value_actual = jsonpath.jsonpath(res, path)
                if value_actual != False:
                    if index == -1:
                        value_actual = value_actual
                    else:
                        value_actual = value_actual[index]
                    if sign == "eq":
                        assert value_actual == value_expect, logger.error(f'断言失败,实际值{value_actual},预期值{value_expect}')
                        logger.info(f'断言成功,实际值{value_actual}==预期值{value_expect}')
                    elif sign == "ne":
                        assert value_actual != value_expect, logger.error(f'断言失败,实际值{value_actual},预期值{value_expect}')
                        logger.info(f'断言成功,实际值{value_actual}!=预期值{value_expect}')
                    elif sign == "lt":
                        assert value_actual < value_expect, logger.error(f'断言失败,实际值{value_actual},预期值{value_expect}')
                        logger.info(f'断言成功,实际值{value_actual}<预期值{value_expect}')
                    elif sign == "gt":
                        assert value_actual > value_expect, logger.error(f'断言失败,实际值{value_actual},预期值{value_expect}')
                        logger.info(f'断言成功,实际值{value_actual}>预期值{value_expect}')
                    elif sign == "le":
                        assert value_actual <= value_expect, logger.error(f'断言失败,实际值{value_actual},预期值{value_expect}')
                        logger.info(f'断言成功,实际值{value_actual}<=预期值{value_expect}')
                    elif sign == "ge":
                        assert value_actual >= value_expect, logger.error(f'断言失败,实际值{value_actual},预期值{value_expect}')
                        logger.info(f'断言成功,实际值{value_actual}>=预期值{value_expect}')
                    elif sign == "in":
                        assert value_expect in value_actual, logger.error(f'断言失败,实际值{value_actual},预期值{value_expect}')
                        logger.info(f'断言成功,实际值{value_actual} in 预期值{value_expect}')
                    elif sign == "nin":
                        assert value_expect not in value_actual, logger.error(f'断言失败,实际值{value_actual},预期值{value_expect}')
                        logger.info(f'断言成功,实际值{value_actual} not in 预期值{value_expect}')
                    else:
                        assert False, logger.error(f'断言处理失败,实际值{value_actual},预期值{value_expect},sign为{sign}')
                else:
                    assert False, logger.error(f'断言value失败,值为{value_actual}')
        except Exception as e:
            assert False, logger.error(f'断言处理异常,{repr(e)}')

    def check_app_upload_status_paas(self):
        self.count += 1
        if self.count == 60:
            assert False, logger.error(f'应用上传超时')
        time.sleep(10)
        uri = "/v1/app/list"
        data = {
            "appId": global_data_paas.get("app_id")
        }
        sign = self.post_auth(data)
        global_data_paas["header"]["Sign"] = sign
        res = session.post(self.url + uri, headers=global_data_paas.get("header"), json=data, verify=False)
        res.raise_for_status()  # 抛出HTTP错误
        res_json = res.json()
        logger.info(f'第{self.count}次查询应用上传状态返回值为 {res.text}')
        status = jsonpath.jsonpath(res_json, "$.data..status")[0]
        if status != 1:
            allure.attach(f"--1.上传中 2.成功 3.失败--{res.text}","应用上传结果")
            logger.info(f'应用上传完成,status为{status} --1.上传中 2.成功 3.失败')
            assert status == 2, logger.error(f'应用上传失败,断言status失败,status为{status}')
        else:
            logger.info(f'应用上传中,status为{status} --1.上传中 2.成功 3.失败')
            self.check_app_upload_status_paas()

    def check_app_exits_paas(self):
        uri = "/v1/app/list"
        data = {
            "remark": global_data_paas.get("app_remark")
        }
        sign = self.post_auth(data)
        global_data_paas["header"]["Sign"] = sign
        res = session.post(self.url + uri, headers=global_data_paas.get("header"), json=data, verify=False)
        res.raise_for_status()  # 抛出HTTP错误
        res_json = res.json()
        logger.info(f'查询应用返回值为 {res.text}')
        appId = jsonpath.jsonpath(res_json, "$..appId")
        # 如果存在该应用则先删除
        if appId:
            uri = "/v1/app/delete"
            data = {
                "appIds": appId
            }
            sign = self.post_auth(data)
            global_data_paas["header"]["Sign"] = sign
            session.post(self.url + uri, headers=global_data_paas.get("header"), json=data, verify=False)
            logger.info(f'应用已存在,appId为{appId[0]},已删除')

    def check_file_upload_status_paas(self):
        self.count += 1
        if self.count == 60:
            assert False, logger.error(f'文件上传超时')
        time.sleep(10)
        uri = "/v1/file/list"
        data = {
            "fileId": global_data_paas.get("file_id")
        }
        sign = self.post_auth(data)
        global_data_paas["header"]["Sign"] = sign
        res = session.post(self.url + uri, headers=global_data_paas.get("header"), json=data, verify=False)
        res.raise_for_status()  # 抛出HTTP错误
        res_json = res.json()
        logger.info(f'第{self.count}次查询文件状态返回值为 {res.text}')
        status = jsonpath.jsonpath(res_json, "$.data..fileStatus")[0]
        if status != 1:
            allure.attach(f"--1 上传中 2 成功 3 失败--{res.text}", "文件上传结果")
            logger.info(f'文件上传完成,fileStatus为{status} --1 上传中 2 成功 3 失败')
            assert status == 2, logger.error(f'文件上传失败,断言fileStatus失败,fileStatus为{status}')
        else:
            logger.info(f'文件上传中,fileStatus为{status} --1 上传中 2 成功 3 失败')
            self.check_file_upload_status_paas()

    def check_file_exits_paas(self):
        uri = "/v1/file/list"
        data = {
            "fileName": global_data_paas.get("file_name")
        }
        sign = self.post_auth(data)
        global_data_paas["header"]["Sign"] = sign
        res = session.post(self.url + uri, headers=global_data_paas.get("header"), json=data, verify=False)
        res.raise_for_status()  # 抛出HTTP错误
        res_json = res.json()
        logger.info(f'查询文件返回值为 {res.text}')
        fileId = jsonpath.jsonpath(res_json, "$..fileId")
        # 判断文件是否已存在，存在则删除
        if fileId:
            uri = "/v1/file/delete"
            data = {
                "fileIds": fileId
            }
            sign = self.post_auth(data)
            global_data_paas["header"]["Sign"] = sign
            session.post(self.url + uri, headers=global_data_paas.get("header"), json=data, verify=False)
            logger.info(f'文件已存在,fileId为{fileId[0]},已删除')

