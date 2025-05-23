from myutils.logformat import MyLogger
import datetime, random

logger = MyLogger("iaas").logger
"""
IAAS需要配置的参数：
url、Ak：环境信息，确保ak有实例
每个环境单独配置，运行时传入环境标志
"""
# 测试环境
env_test = {
    "url": "http://36.25.240.241:38080/api/blade-pass",
    "header": {
        "Ak": "6fe85202-5992-4b10-9b10-eeba5e0124ec",
        "Content-Type": "application/json",
        "Version": "1",
        "Sign": "111111"
    },
    # 实例订购信息
    "idc": "SZSY",
    "instance_package": "board_rk3588_128g_8c16g_1/6",
    "bandwidth": [20, 40, 60, 80, 100, 150, 200],
    "amount": 2,
    # 实例镜像上传、升级等接口使用
    "image_url": "http://test-iaas-szsy-fs.androidscloud.com:62225/download/merge/c492fe476fde3fde951f96b43b5a7847/c8e00785-ea46-4598-9ae3-9ea451390f82.tgz",
    "image_md5sum": "c492fe476fde3fde951f96b43b5a7847",
    "image_build_version": "vc20250314:170nr",
    "image_device_type": "RK3588",
    "image_system": "Android10",
    # 应用模板id
    "template_id": "1344972133019275264",
    # 板卡订购和板卡镜像上传接口使用
    "amount_card": 1,
    "device_type_card": "RK3588_256_B",
    "image_url_card": "http://vclusters.imwork.net:43284/download/merge/d24704805cf10f582261a111b452d341/a2f9f47c-86ce-448e-baad-1381479c316c.img",
    "image_md5_card": "d24704805cf10f582261a111b452d341",
    "image_build_version_card": "emmc_paas_v1.7.1_20241214",
    # 初始化板卡、镜像分发板卡、删除板卡镜像使用的镜像id
    "image_id_init": 60519,
}
# poc环境
env_poc = {
    "url": "http://36.25.252.233:51038/api/blade-pass",
    "header": {
        "Ak": "df401528-2ae1-4afc-acbc-6b5bbd249259",
        "Content-Type": "application/json",
        "Version": "1",
        "Sign": "111111"
    },
    # 实例订购信息
    "idc": "HZXS_3",
    "instance_package": "board_rk3588_256g_8c20g_1/4",
    "bandwidth": [20, 40, 60, 80, 100, 150, 200],
    "amount": 2,
    # 实例镜像上传、升级等接口使用
    "image_url": "http://test-iaas-szsy-fs.androidscloud.com:62225/download/merge/c492fe476fde3fde951f96b43b5a7847/c8e00785-ea46-4598-9ae3-9ea451390f82.tgz",
    "image_md5sum": "c492fe476fde3fde951f96b43b5a7847",
    "image_build_version": "vc20250314:170nr",
    "image_device_type": "RK3588",
    "image_system": "Android10",
    # 应用模板id
    "template_id": "1351868293437435904",
    # 板卡订购和板卡镜像上传接口使用
    "amount_card": 1,
    "device_type_card": "RK3588_256_B",
    "image_url_card": "http://vclusters.imwork.net:43284/download/merge/d24704805cf10f582261a111b452d341/a2f9f47c-86ce-448e-baad-1381479c316c.img",
    "image_md5_card": "d24704805cf10f582261a111b452d341",
    "image_build_version_card": "emmc_paas_v1.7.1_20241214",
    # 初始化板卡、镜像分发板卡、删除板卡镜像使用的镜像id
    "image_id_init": 165,
}
# 生产环境
env_prod = {
    "url": "https://openaccess.armclouding.com:58172/api/blade-pass",
    "header": {
        "Ak": "05fcc5c8-1d6b-4be2-afce-de3124eed19d",
        "Content-Type": "application/json",
        "Version": "1",
        "Sign": "111111"
    },
    # 实例订购信息
    "idc": "FSNH",
    "instance_package": "board_rk3588_256g_8c16g_1/5",
    "bandwidth": [20, 40, 60, 80, 100, 150, 200],
    "amount": 5,
    # 实例镜像上传、升级等接口使用
    "image_url": "http://183.62.127.41:33380/download/merge/3198f93ff247782ae9d6440c6487c46d/98fc9c3e-f6a1-4bc4-a7b8-3190514a75a6.tgz",
    "image_md5sum": "3198f93ff247782ae9d6440c6487c46d",
    "image_build_version": "165-5:20250320",
    "image_device_type": "RK3588",
    "image_system": "Android10",
    # 应用模板id
    "template_id": "1352614170808012800",
    # 板卡订购和板卡镜像上传接口使用
    "amount_card": 7,
    "device_type_card": "RK3588_256_B",
    "image_url_card": "http://vclusters.imwork.net:43284/download/merge/d24704805cf10f582261a111b452d341/a2f9f47c-86ce-448e-baad-1381479c316c.img",
    "image_md5_card": "d24704805cf10f582261a111b452d341",
    "image_build_version_card": "emmc_paas_v1.7.1_20241214",
    # 初始化板卡、镜像分发板卡、删除板卡镜像使用的镜像id
    "image_id_init": 848,
}
# 获取当前时间
now = datetime.datetime.now()
# 获取时间戳，用于订购和续租接口
future_30 = int((now + datetime.timedelta(days=30)).timestamp())
future_60 = int((now + datetime.timedelta(days=60)).timestamp())
# 机型库
machines = [{"brand":"HONOR","models":["ELZ-AN10","OXF-AN10","YAL-AL50"]},{"brand":"samsung","models":["SM-A5160"]},{"brand":"Xiaomi","models":["M2002J9E","Mi10"]},{"brand":"OPPO","models":["PHZ110"]},{"brand":"OnePlus","models":["PHK110","PJA110","PHB110"]},{"brand":"google","models":["Pixel 8a","Pixel 4","Pixel"]},{"brand":"vivo","models":["V2232A","V2001A"]},{"brand":"POCO","models":["POCO F2 Pro"]},{"brand":"HUAWEI","models":["CLS-AL00","TNN-AN00","NOH-AN00"]},{"brand":"Redmi","models":["M2104K10AC","22127RK46C","Redmi Note 8 Pro","Redmi K30","Redmi K30 Pro"]}]
machine = random.choice(machines)
# 全局参数变量
global_data_iaas = {
    # 以下参数可以通用
    "instance_ids": [],
    "card_sns": [],
    "expire_at_sub": future_30,
    "resolution": "720*1280",
    "expire_at_renew": future_60,
    "group_name": "fjtest",
    "instance_port": [5555, 9100],
    "protocol": "tcp",
    "isp": 1,
    "brand": machine.get("brand"),
    "model": random.choice(machine.get("models")),
    "app_id": "",
    "app_package": "com.xiaotaiyang",
    "app_remark": "小太阳",
    "app_url": "http://183.57.144.35:58120/document/newFile/download/1/c1bk700631184d81ad51/breakUpload_52907728516101563200/xiaotaiyang.apk",
    "app_md5": "05a58d67c6a8349d0614a09e6855af66",
    "file_id": "",
    "file_name": "补丁包",
    "file_url": "http://183.57.144.35:58120/document/newFile/download/1/c1bk700631184d81ad51/breakUpload_52839675543631377066/patch_for_kill_process_of_share_memory_leak_20250106.zip",
    "file_md5": "cf0c5526903fc7a8d91930a0c86dcd20",
    "image_id": "",
    "adb_name": "测试密钥创建",
    "adb_identity": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCyf5jGjx6C0KfzTs25I5uBGcK4Al7sDK4pOyXByeXUnxfDnyhFopCWfneDICzIFWgLILaLm7188xF6LuVwbO2lPGxgrmcogAXYObTEbrFEPrIGGh2CdQvQCinCjp7thTqpZShSevNL9djmjA0UVP1sVLxyWMZKmTEAIHMyPaLfw5YZMNP6ghs/mlCWptDjVHiyw2+PdymJH7i/0XBBzrXLC4bUAdIGhaNvvDj12tFwjkBtGr/Tzed0kQQiUSJy2mv235Sh0FAVFLx7im4At7T5bBTWG+0/qBzQHJpMdUatrSv6ChHhuHYegG8ahfDtgPA8wW9NEpBvyel2Fv2+GGOjzK2RjC+0hapFyp9VKgda3LwnCFqwx5Wrclh7w571bs0AsPFfePk5wXh8gojgyaSI6Z/+Z8FjId410ZswqvfPucqzIYAdqL7S34uTvHZiRlNp2tOJrsf0FMnVkIJx9V9JCo8lfn39POLnmkb9YmzUlnqoeYVTjfx1ib3LSAtYzrjUSSJ7ftmZQnO2mf09SPCc5PiypUOf6/3zNbliXtdlPJc8hu82CU0D6JdIT+/f1XjeXmNeOCaYQWMSEcWzhKdj+4x6OOaOXST0qsvPqjImumJtPMKsZgT0KvGVkR1KIG08BpHWMO11ioM5M44qLGTu6CFO9issYAgJvDcU0Vd/IQ== admin@DESKTOP-56MQVAB",
    "adb_remark": "fj测试密钥创建",
    "requestIds": []
}