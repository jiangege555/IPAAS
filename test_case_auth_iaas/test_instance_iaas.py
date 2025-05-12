import jsonpath, allure, random, requests, pytest
from test_case_auth_iaas import logger
from test_case_auth_iaas.baseTestCaseIaas import BaseTestCaseIaas, global_data_iaas
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


@pytest.mark.run(order=8)
@pytest.mark.all
@allure.feature("iaas实例相关接口")
class TestInstanceIaas(BaseTestCaseIaas):

    @allure.title("查询支持的实例套餐")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_package_iaas(self):
        uri = "/openApi/ListPackages"
        res_json = self.sync_get_run_iaas(uri)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert total > 0, logger.error(f'断言total失败,total为{total}')
        logger.info(f'断言成功,status_code == {status_code},total == {total}')

    @allure.title("查询实例空闲余量")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_capacity_iaas(self):
        uri = "/openApi/CheckCapacity"
        data = {
            "package": global_data_iaas.get("instance_package"),
            "idc": global_data_iaas.get("idc")
        }
        res_json = self.sync_get_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert total > 0, logger.error(f'断言total失败,total为{total}')
        package = jsonpath.jsonpath(res_json, "$..package")[0]
        assert package == global_data_iaas.get("instance_package"), logger.error(f'断言package失败,package为{package}')
        logger.info(f'断言成功,status_code == {status_code},total == {total},package == {package}')

    @allure.title("实例订购")
    # @allure.severity("normal")
    @pytest.mark.smoke
    @pytest.mark.dependency()
    def test_instance_subscribe_iaas(self):
        global subcids
        subcids = []
        uri = "/openApi/SubscribeInstance"
        data = {
            "idc": global_data_iaas.get("idc"),
            "bandwidth": random.choice(global_data_iaas.get("bandwidth")),
            "package": global_data_iaas.get("instance_package"),
            "amount": global_data_iaas.get("amount"),
            "expire_at": global_data_iaas.get("expire_at_sub")
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert total == global_data_iaas.get("amount"), logger.error(f'断言total失败,total为{total}')
        instanceId = jsonpath.jsonpath(res_json, "$..instance_id")
        subcids = instanceId
        logger.info(f'断言成功,status_code == {status_code},total == {total},instanceId == {instanceId}')

    @allure.title("实例续租")
    # @allure.severity("normal")
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestInstanceIaas::test_instance_subscribe_iaas"])
    def test_instance_renew_iaas(self):
        uri = "/openApi/RenewInstance"
        data = {
            "renew_data": {subcids[0]: global_data_iaas.get("expire_at_renew")}
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert total == 0, logger.error(f'断言total失败,total为{total}')
        logger.info(f'断言成功,status_code == {status_code},total == {total}')

    @allure.title("实例退订")
    # @allure.severity("normal")
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestInstanceIaas::test_instance_subscribe_iaas"])
    def test_instance_unsubscribe_iaas(self):
        uri = "/openApi/UnsubscribeInstance"
        data = {
            "instance_list": subcids
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert total == 0, logger.error(f'断言total失败,total为{total}')
        logger.info(f'断言成功,status_code == {status_code},total == {total}')

    @allure.title("实例列表查询")
    # @allure.severity("critical")
    @pytest.mark.smoke
    def test_instance_list_iaas(self):
        uri = "/openApi/ListInstanceInfo"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "offset": 0,
            "limit": 1000
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert total > 0, logger.error(f'断言total失败,total为{total}')
        logger.info(f'断言成功,status_code == {status_code},total == {total}')
        # instance_ids = jsonpath.jsonpath(res_json, "$..instance_id")
        # card_sns = list(set(jsonpath.jsonpath(res_json, "$..sn")))
        # global_data["instance_ids"] = instance_ids
        # global_data["card_sns"] = card_sns
        # logger.info(f'提取的instance_ids: {instance_ids}, 提取的card_sns: {card_sns}')

    @allure.title("查询指定实例基本信息")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_info_iaas(self):
        instance = random.choice(global_data_iaas.get("instance_ids"))
        uri = "/openApi/GetInstanceInfo"
        data = {
            "instance_id": instance
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        instance_id = jsonpath.jsonpath(res_json, "$..instance_id")[0]
        assert instance_id == instance, logger.error(f'断言instance_id失败,instance_id为{instance_id}')
        logger.info(f'断言成功,status_code == {status_code},instance_id == {instance_id}')

    @allure.title("查询实例状态信息")
    # @allure.severity("critical")
    @pytest.mark.smoke
    def test_instance_status_iaas(self):
        uri = "/openApi/ListInstanceStatus"
        data = {
            "instance_id": global_data_iaas.get("instance_ids")
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert total > 0, logger.error(f'断言total失败,total为{total}')
        logger.info(f'断言成功,status_code == {status_code},total == {total}')

    @allure.title("实例分组")
    # @allure.severity("critical")
    @pytest.mark.smoke
    def test_instance_group_iaas(self):
        uri = "/openApi/GroupInstance"
        data = {
            "group_name": global_data_iaas.get("group_name"),
            "instance_id": global_data_iaas.get("instance_ids")
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert total == 0, logger.error(f'断言total失败,total为{total}')
        logger.info(f'断言成功,status_code == {status_code},total == {total}')

    @allure.title("实例移除分组")
    # @allure.severity("critical")
    @pytest.mark.smoke
    def test_instance_ungroup_iaas(self):
        uri = "/openApi/UnGroupInstance"
        data = {
            "group_name": global_data_iaas.get("group_name"),
            "instance_list": global_data_iaas.get("instance_ids")
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        logger.info(f'断言成功,status_code == {status_code}')

    @allure.title("修改实例网络带宽")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_bandwidth_iaas(self):
        instance = random.choice(global_data_iaas.get("instance_ids"))
        uri = "/openApi/SetBandWidth"
        data = {
            "instance_id": instance,
            "download": random.choice(global_data_iaas.get("bandwidth")),
            "upload": random.choice(global_data_iaas.get("bandwidth"))
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        msg = jsonpath.jsonpath(res_json, "$..msg")[0]
        assert msg == "操作成功", logger.error(f'断言msg失败,msg为{msg}')
        logger.info(f'断言成功,status_code == {status_code},msg == {msg}')

    @allure.title("实例应用安装")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_appInstall_iaas(self):
        uri = "/openApi/InstallApp"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "url": global_data_iaas.get("app_url"),
            "package_name": global_data_iaas.get("app_package"),
            "md5sum": global_data_iaas.get("app_md5")
        }
        self.async_run_iaas(uri, data)

    @allure.title("实例应用启动")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_appStart_iaas(self):
        uri = "/openApi/AppManage"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "package_name": global_data_iaas.get("app_package"),
            "action": "start"
        }
        self.async_run_iaas(uri, data)

    @allure.title("实例截图")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_screenShot_iaas(self):
        uri = "/openApi/GetScreenshot"
        data = {
            "instance_id": global_data_iaas.get("instance_ids")
        }
        self.async_run_iaas(uri, data)

    @allure.title("实例应用停止")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_appStop_iaas(self):
        uri = "/openApi/AppManage"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "package_name": global_data_iaas.get("app_package"),
            "action": "stop"
        }
        self.async_run_iaas(uri, data)

    @allure.title("查看指定实例应用清单")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_appSingle_iaas(self):
        instance = random.choice(global_data_iaas.get("instance_ids"))
        uri = "/openApi/GetInstanceAppListInfo"
        data = {
            "instance_id": instance
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert total > 0, logger.error(f'断言total失败,total为{total}')
        logger.info(f'断言成功,status_code == {status_code},total == {total}')

    @allure.title("查看应用安装记录")
    # @allure.severity("critical")
    @pytest.mark.smoke
    def test_instance_appRecord_iaas(self):
        uri = "/openApi/InstallationRecord"
        data = {
            "instance_id": global_data_iaas.get("instance_ids")
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert total > 0, logger.error(f'断言total失败,total为{total}')
        logger.info(f'断言成功,status_code == {status_code},total == {total}')

    @allure.title("实例应用停用")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_appDisable_iaas(self):
        uri = "/openApi/AppManage"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "package_name": global_data_iaas.get("app_package"),
            "action": "disable"
        }
        self.async_run_iaas(uri, data)

    @allure.title("实例应用启用")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_appEnable_iaas(self):
        uri = "/openApi/AppManage"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "package_name": global_data_iaas.get("app_package"),
            "action": "enable"
        }
        self.async_run_iaas(uri, data)

    @allure.title("实例应用root启用")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_appRootEnable_iaas(self):
        uri = "/openApi/AppRootControl"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "package_name": [global_data_iaas.get("app_package")],
            "root": 1
        }
        self.async_run_iaas(uri, data)

    @allure.title("实例应用root关闭")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_appRootDisable_iaas(self):
        uri = "/openApi/AppRootControl"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "package_name": [global_data_iaas.get("app_package")],
            "root": 0
        }
        self.async_run_iaas(uri, data)

    @allure.title("实例root启用")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_rootEnable_iaas(self):
        uri = "/openApi/InstanceRootControl"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "root": 1
        }
        self.async_run_iaas(uri, data)

    @allure.title("实例root关闭")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_rootDisable_iaas(self):
        uri = "/openApi/InstanceRootControl"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "root": 0
        }
        self.async_run_iaas(uri, data)

    @allure.title("实例应用卸载")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_appUninstall_iaas(self):
        uri = "/openApi/AppManage"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "package_name": global_data_iaas.get("app_package"),
            "action": "uninstall"
        }
        self.async_run_iaas(uri, data)

    @allure.title("添加实例端口映射")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_portAdd_iaas(self):
        uri = "/openApi/AddPortMap"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "instance_port": global_data_iaas.get("instance_port"),
            "protocol": global_data_iaas.get("protocol"),
            "isp": global_data_iaas.get("isp")
        }
        self.async_run_iaas(uri, data)

    @allure.title("查询实例端口映射")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_portList_iaas(self):
        uri = "/openApi/ListPortMap"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "offset": 0,
            "limit": 100
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert total > 0, logger.error(f'断言total失败,total为{total}')
        logger.info(f'断言成功,status_code == {status_code},total == {total}')

    @allure.title("删除实例端口映射")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_portDel_iaas(self):
        uri = "/openApi/DelPortMap"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "instance_port": [global_data_iaas.get("instance_port")[0]],
            "protocol": global_data_iaas.get("protocol")
        }
        self.async_run_iaas(uri, data, "delete")

    @allure.title("清空实例端口映射")
    @allure.severity("normal")
    def test_instance_portClear_iaas(self):
        uri = "/openApi/ClearPortMap"
        data = {
            "instance_id": global_data_iaas.get("instance_ids")
        }
        self.async_run_iaas(uri, data, "delete")

    @allure.title("查询实例snat映射列表")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_snatList_iaas(self):
        uri = "/openApi/InstanceSnatMappingList"
        data = {
            "offset": 0,
            "limit": 100
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        logger.info(f'断言成功,status_code == {status_code}')

    @allure.title("异步实例系统属性设置")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_prop_async_set_iaas(self):
        uri = "/openApi/SetProperties"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "properties": {
                    "persist.product.v-model": global_data_iaas.get("model"),
                    "persist.product.v-brand": global_data_iaas.get("brand")
                }
        }
        self.async_run_iaas(uri, data)

    @allure.title("异步实例系统属性查询")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_prop_async_iaas(self):
        uri = "/openApi/GetProperties"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "keys": ["persist.product.v-model","persist.product.v-brand","persist.build.v-display_id","persist.sys.v-imei","persist.sys.v-imsi","persist.version.v-release"]
        }
        self.async_run_iaas(uri, data)

    @allure.title("同步实例系统属性查询")
    # @allure.severity("normal")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_prop_sync_iaas(self):
        instance = random.choice(global_data_iaas.get("instance_ids"))
        uri = "/openApi/SyncGetProperties"
        data = {
            "instance_id": instance,
            "keys": ["ro.instance.id"]
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        data = jsonpath.jsonpath(res_json, "$.data")[0]
        assert data != {}, logger.error(f'断言total失败,data为{data}')
        logger.info(f'断言成功,status_code == {status_code},data == {data}')

    @allure.title("关闭adb")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_adb_stop_iaas(self):
        uri = "/openApi/AdbdStop"
        data = {
            "instance_ids": global_data_iaas.get("instance_ids")
        }
        self.async_run_iaas(uri, data)

    @allure.title("开启adb")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_adb_start_iaas(self):
        uri = "/openApi/AdbdStart"
        data = {
            "instance_ids": global_data_iaas.get("instance_ids")
        }
        self.async_run_iaas(uri, data)

    @allure.title("异步命令执行")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_cmd_async_iaas(self):
        uri = "/openApi/AsyncExecuteCommand"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "cmd": "ls /data"
        }
        self.async_run_iaas(uri, data)

    @allure.title("同步命令执行")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_cmd_sync_iaas(self):
        uri = "/openApi/SyncExecuteCommand"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "cmd": "date"
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        status = jsonpath.jsonpath(res_json, "$..status")
        # 如果有失败的剔出去
        for i in status:
            if i != "success":
                status.remove(i)
        # 断言成功的个数等于实例数
        assert len(status) == len(global_data_iaas.get("instance_ids")), logger.error(f'断言status失败,status为{status},长度为{len(status)},instance_ids为{global_data_iaas.get("instance_ids")},instance_ids长度为{len(global_data_iaas.get("instance_ids"))}')
        logger.info(f'断言成功,status_code == {status_code},status == {status}')

    @allure.title("修改限速")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_set_speed_iaas(self):
        instance = random.choice(global_data_iaas.get("instance_ids"))
        uri = "/openApi/SpeedLimit"
        data = {
            "instance_id": instance,
            "public_up": random.choice(global_data_iaas.get("bandwidth")),
            "public_down": random.choice(global_data_iaas.get("bandwidth"))
        }
        self.async_run_iaas(uri, data)

    @allure.title("修改屏幕配置")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_set_stream_iaas(self):
        uri = "/openApi/SetStream"
        data = {
            "instance_ids": global_data_iaas.get("instance_ids"),
            "resolution_ratio": "720*1280",
            "fps": 30,
            "dpi": 320
        }
        self.async_run_iaas(uri, data)

    @allure.title("实例文件分发")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_file_distribution_iaas(self):
        uri = "/openApi/FileDistribution"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "url": "https://cdn.chenair.com/down/apk/luyinzhuanjiazhuanwenzi.apk"
        }
        self.async_run_iaas(uri, data)

    @allure.title("获取实例音视频连接token")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_connect_token_iaas(self):
        instance = random.choice(global_data_iaas.get("instance_ids"))
        uri = "/openApi/GetInstanceConnectToken"
        data = {
            "instance_id": instance
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        connect_token = jsonpath.jsonpath(res_json, "$..connectToken")
        assert connect_token != False, logger.error(f'断言connectToken失败,connectToken为{connect_token}')
        logger.info(f'断言成功,status_code == {status_code},connectToken == {connect_token}')

    @allure.title("获取实例推流参数")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_connect_h5_iaas(self):
        instance = random.choice(global_data_iaas.get("instance_ids"))
        uri = "/openApi/H5ConnectInfo"
        data = {
            "instance_id": instance
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        token = jsonpath.jsonpath(res_json, "$..token")
        assert token != False, logger.error(f'断言token失败,token为{token}')
        logger.info(f'断言成功,status_code == {status_code},token == {token}')

    @allure.title("查询实例webshell链接")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_webshell_url_iaas(self):
        instance = random.choice(global_data_iaas.get("instance_ids"))
        uri = "/openApi/InstanceWebShellUrl"
        data = {
            "instance_id": instance
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        url = jsonpath.jsonpath(res_json, "$..url")
        assert url != False, logger.error(f'断言url失败,url为{url}')
        logger.info(f'断言成功,status_code == {status_code},url == {url}')

    @allure.title("新增实例镜像")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_imageAdd_iaas(self):
        uri = "/openApi/AddImage"
        data = {
            "url": global_data_iaas.get("image_url"),
            "md5sum": global_data_iaas.get("image_md5sum"),
            "build_version": global_data_iaas.get("image_build_version"),
            "device_type": global_data_iaas.get("image_device_type"),
            "system": global_data_iaas.get("image_system")
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        image_id = jsonpath.jsonpath(res_json, "$.data.image_id")[0]
        assert image_id != "", logger.error(f'断言image_id失败,image_id为{image_id}')
        global_data_iaas["image_id"] = image_id
        logger.info(f'断言成功,status_code == {status_code},image_id == {image_id}')
        self.check_image_upload_status_iaas()

    @allure.title("查询实例镜像")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_imageList_iaas(self):
        uri = "/openApi/ListImage"
        data = {
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert total > 0, logger.error(f'断言total失败,total为{total}')
        logger.info(f'断言成功,status_code == {status_code},total == {total}')

    @allure.title("实例镜像分发到板卡")
    # @allure.severity("normal")
    @pytest.mark.smoke
    @pytest.mark.dependency()
    def test_instance_imageDistribute_iaas(self):
        uri = "/openApi/InstanceImageDistribution"
        data = {
            "image_id": global_data_iaas.get("image_id_init"),
            "sn": global_data_iaas.get("card_sns")
        }
        self.async_run_iaas(uri, data)

    @allure.title("升级实例镜像")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_imageUpgrade_iaas(self):
        uri = "/openApi/Upgrade"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "image_id": global_data_iaas.get("image_id"),
            "saveprop": True
        }
        self.async_run_iaas(uri, data, time_sleep=10)

    @allure.title("板卡中实例镜像删除")
    # @allure.severity("normal")
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestInstanceIaas::test_instance_imageDistribute_iaas"])
    def test_instance_imageRemove_iaas(self):
        uri = "/openApi/InstanceImageDelete"
        data = {
            "image_id": global_data_iaas.get("image_id_init"),
            "sn": global_data_iaas.get("card_sns")
        }
        self.async_run_iaas(uri, data)

    @allure.title("触发式升级实例镜像")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_triggerUpgrade_iaas(self):
        uri = "/openApi/Upgrade"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "image_id": global_data_iaas.get("image_id"),
            "trigger_type": 1,
            "clean_data": True,
            "saveprop": True
        }
        allure.attach(f"""{str(data).replace("'", '"')}""", "传参")
        sign = self.postSign(data)
        global_data_iaas["header"]["Sign"] = sign
        res = requests.post(url=self.url + uri, json=data, headers=global_data_iaas.get("header"), verify=False)
        logger.info(f'请求url--{res.url}')
        logger.info(f"""请求headers--{str(global_data_iaas.get("header")).replace("'", '"')}""")
        allure.attach(f"{res.text}", "返回值")
        res.raise_for_status()  # 抛出HTTP错误
        res_json = res.json()
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        # 同步返回的断言
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        # request_id = list(res_json.get("data").get("task_map").values())
        task_map = jsonpath.jsonpath(res_json, "$..task_map")
        assert task_map != [], logger.error(f'断言task_map失败,task_map为{task_map}')
        request_id = list(task_map[0].values())
        # logger.info(f'提取的request_id为 {request_id}')
        logger.info(f'断言成功,status_code == {status_code},request_id == {request_id}')
        uri_reboot = "/openApi/SystemCtl"
        data_reboot = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "action": "restart",
            "saveprop": True
        }
        sign = self.postSign(data_reboot)
        global_data_iaas["header"]["Sign"] = sign
        requests.post(url=self.url + uri_reboot, json=data_reboot, headers=global_data_iaas.get("header"), verify=False)
        logger.info(f'已重启实例触发升级')
        # 异步任务的断言
        self.checkProgressIaas(request_id, 10)
        # self.async_run_iaas(uri, data, time_sleep=10)

    @allure.title("删除实例镜像")
    # @allure.severity("critical")
    @pytest.mark.smoke
    def test_instance_imageDelete_iaas(self):
        uri = "/openApi/DeleteImage"
        data = {
            "image_id": global_data_iaas.get("image_id")
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        logger.info(f'断言成功,status_code == {status_code}')

    @allure.title("查询应用模板")
    # @allure.severity("critical")
    @pytest.mark.smoke
    def test_instance_templateList_iaas(self):
        uri = "/openApi/ListAppTemplate"
        data = {
            "template_id": global_data_iaas.get("template_id")
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        total = jsonpath.jsonpath(res_json, "$..total")[0]
        assert total == 1, logger.error(f'断言total失败,total为{total}')
        logger.info(f'断言成功,status_code == {status_code},total == {total}')

    @allure.title("挂载应用模板")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_templateMount_iaas(self):
        uri = "/openApi/MountAppTemplate"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "template_id": global_data_iaas.get("template_id")
        }
        self.async_run_iaas(uri, data, time_sleep=10)

    @allure.title("解挂应用模板")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_templateUnmount_iaas(self):
        uri = "/openApi/UnmountAppTemplate"
        data = {
            "instance_id": global_data_iaas.get("instance_ids")
        }
        self.async_run_iaas(uri, data, time_sleep=10)

    @allure.title("实例更换")
    # @allure.severity("normal")
    @pytest.mark.smoke
    def test_instance_change_iaas(self):
        instances = global_data_iaas.get("instance_ids").copy()
        instance_1 = random.choice(instances)
        instances.remove(instance_1)
        instance_2 = random.choice(instances)
        uri = "/openApi/ChangeInstance"
        data = {
            "from_instance_id": instance_1,
            "to_instance_id": instance_2
        }
        self.async_run_iaas(uri, data)

    @allure.title("实例备份")
    # @allure.severity("normal")
    @pytest.mark.smoke
    @pytest.mark.dependency()
    def test_instance_dataBackup_iaas(self):
        global instance_backup
        instance_backup = random.choice(global_data_iaas.get("instance_ids"))
        uri = "/openApi/BackUpInstance"
        data = {
            "instance_id": instance_backup,
            "path": "/data/"
        }
        allure.attach(f"{data}", "传参")
        sign = self.postSign(data)
        global_data_iaas["header"]["Sign"] = sign
        res = requests.post(url=self.url + uri, json=data, headers=global_data_iaas.get("header"), verify=False)
        logger.info(f'请求url--{res.url}')
        logger.info(f'请求headers--{res.headers}')
        # logger.info(f'test_instance_list res为{res.text}')
        allure.attach(f"{res.text}", "返回值")
        res.raise_for_status()  # 抛出HTTP错误
        res_json = res.json()
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        backup_id = jsonpath.jsonpath(res_json, "$..backup_id")
        assert backup_id != False, logger.error(f'断言backup_id失败,backup_id为{backup_id[0]}')
        logger.info(f'断言成功,status_code == {status_code},backup_id == {backup_id[0]}')
        global_data_iaas["backup_id"] = backup_id[0]
        self.check_backup_status_iaas()

    @allure.title("实例还原")
    # @allure.severity("normal")
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestInstanceIaas::test_instance_dataBackup_iaas"])
    def test_instance_dataRestore_iaas(self):
        instances = global_data_iaas.get("instance_ids").copy()
        instances.remove(instance_backup)
        uri = "/openApi/RestoreInstance"
        data = {
            "instance_id": random.choice(instances),
            "backup_id": global_data_iaas.get("backup_id")
        }
        self.async_run_iaas(uri, data)

    @allure.title("删除实例备份文件")
    # @allure.severity("normal")
    @pytest.mark.smoke
    @pytest.mark.dependency(depends=["TestInstanceIaas::test_instance_dataBackup_iaas"])
    def test_instance_deleteBackUp_iaas(self):
        uri = "/openApi/DeleteBackUp"
        data = {
            "backup_ids": [global_data_iaas.get("backup_id")]
        }
        res_json = self.sync_post_run_iaas(uri, data)
        status_code = jsonpath.jsonpath(res_json, "status_code")[0]
        assert status_code == 0, logger.error(f'断言status_code失败,status_code为{status_code}')
        logger.info(f'断言成功,status_code == {status_code}')

    @allure.title("实例关机")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_shutdown_iaas(self):
        uri = "/openApi/SystemCtl"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "action": "stop"
        }
        self.async_run_iaas(uri, data)

    @allure.title("实例开机")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_startup_iaas(self):
        uri = "/openApi/SystemCtl"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "action": "start"
        }
        self.async_run_iaas(uri, data)

    @allure.title("实例重启")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_reboot_iaas(self):
        uri = "/openApi/SystemCtl"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "action": "restart",
            "saveprop": True
        }
        self.async_run_iaas(uri, data)

    @allure.title("实例恢复出厂")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_reset_iaas(self):
        uri = "/openApi/Recovery"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "saveprop": True
        }
        self.async_run_iaas(uri, data, time_sleep=10)

    @allure.title("实例恢复出厂V2")
    # @allure.severity("critical")
    @pytest.mark.pressure
    @pytest.mark.smoke
    def test_instance_resetV2_iaas(self):
        uri = "/openApi/RecoveryV2"
        data = {
            "instance_id": global_data_iaas.get("instance_ids"),
            "dir_path": "/data/local",
            "saveprop": True
        }
        self.async_run_iaas(uri, data, time_sleep=10)

