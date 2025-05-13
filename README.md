# IPAAS
IAAS、PAAS平台接口测试框架，接口带了鉴权请求

测试包、测试用例py文件、测试方法命名以test开头或者结尾

test_case_auth_paas：PAAS平台接口测试包（test_case_auth_iaas则为IAAS平台接口测试包，下面同理）

​	\_\_init\_\_.py：环境需要的一些依赖配置信息

​	baseTestCasePaas.py：测试基类，封装公共方法，在其他测试文件中继承该类

​	test_instance_paas.py：测试用例编写文件，支持单个封装测试方法，也支持yaml文件写用例

**1、主入口main_new.py**

def main(env, platform, repeat=None, mark="all"):

​	:param env: 环境参数 test | poc | prod（string）

​	:param platform: 平台参数 iaas | paas | all（string）

​	:param repeat: 是否重复执行，用于压测，默认不重复，传重复执行的次数（int）

​	:param mark: 指定要运行的用例标记，默认all标签（在测试用例类上面已经默认打上了all标签）（string）

mark传参格式：字符串，支持单标签、多标签逻辑组合

​	传"smoke"：执行具有 smoke 标记的用例

​	传"smoke and regression"：执行同时具有 smoke 和 regression 标记的用例

​	传"smoke or ui"：执行有 smoke 或 ui 标记的用例

​	传"regression and not slow"：执行有 regression 但没有 slow 标记的用例

​	传"(smoke or quick) and not slow"：执行 (smoke 或 quick) 且 (非 slow) 的用例

**2、pytest.ini文件**

主要用于标签管理，给用例打上标签，可以在执行时选择指定标签

**3、yaml用例文件**

格式规范看 “yaml用例解释.txt” 文件

在代码中这样引入，case_handle方法为处理yaml用例的方法，可以根据需求自己修改适配：

```python
@allure.story("压测")
@pytest.mark.parametrize("case_info", [
    pytest.param(
        case,  # 直接传递整个字典
        marks=[getattr(pytest.mark, mark) for mark in case.get('mark', [])],  # 动态获取 mark
        id=case["name"]
    )
    for case in read_testcase_yaml(f"{os.getcwd()}/test_case_auth_paas/204d.yaml", "test_204d",
                                   global_data_paas)
])
def test_pressure_paas(self, case_info):
    self.case_handle(case_info)
```

allure.story：描述用例场景

/test_case_auth_paas/204d.yaml：传入的yaml文件路径

test_204d：yaml文件第一行内容

test_pressure_paas：自定义测试方法名，注意不要重复

其他地方不用修改

**4、report目录**

html目录：生成的测试报告html包，查看需要借助allure命令

result目录：测试报告源数据，已自动处理转换为上面的html格式

openReport.bat：已写好的打开html包的批处理文件