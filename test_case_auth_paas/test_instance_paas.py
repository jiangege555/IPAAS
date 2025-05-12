import jsonpath, allure, random, requests, pytest, os
from test_case_auth_paas import logger
from test_case_auth_paas.baseTestCasePaas import BaseTestCasePaas, global_data_paas
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from myutils.read_yaml import read_testcase_yaml
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


@pytest.mark.run(order=5)
@pytest.mark.all
@allure.feature("paas实例相关接口")
class TestInstancePaas(BaseTestCasePaas):

    # instance_id = global_data.get("instance_id")
    # url = global_data.get("url")
    # header = global_data.get("header")
    # file_id = global_data.get("file_id")
    # app_id = global_data.get("app_id")
    # app_package = global_data.get("app_package")

    @allure.title("查询实例余量")
    # @allure.severity("normal")
    @pytest.mark.other
    def test_instance_capacity_paas(self):
        uri = "/v1/instance/capacity"
        data = {
            "vendor": global_data_paas.get("vendor"),
            "idc": global_data_paas.get("idc"),
            "cardType": global_data_paas.get("card_type"),
            "instanceType": global_data_paas.get("instance_type")
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        logger.info(f'断言成功,status == {status}')

    @allure.title("实例订购")
    # @allure.severity("normal")
    @pytest.mark.smoke
    @pytest.mark.dependency()
    def test_instance_subscribe_paas(self):
        global subcids
        subcids = []
        uri = "/v1/instance/subscribe"
        data = {
            "vendor": global_data_paas.get("vendor"),
            "idc": global_data_paas.get("idc"),
            "cardType": global_data_paas.get("card_type"),
            "instanceType": global_data_paas.get("instance_type"),
            "amount": global_data_paas.get("amount")
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        instanceId = jsonpath.jsonpath(res_json, "$..instanceId")
        assert instanceId != False, logger.error(f'断言instanceId失败,instanceId{instanceId}')
        subcids = instanceId
        # logger.info(subcids)
        logger.info(f'断言成功,status == {status},instanceId == {instanceId}')

    @allure.story("查询实例列表")
    # @allure.severity("critical")
    @pytest.mark.parametrize("case_info", [
        pytest.param(
            case,  # 直接传递整个字典
            # marks=getattr(pytest.mark, case["mark"]),  # 动态获取 mark
            marks=[getattr(pytest.mark, mark) for mark in case.get('mark', [])],  # 动态获取 mark
            id=case["name"]
        )
        for case in read_testcase_yaml(f"{os.getcwd()}/test_case_auth_paas/instanceList.yaml", "test_instance_list", global_data_paas)
    ])
    def test_list_paas(self, case_info):
        self.case_handle(case_info)

    @allure.title("查询实例列表V1")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_list_paas(self):
        uri = "/v1/instance/list"
        data = {
            "idcs": [global_data_paas.get("idc")],
            "vendor": global_data_paas.get("vendor")
            }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert total > 0, logger.error(f'断言total失败,total为{total}')
        # instance_ids = jsonpath.jsonpath(res_json, "$..instanceId")
        # global_data["instance_ids"] = instance_ids
        # logger.info(f'提取的instance_ids: {instance_ids}')
        logger.info(f'断言成功,status == {status},total == {total}')

    @allure.title("查询实例列表V2")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_list2_paas(self):
        uri = "/v2/instance/list"
        data = {
            "idcs": [global_data_paas.get("idc")],
            "vendor": global_data_paas.get("vendor")
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert total > 0, logger.error(f'断言total失败,total为{total}')
        logger.info(f'断言成功,status == {status},total == {total}')

    @allure.title("实例退订")
    # @allure.severity("normal")
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestInstancePaas::test_instance_subscribe_paas"])
    def test_instance_unsubscribe_paas(self):
        # logger.info(subcids)
        uri = "/v1/instance/unsubscribe"
        data = {
            "instanceIds": subcids
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        logger.info(f'断言成功,status == {status}')

    @allure.title("实例控制Token获取")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_control_token_paas(self):
        uri = "/v1/instance/control/token/get"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "deviceId": "123123",
            "renewalTime": 48
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        token = jsonpath.jsonpath(res_json, "$..token")
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert token != False, logger.error(f'断言token失败,token为{token}')
        logger.info(f'断言成功,status == {status},token == {token[0]}')

    @allure.title("实例控制Token获取V2")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_control_token2_paas(self):
        uri = "/v2/instance/control/token/get"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "deviceId": "123123",
            "renewalTime": 48
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        token = jsonpath.jsonpath(res_json, "$..token")
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert token != False, logger.error(f'断言token失败,token为{token}')
        logger.info(f'断言成功,status == {status},token == {token[0]}')

    @allure.title("实例推流Token获取")
    # @allure.severity("critical")
    @pytest.mark.important
    def test_instance_stream_token_paas(self):
        uri = "/v1/instance/stream/token/get"
        data = {
            "instanceId": global_data_paas.get("instance_ids")[0],
            "deviceId": "123123",
            "renewalTime": 48
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        token = jsonpath.jsonpath(res_json, "$..token")
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert token != False, logger.error(f'断言token失败,token为{token}')
        logger.info(f'断言成功,status == {status},token == {token[0]}')

    @allure.title("实例推流Token批量获取")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_stream_token_batch_paas(self):
        uri = "/v1/instance/stream/token/batch/get"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "deviceId": "123123",
            "renewalTime": 48
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        token = jsonpath.jsonpath(res_json, "$..token")
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert token != False, logger.error(f'断言token失败,token为{token}')
        logger.info(f'断言成功,status == {status},token == {token[0]}')

    @allure.title("实例推流Token获取V2")
    # @allure.severity("critical")
    @pytest.mark.important
    def test_instance_stream_tokenV2_paas(self):
        uri = "/v2/instance/stream/token/get"
        data = {
            "instanceId": global_data_paas.get("instance_ids")[0],
            "deviceId": "123123",
            "renewalTime": 48
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        token = jsonpath.jsonpath(res_json, "$..token")
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert token != False, logger.error(f'断言token失败,token为{token}')
        logger.info(f'断言成功,status == {status},token == {token[0]}')

    @allure.title("实例推流Token批量获取V2")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_stream_tokenV2_batch_paas(self):
        uri = "/v2/instance/stream/token/batch/get"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "deviceId": "123123",
            "renewalTime": 48
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        token = jsonpath.jsonpath(res_json, "$..token")
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert token != False, logger.error(f'断言token失败,token为{token}')
        logger.info(f'断言成功,status == {status},token == {token[0]}')

    @allure.title("获取实例SSH连接信息")
    # @allure.severity("normal")
    @pytest.mark.other
    def test_instance_ssh_paas(self):
        uri = "/v1/instance/ssh/get"
        data = {
            "instanceId": global_data_paas.get("instance_ids")[0]
        }
        res_json = self.sync_get_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        sshUrl = jsonpath.jsonpath(res_json, "$..sshUrl")
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert sshUrl != False, logger.error(f'断言sshUrl失败,sshUrl为{sshUrl}')
        logger.info(f'断言成功,status == {status},sshUrl == {sshUrl[0]}')

    @allure.title("获取实例ADB信息")
    # @allure.severity("normal")
    @pytest.mark.other
    def test_instance_adb_paas(self):
        uri = "/v1/instance/adb/get"
        data = {
            "instanceId": global_data_paas.get("instance_ids")[0]
        }
        res_json = self.sync_get_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        adbIp = jsonpath.jsonpath(res_json, "$..adbIp")
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert adbIp != False, logger.error(f'断言adbIp失败,adbIp为{adbIp}')
        logger.info(f'断言成功,status == {status},adbIp == {adbIp[0]}')

    @allure.title("终止实例推流")
    # @allure.severity("normal")
    @pytest.mark.other
    def test_instance_stream_stop_paas(self):
        uri = "/v1/instance/stream/stop"
        data = {
            "instanceId": global_data_paas.get("instance_ids")[0]
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        # sshUrl = jsonpath.jsonpath(res_json, "$..sshUrl")
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        # assert sshUrl != False, logger.error(f'断言sshUrl失败,sshUrl为{sshUrl}')
        logger.info(f'断言成功,status == {status}')

    @allure.title("实例异步执行命令")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_cmd_async_paas(self):
        uri = "/v1/instance/cmd/async/run"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "command": "date",
            "timeout": 10
        }
        self.async_run_paas(uri, data)
        # task_id = self.async_run_paas(uri, data)
        # task_name = "实例异步执行命令"
        # global_data["taskIds"].append({"task_name": task_name, "task_id": task_id})

    @allure.title("实例限速设置")
    # @allure.severity("normal")
    @pytest.mark.other
    def test_instance_bandwidth_paas(self):
        uri = "/v1/instance/bandwidth/set"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "downstream": random.randint(10, 30),
            "upstream": random.randint(10, 30)
        }
        self.async_run_paas(uri, data)

    @allure.title("实例内存设置")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_memory_paas(self):
        mems = [2048, 3072, 4096, 5120, 6144, 7168, 8192, 9216, 10240]
        uri = "/v1/instance/memory/set"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "memorySize": random.choice(mems)
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        substatus = jsonpath.jsonpath(res_json, "$.data..status")
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert substatus != False, logger.error(f'断言子status失败,子status为{substatus}')
        logger.info(f'断言成功,status == {status},substatus == {substatus[0]}')

    @allure.title("实例截图")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_screenCapture_paas(self):
        uri = "/v1/instance/screen/capture"
        data = {
            "instanceIds": global_data_paas.get("instance_ids")
        }
        self.async_run_paas(uri, data)
        # task_id = self.async_run_paas(uri, data)
        # task_name = "实例截图"
        # global_data["taskIds"].append({"task_name": task_name, "task_id": task_id})

    @allure.title("实例屏幕截图V2（异步）")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_screen_async_paas(self):
        uri = "/v2/instance/screen/capture/async"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "localStorage": True
        }
        self.async_run_paas(uri, data)

    @allure.title("实例文件上传")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_fileUpload_paas(self):
        global_data_paas["file_id"] = self.file_list()[0]
        logger.info(f'本次上传的文件id为:{global_data_paas.get("file_id")}')
        uri = "/v1/instance/file/upload"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "path": "/data",
            "fileId": global_data_paas.get("file_id")
        }
        self.async_run_paas(uri, data)

    @allure.title("实例文件上传到相册")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_fileUploadToDCIM_paas(self):
        global_data_paas["file_id"] = self.file_list()[0]
        logger.info(f'本次上传的文件id为:{global_data_paas.get("file_id")}')
        uri = "/v1/instance/file/uploadToPhoto"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "fileId": global_data_paas.get("file_id")
        }
        self.async_run_paas(uri, data)

    @allure.title("实例换肤")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_skinRefresh_paas(self):
        self.get_machine_list()
        uri = "/v1/instance/skin/refresh"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "brand": global_data_paas.get("brand"),
            "model": global_data_paas.get("model")
        }
        self.async_run_paas(uri, data)

    @allure.title("实例备份")
    # @allure.severity("normal")
    @pytest.mark.important
    @pytest.mark.smoke
    @pytest.mark.dependency()
    def test_instance_dataBackup_paas(self):
        global instance_backup
        instance_backup = random.choice(global_data_paas.get("instance_ids"))
        uri = "/v1/instance/data/backup"
        data = {
            "instanceId": instance_backup,
            "path": "/data/"
        }
        allure.attach(f"{data}", "传参")
        sign = self.post_auth(data)
        global_data_paas["header"]["Sign"] = sign
        res = requests.post(url=self.url + uri, json=data, headers=global_data_paas.get("header"), verify=False)
        logger.info(f'请求url--{res.url}')
        logger.info(f'请求headers--{res.headers}')
        # logger.info(f'test_instance_list res为{res.text}')
        allure.attach(f"{res.text}", "返回值")
        res.raise_for_status()  # 抛出HTTP错误
        res_json = res.json()
        status = jsonpath.jsonpath(res_json, "status")[0]
        taskId = jsonpath.jsonpath(res_json, "$..taskId")
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert taskId != False, logger.error(f'断言taskId失败,taskId为{taskId}')
        logger.info(f'断言成功,status == {status},taskId == {taskId[0]}')
        global_data_paas["backup_id"] = jsonpath.jsonpath(res_json, "$..backupId")[0]
        self.checkProgressPaas(taskId[0], 10)

    @allure.title("实例换机")
    # @allure.severity("normal")
    @pytest.mark.important
    @pytest.mark.smoke
    def test_instance_dataReplace_paas(self):
        uri = "/v1/instance/data/replace"
        data = {
            "sourceInstanceId": global_data_paas.get("instance_ids")[2],
            "targetInstanceId": global_data_paas.get("instance_ids")[3]
        }
        self.async_run_paas(uri, data, 10)

    @allure.title("实例还原")
    # @allure.severity("normal")
    @pytest.mark.important
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestInstancePaas::test_instance_dataBackup_paas"])
    def test_instance_dataRestore_paas(self):
        instances = global_data_paas.get("instance_ids").copy()
        instances.remove(instance_backup)
        uri = "/v1/instance/data/restore"
        data = {
            "instanceIds": instances,
            "backupId": global_data_paas.get("backup_id")
        }
        self.async_run_paas(uri, data, 10)

    @allure.title("实例恢复出厂")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_recovery_paas(self):
        uri = "/v1/instance/recovery"
        data = {
            "instanceIds": global_data_paas.get("instance_ids")
        }
        self.async_run_paas(uri, data, 10)

    @allure.title("实例重启")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_reboot_paas(self):
        uri = "/v1/instance/reboot"
        data = {
            "instanceIds": global_data_paas.get("instance_ids")
        }
        self.async_run_paas(uri, data)

    @allure.title("实例关机")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_stop_paas(self):
        uri = "/v1/instance/stop"
        data = {
            "instanceIds": global_data_paas.get("instance_ids")
        }
        self.async_run_paas(uri, data)

    @allure.title("实例开机")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_start_paas(self):
        uri = "/v1/instance/start"
        data = {
            "instanceIds": global_data_paas.get("instance_ids")
        }
        self.async_run_paas(uri, data)

    @allure.title("查询机型列表")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_machine_paas(self):
        uri = "/v1/instance/machine/get"
        data = {
            "instanceId": global_data_paas.get("instance_ids")[0]
        }
        res_json = self.sync_get_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        data = jsonpath.jsonpath(res_json, "$.data")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert len(data) > 0, logger.error(f'断言data失败,data为{data}')
        logger.info(f'断言成功,status == {status},data == {data}')

