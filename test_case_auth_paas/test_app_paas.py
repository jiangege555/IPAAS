import jsonpath, allure, pytest
import requests
import time

from test_case_auth_paas import logger
from test_case_auth_paas.baseTestCasePaas import BaseTestCasePaas, global_data_paas
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


@pytest.mark.run(order=1)
@pytest.mark.all
@allure.feature("paas应用相关接口")
class TestAppPaas(BaseTestCasePaas):

    count = 0
    @allure.title("应用上传")
    # @allure.severity("normal")
    @pytest.mark.other
    def test_appUpload_paas(self):
        self.check_app_exits_paas()
        uri = "/v1/app/add"
        data = {
                "remark": global_data_paas.get("app_remark"),
                "url": global_data_paas.get("app_url"),
                "md5": global_data_paas.get("app_md5"),
            }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        appStatus = jsonpath.jsonpath(res_json, "$.data.appStatus")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert appStatus == 1, logger.error(f'断言appStatus失败,appStatus为{appStatus}')
        global_data_paas["app_id"] = jsonpath.jsonpath(res_json, "$.data.appId")[0]
        self.check_app_upload_status_paas()
        logger.info(f'断言status成功,status为{status},appStatus为{appStatus},appId为{global_data_paas["app_id"]}')

    @allure.title("应用列表")
    # @allure.severity("normal")
    @pytest.mark.other
    def test_appList_paas(self):
        uri = "/v1/app/list"
        data = {

        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert total > 0, logger.error(f'断言total失败,total为{total}')
        logger.info(f'断言status成功,status为{status},total为{total}')

    @allure.title("删除应用")
    # @allure.severity("normal")
    @pytest.mark.other
    def test_appDelete_paas(self):
        uri = "/v1/app/delete"
        data = {
            "appIds": [global_data_paas.get("app_id")]
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        logger.info(f'断言status成功,status为{status}')
