import jsonpath, allure, pytest
from test_case_auth_paas import logger
from test_case_auth_paas.baseTestCasePaas import BaseTestCasePaas, global_data_paas


@pytest.mark.run(order=3)
@pytest.mark.all
@allure.feature("paas群控相关接口")
class TestStreamPaas(BaseTestCasePaas):

    @allure.title("创建群控会话")
    # @allure.severity("critical")
    @pytest.mark.smoke
    @pytest.mark.dependency()
    def test_stream_create_paas(self):
        # global_data["instance_ids"] = self.instance_list()
        uri = "/v1/multiple/stream/session/create"
        data = {
            "masterInstanceId": global_data_paas.get("instance_ids")[0],
            "slaveInstanceIds": global_data_paas.get("instance_ids")[1:3]
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        sessionId = jsonpath.jsonpath(res_json, "$.data.sessionId")
        failInstanceIds = jsonpath.jsonpath(res_json, "$.data.failInstanceIds")
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert sessionId != False, logger.error(f'断言sessionId失败,sessionId为{sessionId}')
        assert failInstanceIds[0] == [], logger.error(f'断言failInstanceIds失败,failInstanceIds为{failInstanceIds}')
        global_data_paas["session_id"] = sessionId[0]
        logger.info(f'断言status成功,status为{status},sessionId为{sessionId[0]},failInstanceIds为{failInstanceIds[0]}')

    @allure.title("群控会话续期")
    # @allure.severity("critical")
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestStreamPaas::test_stream_create_paas"])
    def test_stream_renewal_paas(self):
        uri = "/v1/multiple/stream/session/renewal"
        data = {
            "sessionId": global_data_paas.get("session_id"),
            "renewalTime": 2
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        logger.info(f'断言status成功,status为{status}')

    @allure.title("从控设备选定")
    # @allure.severity("critical")
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestStreamPaas::test_stream_create_paas"])
    def test_stream_slaveAvailable_paas(self):
        uri = "/v1/multiple/stream/session/slave/available"
        data = {
            "sessionId": global_data_paas.get("session_id"),
            "slaveInstanceIds": global_data_paas.get("instance_ids")[1:3]
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        logger.info(f'断言status成功,status为{status}')

    @allure.title("从控设备选定详情")
    # @allure.severity("critical")
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestStreamPaas::test_stream_create_paas"])
    def test_stream_slaveAvailableDetail_paas(self):
        uri = "/v1/multiple/stream/session/slave/available/detail"
        data = {
            "sessionId": global_data_paas.get("session_id")
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        availableInstanceIds = jsonpath.jsonpath(res_json, "$.data.availableInstanceIds")
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert set(availableInstanceIds[0]) == set(global_data_paas.get("instance_ids")[1:3]), logger.error(f'断言availableInstanceIds失败,availableInstanceIds为{availableInstanceIds}')
        logger.info(f'断言status成功,status为{status},availableInstanceIds为{availableInstanceIds[0]}')

    @allure.title("同屏推流会话列表")
    # @allure.severity("critical")
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestStreamPaas::test_stream_create_paas"])
    def test_stream_list_paas(self):
        uri = "/v1/multiple/stream/session/list"
        data = {
            "sessionId": global_data_paas.get("session_id")
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        sessionId = jsonpath.jsonpath(res_json, "$.data.records[0].sessionId")
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert sessionId[0] == global_data_paas.get("session_id"), logger.error(f'断言sessionId失败,sessionId为{sessionId})')
        logger.info(f'断言status成功,status为{status},sessionId为{sessionId[0]}')

    @allure.title("添加从控实例")
    # @allure.severity("critical")
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestStreamPaas::test_stream_create_paas"])
    def test_stream_add_paas(self):
        uri = "/v1/multiple/stream/session/slave/switch"
        data = {
            "sessionId": global_data_paas.get("session_id"),
            "type": 1,
            "slaveInstanceIds": [global_data_paas.get("instance_ids")[3]]
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        successInstanceIds = jsonpath.jsonpath(res_json, "$.data.successInstanceIds")
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert successInstanceIds[0] == [global_data_paas.get("instance_ids")[3]], logger.error(f'断言sessionId失败,successInstanceIds为{successInstanceIds[0]})')
        logger.info(f'断言status成功,status为{status},successInstanceIds为{successInstanceIds[0][0]}')

    @allure.title("删除从控实例")
    # @allure.severity("critical")
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestStreamPaas::test_stream_create_paas"])
    def test_stream_del_paas(self):
        uri = "/v1/multiple/stream/session/slave/switch"
        data = {
            "sessionId": global_data_paas.get("session_id"),
            "type": 2,
            "slaveInstanceIds": [global_data_paas.get("instance_ids")[3]]
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        successInstanceIds = jsonpath.jsonpath(res_json, "$.data.successInstanceIds")
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert successInstanceIds[0] == [global_data_paas.get("instance_ids")[3]], logger.error(f'断言sessionId失败,successInstanceIds为{successInstanceIds[0]})')
        logger.info(f'断言status成功,status为{status},successInstanceIds为{successInstanceIds[0][0]}')

    @allure.title("主屏控制权切换")
    # @allure.severity("critical")
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestStreamPaas::test_stream_create_paas"])
    def test_stream_del_paas(self):
        uri = "/v1/multiple/stream/session/master/switch"
        data = {
            "sessionId": global_data_paas.get("session_id"),
            "masterInstanceId": global_data_paas.get("instance_ids")[1]
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        logger.info(f'断言status成功,status为{status}')

    @allure.title("同屏推流会话详情")
    # @allure.severity("critical")
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestStreamPaas::test_stream_create_paas"])
    def test_stream_get_paas(self):
        uri = "/v1/multiple/stream/session/get"
        data = {
            "sessionId": global_data_paas.get("session_id")
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        sessionId = jsonpath.jsonpath(res_json, "$.data.sessionId")
        masterInstanceId = jsonpath.jsonpath(res_json, "$.data.masterInstanceId")
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert sessionId[0] == global_data_paas.get("session_id"), logger.error(f'断言sessionId失败,sessionId为{sessionId})')
        assert masterInstanceId[0] == global_data_paas.get("instance_ids")[1], logger.error(f'断言masterInstanceId失败,masterInstanceId为{masterInstanceId})')
        logger.info(f'断言status成功,status为{status},sessionId为{sessionId[0]},masterInstanceId为{masterInstanceId[0]}')

    @allure.title("注销群控会话")
    # @allure.severity("critical")
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestStreamPaas::test_stream_create_paas"])
    def test_stream_cancel_paas(self):
        uri = "/v1/multiple/stream/session/cancel"
        data = {
            "sessionId": global_data_paas.get("session_id")
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        logger.info(f'断言status成功,status为{status}')

    @allure.title("推流异常日志上报")
    # @allure.severity("normal")
    @pytest.mark.other
    def test_stream_report_paas(self):
        uri = "/v1/plugFlowLog/report"
        data = {
                "logId": "11113挨打奥德asdasd赛",
                "logTime": "03-12挨打",
                "sdkVersion": "sdk2025-03-121123123123挨as打",
                "sdkMediaVersion": "2025-03-1211112312啊sa啊",
                "sdkErrorCode": "dasdadas打asd adea ",
                "sdkErrorDesc": "嗷嗷嗷12a 啊大萨达21打  啊大as萨达  ",
                "sdkErrorLog": "测试上报接口11adsadasde挨打qwAsdasd ae12easda adsa奥斯登",
                "userDeviceVersion": "userDeviceVersion1",
                "userDevice": "userDevice1",
                "userExtranetIp": "127.0.0.1",
                "sdkErrorLogUrl": "localhost"
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        logger.info(f'断言status成功,status为{status}')