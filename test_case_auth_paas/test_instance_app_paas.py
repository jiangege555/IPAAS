import jsonpath, allure, pytest
from test_case_auth_paas import logger
from test_case_auth_paas.baseTestCasePaas import BaseTestCasePaas, global_data_paas


@pytest.mark.run(order=4)
@pytest.mark.all
@allure.feature("paas实例应用相关接口")
class TestInstancePaas(BaseTestCasePaas):

    @allure.title("实例应用安装")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_appInstall_paas(self):
        self.app_list()
        uri = "/v1/instance/app/install"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "appId": global_data_paas.get("app_id"),
        }
        self.async_run_paas(uri, data)

    @allure.title("实例应用启动")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_appStart_paas(self):
        uri = "/v1/instance/app/control"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "packageName": global_data_paas.get("app_package"),
            "operatorType": "start"
        }
        self.async_run_paas(uri, data)

    @allure.title("实例应用停止")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_appStop_paas(self):
        uri = "/v1/instance/app/control"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "packageName": global_data_paas.get("app_package"),
            "operatorType": "stop"
        }
        self.async_run_paas(uri, data)

    @allure.title("实例应用停用")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_appDisable_paas(self):
        uri = "/v1/instance/app/control"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "packageName": global_data_paas.get("app_package"),
            "operatorType": "disable"
        }
        self.async_run_paas(uri, data)

    @allure.title("实例应用启用")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_appEnable_paas(self):
        uri = "/v1/instance/app/control"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "packageName": global_data_paas.get("app_package"),
            "operatorType": "enable"
        }
        self.async_run_paas(uri, data)

    @allure.title("实例应用清理")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_appClear_paas(self):
        uri = "/v1/instance/app/control"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "packageName": global_data_paas.get("app_package"),
            "operatorType": "clear"
        }
        self.async_run_paas(uri, data)

    @allure.title("实例应用前台保活开启（同步）")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_frontapp_opensync_paas(self):
        uri = "/v2/instance/app/front/open/sync"
        data = {
            "instanceId": global_data_paas.get("instance_ids")[0],
            "appPackage": global_data_paas.get("app_package")
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        logger.info(f'断言成功,status == {status}')

    @allure.title("实例应用前台保活关闭（同步）")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_frontapp_closesync_paas(self):
        uri = "/v2/instance/app/front/close/sync"
        data = {
            "instanceId": global_data_paas.get("instance_ids")[0],
            "appPackage": global_data_paas.get("app_package")
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        logger.info(f'断言成功,status == {status}')

    @allure.title("实例应用后台保活开启（同步）")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_backapp_opensync_paas(self):
        uri = "/v2/instance/app/back/open/sync"
        data = {
            "instanceId": global_data_paas.get("instance_ids")[0],
            "appPackageList": [global_data_paas.get("app_package")]
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        logger.info(f'断言成功,status == {status}')

    @allure.title("实例应用后台保活关闭（同步）")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_backapp_closesync_paas(self):
        uri = "/v2/instance/app/back/close/sync"
        data = {
            "instanceId": global_data_paas.get("instance_ids")[0],
            "appPackageList": [global_data_paas.get("app_package")]
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        logger.info(f'断言成功,status == {status}')

    @allure.title("实例应用前台保活开启（异步）")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_frontapp_openasync_paas(self):
        uri = "/v2/instance/app/front/open/async"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "appPackage": global_data_paas.get("app_package")
        }
        self.async_run_paas(uri, data)

    @allure.title("实例应用前台保活关闭（异步）")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_frontapp_closeasync_paas(self):
        uri = "/v2/instance/app/front/close/async"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "appPackage": global_data_paas.get("app_package")
        }
        self.async_run_paas(uri, data)

    @allure.title("实例应用后台保活开启（异步）")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_backapp_openasync_paas(self):
        uri = "/v2/instance/app/back/open/async"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "appPackageList": [global_data_paas.get("app_package")]
        }
        self.async_run_paas(uri, data)

    @allure.title("实例应用后台保活关闭（异步）")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_backapp_closeasync_paas(self):
        uri = "/v2/instance/app/back/close/async"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "appPackageList": [global_data_paas.get("app_package")]
        }
        self.async_run_paas(uri, data)

    @allure.title("查询实例应用清单")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_appList_paas(self):
        uri = "/v1/instance/app/list"
        data = {
            "instanceId": global_data_paas.get("instance_ids")[0]
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        packageName = jsonpath.jsonpath(res_json,
                                        f"$.data[?(@.packageName=='{global_data_paas.get('app_package')}')].packageName")
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert packageName != False, logger.error(f'断言packageName失败,packageName为{packageName}')
        logger.info(f'断言成功,status == {status},packageName == {packageName[0]}')

    @allure.title("查询实例应用清单（异步）")
    # @allure.severity("normal")
    @pytest.mark.smoke
    @pytest.mark.pressure
    def test_instance_appListAsync_paas(self):
        uri = "/v2/instance/app/list/async"
        data = {
            "instanceIds": global_data_paas.get("instance_ids")
        }
        self.async_run_paas(uri, data)

    @allure.title("实例全局root开启（同步）")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_rootGloabl_openSync_paas(self):
        uri = "/v2/instance/root/global/open/sync"
        data = {
            "instanceId": global_data_paas.get("instance_ids")[0]
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        logger.info(f'断言成功,status == {status}')

    @allure.title("实例全局root关闭（同步）")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_rootGloabl_closeSync_paas(self):
        uri = "/v2/instance/root/global/close/sync"
        data = {
            "instanceId": global_data_paas.get("instance_ids")[0]
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        logger.info(f'断言成功,status == {status}')

    @allure.title("实例全局root开启（异步）")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_rootGloabl_openAsync_paas(self):
        uri = "/v2/instance/root/global/open/async"
        data = {
            "instanceIds": global_data_paas.get("instance_ids")
        }
        self.async_run_paas(uri, data)

    @allure.title("实例全局root关闭（异步）")
    @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_rootGloabl_closeAsync_paas(self):
        uri = "/v2/instance/root/global/close/async"
        data = {
            "instanceIds": global_data_paas.get("instance_ids")
        }
        self.async_run_paas(uri, data)

    @allure.title("实例应用root开启（同步）")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_rootApp_openSync_paas(self):
        uri = "/v2/instance/root/app/open/sync"
        data = {
            "instanceId": global_data_paas.get("instance_ids")[0],
            "appPackageList": [global_data_paas.get("app_package")]
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        logger.info(f'断言成功,status == {status}')

    @allure.title("实例应用root关闭（同步）")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_rootApp_closeSync_paas(self):
        uri = "/v2/instance/root/app/close/sync"
        data = {
            "instanceId": global_data_paas.get("instance_ids")[0],
            "appPackageList": [global_data_paas.get("app_package")]
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        logger.info(f'断言成功,status == {status}')

    @allure.title("实例应用root开启（异步）")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_rootApp_openAsync_paas(self):
        uri = "/v2/instance/root/app/open/async"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "appPackageList": [global_data_paas.get("app_package")]
        }
        self.async_run_paas(uri, data)

    @allure.title("实例应用root关闭（异步）")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_rootApp_closeAsync_paas(self):
        uri = "/v2/instance/root/app/close/async"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "appPackageList": [global_data_paas.get("app_package")]
        }
        self.async_run_paas(uri, data)

    @allure.title("实例应用卸载")
    # @allure.severity("critical")
    @pytest.mark.important
    @pytest.mark.pressure
    def test_instance_appUninstall_paas(self):
        uri = "/v1/instance/app/control"
        data = {
            "instanceIds": global_data_paas.get("instance_ids"),
            "packageName": global_data_paas.get("app_package"),
            "operatorType": "uninstall"
        }
        self.async_run_paas(uri, data)