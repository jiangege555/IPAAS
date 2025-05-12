import jsonpath, allure, pytest
from test_case_auth_iaas import logger
from test_case_auth_iaas.baseTestCaseIaas import BaseTestCaseIaas, global_data_iaas


@pytest.mark.run(order=9)
@pytest.mark.all
@allure.feature("iaas宿主机相关接口")
class TestCardIaas(BaseTestCaseIaas):

    @allure.title("宿主机冷重启")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_card_restart_iaas(self):
        uri = "/openApi/HostRestart"
        data = {
            "sn": global_data_iaas.get("card_sns")
        }
        self.async_run_iaas(uri, data)

    @allure.title("宿主机重启")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_card_reboot_iaas(self):
        uri = "/openApi/CardReboot"
        data = {
            "sn": global_data_iaas.get("card_sns")
        }
        self.async_run_iaas(uri, data)

    @allure.title("空闲板卡查询")
    # @allure.severity("critical")
    @pytest.mark.smoke
    @pytest.mark.dependency()
    def test_card_checkCapacity_iaas(self):
        uri = "/openApi/CheckCapacityCard"
        data = {
            "card_type": global_data_iaas.get("device_type_card"),
            "idc": global_data_iaas.get("idc")
        }
        res_json = self.sync_get_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert total > 0, logger.error(f'断言total失败,total为{total}')
        logger.info(f'断言成功,status_code == {status_code},total == {total}')

    @allure.title("板卡订购")
    # @allure.severity("critical")
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestCardIaas::test_card_checkCapacity_iaas"])
    def test_card_subscribe_iaas(self):
        uri = "/openApi/SubscribeCard"
        data = {
            "card_type": global_data_iaas.get("device_type_card"),
            "idc": global_data_iaas.get("idc"),
            "amount": global_data_iaas.get("amount_card")
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert total == global_data_iaas.get("amount_card"), logger.error(f'断言total失败,total为{total}')
        sn = jsonpath.jsonpath(res_json, "$..sn")
        global_data_iaas["sub_cards"] = sn
        logger.info(f'断言成功,status_code == {status_code},total == {total},sn == {sn}')

    @allure.title("查询待初始化状态的板卡")
    # @allure.severity("critical")
    @pytest.mark.smoke
    @pytest.mark.dependency()
    def test_card_info_iaas(self):
        uri = "/openApi/ListCardInfo"
        data = {
            "initial_status": 0
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert total > 0, logger.error(f'断言total失败,total为{total}')
        sn = jsonpath.jsonpath(res_json, "$..sn")
        global_data_iaas["init_cards"] = sn
        logger.info(f'断言成功,status_code == {status_code},total == {total},init_sn == {sn}')

    @allure.title("初始化板卡")
    # @allure.severity("critical")
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestCardIaas::test_card_info_iaas"])
    def test_card_init_iaas(self):
        uri = "/openApi/InitialCard"
        data = {
            "sn": global_data_iaas.get("init_cards"),
            "image_id": global_data_iaas.get("image_id_init"),
            "amount": 5,
            "net_model": 0,
            "cpu_strategy": 0,
            "storage_strategy": 1,
            "mem_strategy": 1,
            "manufacturer": "123",
            "brand": global_data_iaas.get("brand"),
            "model": global_data_iaas.get("model"),
            "resolution_ratio": "1920*1080",
            "dpi": "320"
        }
        self.async_run_iaas(uri, data)

    @allure.title("还原板卡")
    # @allure.severity("critical")
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestCardIaas::test_card_init_iaas"])
    def test_card_revert_iaas(self):
        uri = "/openApi/RevertCard"
        data = {
            "sn": global_data_iaas.get("init_cards")
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        logger.info(f'断言成功,status_code == {status_code}')

    @allure.title("退订板卡")
    # @allure.severity("critical")
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestCardIaas::test_card_subscribe_iaas"])
    def test_card_unsubscribe_iaas(self):
        uri = "/openApi/UnsubscribeCard"
        data = {
            "sn": global_data_iaas.get("sub_cards")
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        logger.info(f'断言成功,status_code == {status_code}')

    @allure.title("板卡同步命令执行")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_card_cmd_sync_iaas(self):
        uri = "/openApi/CardSyncExecuteCommand"
        data = {
            "sn": global_data_iaas.get("card_sns"),
            "cmd": "date"
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        status = jsonpath.jsonpath(res_json, "$..status")[0]
        assert status == "success", logger.error(f'断言status失败,status为{status}')
        logger.info(f'断言成功,status_code == {status_code},status为{status}')

    @allure.title("板卡异步命令执行")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_card_cmd_async_iaas(self):
        uri = "/openApi/CardAsyncExecuteCommand"
        data = {
            "sn": global_data_iaas.get("card_sns"),
            "cmd": "date",
            "timeout": "60"
        }
        self.async_run_iaas(uri, data)

    @allure.title("板卡文件分发")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_card_fileDistribution_iaas(self):
        uri = "/openApi/CardFileDistribution"
        data = {
            "sn": global_data_iaas.get("card_sns"),
            "url": global_data_iaas.get("file_url"),
            "url_type": "other"
        }
        self.async_run_iaas(uri, data)
