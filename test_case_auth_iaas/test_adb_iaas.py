import jsonpath, allure, pytest
from test_case_auth_iaas import logger
from test_case_auth_iaas.baseTestCaseIaas import BaseTestCaseIaas, global_data_iaas


@pytest.mark.run(order=7)
@pytest.mark.all
@allure.feature("iaasADB密钥相关接口")
class TestAdbIaas(BaseTestCaseIaas):

    @allure.title("密钥创建")
    # @allure.severity("normal")
    @pytest.mark.other
    @pytest.mark.dependency()
    def test_adb_create_iaas(self):
        uri = "/openApi/AdbKeyCreate"
        data = {
            "name": global_data_iaas.get("adb_name"),
            "identity": global_data_iaas.get("adb_identity"),
            "remark": global_data_iaas.get("adb_remark")
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        adb_key_id = jsonpath.jsonpath(res_json, "$..adb_key_id")
        assert adb_key_id != False, logger.error(f'断言adb_key_id失败,adb_key_id为{adb_key_id[0]}')
        global_data_iaas["adb_key_id"] = adb_key_id[0]
        logger.info(f'ADB密钥创建成功,app_id为{adb_key_id[0]}')

    @allure.title("密钥列表查询")
    # @allure.severity("normal")
    @pytest.mark.other
    def test_adb_query_iaas(self):
        uri = "/openApi/AdbKeyQuery"
        data = {

        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert total > 0, logger.error(f'断言total失败,total为{total}')
        logger.info(f'断言成功,status_code == {status_code},total == {total}')

    @allure.title("密钥详情")
    # @allure.severity("normal")
    @pytest.mark.other
    @pytest.mark.dependency(depends=["TestAdbIaas::test_adb_create_iaas"])
    def test_adb_detail_iaas(self):
        uri = "/openApi/AdbKeyGet"
        data = {
            "adb_key_id": global_data_iaas.get("adb_key_id")
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        adb_key_id = jsonpath.jsonpath(res_json, "$..adb_key_id")[0]
        assert adb_key_id == global_data_iaas.get("adb_key_id"), logger.error(f'断言adb_key_id失败,adb_key_id为{adb_key_id}')
        logger.info(f'断言成功,status_code == {status_code},adb_key_id == {adb_key_id}')

    @allure.title("密钥绑定")
    # @allure.severity("normal")
    @pytest.mark.other
    @pytest.mark.dependency(depends=["TestAdbIaas::test_adb_create_iaas"])
    def test_adb_bind_iaas(self):
        uri = "/openApi/AdbKeyBind"
        data = {
            "instance_ids": global_data_iaas.get("instance_ids"),
            "adb_key_id": global_data_iaas.get("adb_key_id")
        }
        self.async_run_iaas(uri, data)

    @allure.title("密钥解绑")
    # @allure.severity("normal")
    @pytest.mark.other
    @pytest.mark.dependency(depends=["TestAdbIaas::test_adb_create_iaas"])
    def test_adb_unbind_iaas(self):
        uri = "/openApi/AdbKeyUnbind"
        data = {
            "instance_ids": global_data_iaas.get("instance_ids"),
            "adb_key_id": global_data_iaas.get("adb_key_id")
        }
        self.async_run_iaas(uri, data)

    @allure.title("密钥删除")
    # @allure.severity("normal")
    @pytest.mark.other
    @pytest.mark.dependency(depends=["TestAdbIaas::test_adb_create_iaas"])
    def test_adb_delete_iaas(self):
        uri = "/openApi/AdbKeyDelete"
        data = {
            "adb_key_id": global_data_iaas.get("adb_key_id")
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        logger.info(f'断言成功,status_code == {status_code}')