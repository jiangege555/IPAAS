import jsonpath, allure, time, requests, pytest
from test_case_auth_paas import logger
from test_case_auth_paas.baseTestCasePaas import BaseTestCasePaas, global_data_paas
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


@pytest.mark.run(order=2)
@pytest.mark.all
@allure.feature("paas文件相关接口")
class TestFilePaas(BaseTestCasePaas):

    count = 0

    @allure.title("文件上传")
    # @allure.severity("normal")
    @pytest.mark.other
    def test_fileUpload_paas(self):
        self.check_file_exits_paas()
        uri = "/v1/file/add"
        data = {
            "fileName": global_data_paas.get("file_name"),
            "url": global_data_paas.get("file_url"),
            "md5": global_data_paas.get("file_md5"),
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        fileStatus = jsonpath.jsonpath(res_json, "$.data.fileStatus")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert fileStatus == 1, logger.error(f'断言fileStatus失败,fileStatus为{fileStatus}')
        global_data_paas["file_id"] = jsonpath.jsonpath(res_json, "$.data.fileId")[0]
        self.check_file_upload_status_paas()
        logger.info(f'断言status成功,status为{status},fileStatus为{fileStatus},fileId为{global_data_paas["file_id"]}')

    @allure.title("文件列表")
    # @allure.severity("normal")
    @pytest.mark.other
    def test_fileList_paas(self):
        uri = "/v1/file/list"
        data = {

        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        assert total > 0, logger.error(f'断言total失败,total为{total}')
        logger.info(f'断言status成功,status为{status},total为{total}')

    @allure.title("删除文件")
    # @allure.severity("normal")
    @pytest.mark.other
    def test_fileDelete_paas(self):
        uri = "/v1/file/delete"
        data = {
            "fileIds": [global_data_paas.get("file_id")]
        }
        res_json = self.sync_post_run_paas(uri, data)
        status = jsonpath.jsonpath(res_json, "status")[0]
        assert status == 0, logger.error(f'断言status失败,status为{status}')
        logger.info(f'断言status成功,status为{status}')

