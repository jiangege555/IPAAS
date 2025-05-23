import jsonpath, allure, time, pytest
from test_case_auth_paas import logger
from test_case_auth_paas.baseTestCasePaas import BaseTestCasePaas, global_data_paas


@pytest.mark.run(order=6)
@pytest.mark.all
@allure.feature("paas镜像管理接口")
class TestImagePaas(BaseTestCasePaas):
    pass