import jsonpath, allure, random, pytest, time
from test_case_auth_iaas import logger
from test_case_auth_iaas.baseTestCaseIaas import BaseTestCaseIaas, global_data_iaas


@pytest.mark.run(order=5)
@pytest.mark.all
@allure.feature("iaas应用相关接口")
class TestAppIaas(BaseTestCaseIaas):

    @allure.title("应用上传")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    @pytest.mark.dependency()
    def test_app_upload_iaas(self):
        uri = "/openApi/UploadApp"
        data = {
            "url": global_data_iaas.get("app_url")
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        app_id = jsonpath.jsonpath(res_json, "$..app_id")
        assert app_id != False, logger.error(f'断言app_id失败,app_id为{app_id[0]}')
        global_data_iaas["app_id"] = app_id[0]
        self.check_app_upload_status_iaas()
        logger.info(f'应用上传成功,app_id为{app_id[0]}')

    @allure.title("应用列表")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_app_list_iaas(self):
        uri = "/openApi/ListApp"
        data = {

        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert total > 0, logger.error(f'断言total失败,total为{total}')
        logger.info(f'断言成功,status_code == {status_code},total == {total}')

    @allure.title("应用安装")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestAppIaas::test_app_upload_iaas"])
    def test_app_install_iaas(self):
        uri = "/openApi/InstallAppToInstance"
        data = {
            "instance_ids": global_data_iaas.get("instance_ids"),
            "app_ids": [global_data_iaas.get("app_id")]
        }
        self.async_run_iaas(uri, data)

    @allure.title("查询已安装应用的实例列表")
    # @allure.severity("normal")
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestAppIaas::test_app_upload_iaas"])
    def test_app_list_byapp_iaas(self):
        uri = "/openApi/ListInstanceByAppId"
        data = {
            "app_id": global_data_iaas.get("app_id"),
            "offset": 0,
            "limit": 10
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert total > 0, logger.error(f'断言total失败,total为{total}')
        logger.info(f'断言成功,status_code == {status_code},total == {total}')

    @allure.title("查询实例已安装的应用列表")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_app_list_byinstance_iaas(self):
        uri = "/openApi/ListAppByInstanceId"
        data = {
            "instance_id": random.choice(global_data_iaas.get("instance_ids")),
            "offset": 0,
            "limit": 10
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert total > 0, logger.error(f'断言total失败,total为{total}')
        logger.info(f'断言成功,status_code == {status_code},total == {total}')

    @allure.title("应用卸载")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestAppIaas::test_app_upload_iaas"])
    def test_app_uninstall_iaas(self):
        uri = "/openApi/InstanceUninstallApp"
        data = {
            "instance_ids": global_data_iaas.get("instance_ids"),
            "app_ids": [global_data_iaas.get("app_id")]
        }
        self.async_run_iaas(uri, data)

    @allure.title("删除应用")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestAppIaas::test_app_upload_iaas"])
    def test_app_delete_iaas(self):
        uri = "/openApi/DeleteApp"
        data = {
            "app_id": global_data_iaas.get("app_id")
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        logger.info(f'断言成功,status_code == {status_code}')
