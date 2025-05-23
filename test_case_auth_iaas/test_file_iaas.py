import jsonpath, allure, pytest, time
from test_case_auth_iaas import logger
from test_case_auth_iaas.baseTestCaseIaas import BaseTestCaseIaas, global_data_iaas


@pytest.mark.run(order=6)
@pytest.mark.all
@allure.feature("iaas文件相关接口")
class TestFileIaas(BaseTestCaseIaas):

    @allure.title("文件上传")
    @allure.severity("normal")
    @pytest.mark.dependency()
    def test_file_upload_iaas(self):
        uri = "/openApi/UploadFile"
        data = {
            "url": global_data_iaas.get("file_url"),
            "md5sum": global_data_iaas.get("file_md5")
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        file_id = jsonpath.jsonpath(res_json, "$..file_id")
        assert file_id != False, logger.error(f'断言file_id失败,file_id为{file_id[0]}')
        global_data_iaas["file_id"] = file_id[0]
        self.check_file_upload_status_iaas()
        logger.info(f'文件上传成功,file_id为{file_id[0]}')

    @allure.title("文件删除")
    @allure.severity("normal")
    @pytest.mark.dependency(depends=["TestFileIaas::test_file_upload_iaas"])
    def test_file_delete_iaas(self):
        uri = "/openApi/FileDelete"
        data = {
            "file_id": global_data_iaas.get("file_id")
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        logger.info(f'断言成功,status_code == {status_code}')

