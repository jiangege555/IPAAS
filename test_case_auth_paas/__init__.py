from myutils.logformat import MyLogger

logger = MyLogger("paas").logger
"""
PAAS平台需要配置的参数：
url、Ak：环境信息，确保ak有实例，平台上传过可用的应用、文件
vendor、idc、card_type、instance_type：订购相关的供应商、实例信息
"""
# 测试环境
env_test = {
    "url": "http://36.25.240.241:33313/api/blade-paas",
    # "url": "http://36.25.240.241:38085/api/blade-paas",
    "header": {
        # "Ak": "3ef0ac13-8771-4ba7-9ed3-9d7a981ac5fc",
        # "Ak": "6b7612ae-3f1a-4d55-9fc8-3d4f3470f974",
        # "Ak": "0aa84f2a-e491-49e9-a4d6-cd71e9b8aeac",
        "Ak": "03a58aeb-ac49-4273-bf60-37cd56c5431d",
        "Content-Type": "application/json",
        "Version": "1",
        "Sign": "111111"
    },
    "vendor": "RCSX",
    "idc": "SZSY",
    "card_type": "RK3588_256_B",
    "instance_type": "C4",
    "amount": 1,
    # 初始化instance_ids的idc
    "idc_init": "SZSY"
    # "idc_init": "SZ"
}
# poc环境
env_poc = {
    "url": "http://101.69.168.129:33280/api/blade-paas",
    "header": {
        "Ak": "75e039fd-a8f8-45fc-9127-b379fc5ca164",
        "Content-Type": "application/json",
        "Version": "1",
        "Sign": "111111"
    },
    "vendor": "RCSX",
    "idc": "HZXS_3",
    "card_type": "RK3588_256_B",
    "instance_type": "C5",
    "amount": 1,
    # 初始化instance_ids的idc
    "idc_init": "HZXS_3"
}
# 生产环境
env_prod = {
    "url": "https://pass-sjzb.phone.armclouding.com:49443/api/blade-paas",
    "header": {
        "Ak": "ec75a80b-1e14-4bc9-84cd-6d9f82f0994b",
        "Content-Type": "application/json",
        "Version": "1",
        "Sign": "111111"
    },
    # 订购信息
    "vendor": "ByIaaS",
    "idc": "HZXS_3",
    "card_type": "RK3588_256_B",
    "instance_type": "C5",
    "amount": 5,
    # 初始化instance_ids的idc
    "idc_init": "HZXS_3"
}
# 全局参数变量
global_data_paas = {
    # 以下参数可以通用
    "instance_ids": [],
    "task_id": "",
    "app_id": "",
    "app_package": "",
    "app_remark": "测试url应用上传",
    "app_url": "https://cdn.chenair.com/a/apk/baolikuangbiao3d_downcc.apk",
    "app_md5": "8980c87a3e261fdb5181df7ef408a409",
    "file_id": "",
    "file_name": "测试url文件上传",
    "file_url": "https://cdn.chenair.com/down/apk2/com.tophotapp.topbike.apk",
    "file_md5": "9ce0eb207215dcc3395e73e5d2268352",
    "image_id": "",
    "brand": "",
    "model": "",
    "taskIds": []
}

