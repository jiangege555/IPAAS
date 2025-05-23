import jsonpath, allure, random, pytest, os
from test_case_auth_paas import logger
from test_case_auth_paas.baseTestCasePaas import BaseTestCasePaas, global_data_paas
from myutils.read_yaml import read_testcase_yaml


@pytest.mark.run(order=7)
@pytest.mark.pressure
@allure.feature("paas实例相关接口")
class TestPressure(BaseTestCasePaas):

    @allure.story("压测")
    # @allure.severity("critical")
    @pytest.mark.parametrize("case_info", [
        pytest.param(
            case,  # 直接传递整个字典
            # marks=getattr(pytest.mark, case["mark"]),  # 动态获取 mark
            marks=[getattr(pytest.mark, mark) for mark in case.get('mark', [])],  # 动态获取 mark
            id=case["name"]
        )
        for case in read_testcase_yaml(f"{os.getcwd()}/test_case_auth_paas/204d.yaml", "test_204d",
                                       global_data_paas)
    ])
    def test_pressure_paas(self, case_info):
        self.case_handle(case_info)