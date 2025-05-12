import os, time, sys, pytest, json, webbrowser, threading
from test_case_auth_paas import global_data_paas, env_test as env_test_paas, env_poc as env_poc_paas, env_prod as env_prod_paas
from test_case_auth_iaas import global_data_iaas, env_test as env_test_iaas, env_poc as env_poc_iaas, env_prod as env_prod_iaas
from test_case_auth_paas import logger as paas_logger
from test_case_auth_iaas import logger as iaas_logger
import requests, jsonpath, re
from functools import reduce

host = 'localhost'
port = '63342'
allure_url = f'http://{host}:{port}/API_Test_Auto/report/html'
BASEDIR = os.getcwd()
# print(BASEDIR)
# 报告的路径
ALLURE_DIR = os.path.join(BASEDIR, 'report')
# allure生成json文件的路径
ALLURE_RESULT = os.path.join(ALLURE_DIR, 'result')
if not os.path.exists(ALLURE_RESULT):
    os.mkdir(ALLURE_RESULT)
ALLURE_PATH = os.path.join(ALLURE_RESULT, str(int(time.time())))
# 最终生成html的路径
ALLURE_HTML_DIR = os.path.join(ALLURE_DIR, 'html')
if not os.path.exists(ALLURE_HTML_DIR):
    os.mkdir(ALLURE_HTML_DIR)


# 记录历史运行结果，展示测试结果趋势图，可以在TREND里进行新老数据切换
def get_dirname():
    hostory_file = os.path.join(ALLURE_HTML_DIR, "history.json")
    if os.path.exists(hostory_file):
        with open(hostory_file) as f:
            li = eval(f.read())
        # 根据构建次数进行排序，从大到小
        li.sort(key=lambda x: x['buildOrder'], reverse=True)
        # 返回下一次的构建次数，所以要在排序后的历史数据中的buildOrder+1
        return li[0]["buildOrder"] + 1, li
    else:
        # 首次进行生成报告，肯定会进到这一步，先创建history.json,然后返回构建次数1（代表首次）
        with open(hostory_file, "w"):
            pass
        return 1, None


def update_trend_data(dirname, old_data: list, env):
    """
    dirname：构建次数
    old_data：备份的数据
    update_trend_data(get_dirname())
    """
    dic = {}
    WIDGETS_DIR = os.path.join(ALLURE_HTML_DIR, f"{str(dirname)}/widgets")
    """更换报告标题"""
    # 定义为只读模型，并定义名称为f
    with open(f'{WIDGETS_DIR}/summary.json', 'rb') as f:
        # 加载json文件中的内容给params
        params = json.load(f)
        # 修改内容
        params['reportName'] = f'{env}环境接口自动化测试报告'
        # 将修改后的内容保存在dict中
        dic.update(params)
    # 定义为写模式，名称定义为r
    with open(f'{WIDGETS_DIR}/summary.json', 'w', encoding="utf-8") as r:
        # 将dict写入名称为r的文件中
        json.dump(dic, r, ensure_ascii=False, indent=4)
    """更换历史数据"""
    # 读取最新生成的history-trend.json数据
    with open(os.path.join(WIDGETS_DIR, "history-trend.json")) as f:
        data = f.read()
    new_data = eval(data)
    if old_data is not None:
        new_data[0]["buildOrder"] = old_data[0]["buildOrder"] + 1
    else:
        old_data = []
        new_data[0]["buildOrder"] = 1
    # 给最新生成的数据添加reportUrl key，reportUrl要根据自己的实际情况更改
    new_data[0]["reportUrl"] = f"{allure_url}/{dirname}/index.html"
    # 把最新的数据，插入到备份数据列表首位
    old_data.insert(0, new_data[0])
    # 把所有生成的报告中的history-trend.json都更新成新备份的数据old_data，这样的话，点击历史趋势图就可以实现新老报告切换
    for i in range(1, dirname + 1):
        try:
            with open(os.path.join(ALLURE_HTML_DIR, f"{str(i)}/widgets/history-trend.json"), "w+") as f:
                f.write(json.dumps(old_data))
        except:
            for j in old_data:
                if j.get("buildOrder") == i:
                    old_data.remove(j)
            continue
    # 把数据备份到history.json
    history_file = os.path.join(ALLURE_HTML_DIR, "history.json")
    with open(history_file, "w+") as f:
        f.write(json.dumps(old_data))
    return old_data, new_data[0]["reportUrl"]


def iaas_init():
    # 初始化iaas参数
    url_iaas = global_data_iaas.get("url")
    header_iaas = global_data_iaas.get("header")
    data_iaas = {}
    # IAAS鉴权请求
    res_iaas_sign = requests.post(url=url_iaas + "/openApi/post/sign", headers=header_iaas, json=data_iaas)
    res_text = res_iaas_sign.text
    if res_iaas_sign.status_code != 200:
        Sign = re.findall(r'serverSign\\":\\"(\w+)\\",', res_text)[0]
        header_iaas["Sign"] = Sign
    res_iaas = requests.post(url=url_iaas + "/openApi/ListInstanceInfo", headers=header_iaas, json=data_iaas)
    res_iaas_json = res_iaas.json()
    iaas_logger.info(f'iaas查询结果为{res_iaas_json}')
    # with lock:
    iaas_instance = list(set(jsonpath.jsonpath(res_iaas_json, "$..instance_id")))
    iaas_sns = list(set(jsonpath.jsonpath(res_iaas.json(), "$..sn")))
    global_data_iaas["instance_ids"] = iaas_instance
    global_data_iaas["card_sns"] = iaas_sns
    iaas_logger.info(f'提取的iaas instance_ids: {iaas_instance}, 提取的iaas card_sns: {iaas_sns}')


def iaas_init_repeat():
    """
    压测重复执行时使用
    :return:
    """
    # 初始化iaas参数
    url_iaas = global_data_iaas.get("url")
    header_iaas = global_data_iaas.get("header")
    data_iaas = {
        "limit": 1000
    }
    # IAAS鉴权请求
    res_iaas_sign = requests.post(url=url_iaas + "/openApi/post/sign", headers=header_iaas, json=data_iaas)
    res_text = res_iaas_sign.text
    if res_iaas_sign.status_code != 200:
        Sign = re.findall(r'serverSign\\":\\"(\w+)\\",', res_text)[0]
        header_iaas["Sign"] = Sign
    res_iaas = requests.post(url=url_iaas + "/openApi/ListInstanceInfo", headers=header_iaas, json=data_iaas)
    res_iaas_json = res_iaas.json()
    iaas_logger.info(f'iaas查询结果为{res_iaas_json}')
    # with lock:
    iaas_instance = list(set(jsonpath.jsonpath(res_iaas_json, "$..instance_id")))
    iaas_sns = list(set(jsonpath.jsonpath(res_iaas.json(), "$..sn")))
    global_data_iaas["instance_ids"] = iaas_instance
    global_data_iaas["card_sns"] = iaas_sns
    iaas_logger.info(f'提取的iaas instance_ids: {iaas_instance}, 提取的iaas card_sns: {iaas_sns}')


def paas_init():
    # 初始化paas参数
    url_paas = global_data_paas.get("url")
    header_paas = global_data_paas.get("header")
    data_paas = {
        "idcs": [global_data_paas.get("idc_init")],
        "vendor": global_data_paas.get("vendor"),
        "instanceType": global_data_paas.get("instance_type")
    }
    # PAAS鉴权请求
    res_paas_sign = requests.post(url=url_paas + "/v1/post/sign", headers=header_paas, json=data_paas)
    res_text = res_paas_sign.text
    if res_paas_sign.status_code != 200:
        Sign = re.findall(r'serverSign\\":\\"(\w+)\\",', res_text)[0]
        header_paas["Sign"] = Sign
    res_paas = requests.post(url=url_paas + "/v1/instance/list", headers=header_paas, json=data_paas)
    res_paas_json = res_paas.json()
    paas_logger.info(f'paas查询结果为{res_paas_json}')
    # with lock:
    paas_instance = jsonpath.jsonpath(res_paas_json, "$..instanceId")
    global_data_paas["instance_ids"] = paas_instance
    paas_logger.info(f'提取的paas instance_ids: {paas_instance}')


def paas_init_repeat():
    # 初始化paas参数
    url_paas = global_data_paas.get("url")
    header_paas = global_data_paas.get("header")
    data_paas = {
        "idcs": [global_data_paas.get("idc_init")],
        "vendor": global_data_paas.get("vendor"),
        "instanceType": global_data_paas.get("instance_type"),
        "pageSize": 1000
    }
    # PAAS鉴权请求
    res_paas_sign = requests.post(url=url_paas + "/v1/post/sign", headers=header_paas, json=data_paas)
    res_text = res_paas_sign.text
    if res_paas_sign.status_code != 200:
        Sign = re.findall(r'serverSign\\":\\"(\w+)\\",', res_text)[0]
        header_paas["Sign"] = Sign
    res_paas = requests.post(url=url_paas + "/v1/instance/list", headers=header_paas, json=data_paas)
    res_paas_json = res_paas.json()
    paas_logger.info(f'paas查询结果为{res_paas_json}')
    # with lock:
    paas_instance = jsonpath.jsonpath(res_paas_json, "$..instanceId")
    global_data_paas["instance_ids"] = paas_instance
    paas_logger.info(f'提取的paas instance_ids: {paas_instance}')

def worker(*args):
    """
    --allure-severities为用例等级，对应用例上@allure.severity
    :param args: 用例路径
    :return:
    """
    pytest.main(['-sv', f'--alluredir={ALLURE_PATH}', *args])


# 程序入口
def main(env, platform, repeat=None):
    """
    :param env: 环境参数 test | poc | prod
    :param platform: 平台参数 iaas | paas | all
    :return:
    测试用例执行命令
    test_case_auth_paas表示执行test_case_auth_paas包下的所有用例文件
    test_case_auth_iaas/test_adb.py表示执行test_case_auth_iaas/test_adb.py文件里的用例
    test_case_auth_iaas/test_instance_paas.py::TestInstancePaas::test_instance_package表示执行test_instance_package用例
    """
    if env.lower() == 'test':
        global_data_paas.update(env_test_paas)
        global_data_iaas.update(env_test_iaas)
    elif env.lower() == 'poc':
        global_data_paas.update(env_poc_paas)
        global_data_iaas.update(env_poc_iaas)
    elif env.lower() == 'prod':
        global_data_paas.update(env_prod_paas)
        global_data_iaas.update(env_prod_iaas)
    else:
        print("请输入正确的环境参数: test | poc | prod")
        return
    if repeat:
        # 采用多线程来执行iaas和paas的测试用例
        if platform.lower() == 'iaas':
            iaas_init_repeat()
            thread_iaas = threading.Thread(target=worker, args=('--allure-severities=critical', f"--count={repeat}", "--repeat-scope=session", os.path.join(BASEDIR, 'test_case_auth_iaas'),))
            thread_iaas.start()
            thread_iaas.join()
        elif platform.lower() == 'paas':
            paas_init_repeat()
            # thread_paas = threading.Thread(target=worker, args=('--allure-severities=critical', f"--count={repeat}", "--repeat-scope=session", os.path.join(BASEDIR, 'test_case_auth_paas'),))
            for i in range(int(repeat)):
                thread_paas = threading.Thread(target=worker, args=('--allure-severities=critical', os.path.join(BASEDIR, 'test_case_auth_paas/test_stream_paas.py'),))
                thread_paas.start()
                thread_paas.join()
        elif platform.lower() == 'all':
            iaas_init_repeat()
            paas_init_repeat()
            thread_iaas = threading.Thread(target=worker, args=('--allure-severities=critical', f"--count={repeat}", "--repeat-scope=session", os.path.join(BASEDIR, 'test_case_auth_iaas'),))
            thread_paas = threading.Thread(target=worker, args=('--allure-severities=critical', f"--count={repeat}", "--repeat-scope=session", os.path.join(BASEDIR, 'test_case_auth_paas'),))
            thread_iaas.start()
            thread_paas.start()
            thread_iaas.join()
            thread_paas.join()
        else:
            print("请输入正确的平台参数: iaas | paas | all")
            return
    else:
        # 采用多线程来执行iaas和paas的测试用例
        if platform.lower() == 'iaas':
            iaas_init()
            thread_iaas = threading.Thread(target=worker, args=('--allure-severities=minor,normal,critical', os.path.join(BASEDIR, 'test_case_auth_iaas'),))
            thread_iaas.start()
            thread_iaas.join()
        elif platform.lower() == 'paas':
            paas_init()
            thread_paas = threading.Thread(target=worker, args=('--allure-severities=minor,normal,critical', os.path.join(BASEDIR, 'test_case_auth_paas'),))
            thread_paas.start()
            thread_paas.join()
        elif platform.lower() == 'all':
            iaas_init()
            paas_init()
            thread_iaas = threading.Thread(target=worker, args=('--allure-severities=minor,normal,critical', os.path.join(BASEDIR, 'test_case_auth_iaas'),))
            thread_paas = threading.Thread(target=worker, args=('--allure-severities=minor,normal,critical', os.path.join(BASEDIR, 'test_case_auth_paas'),))
            thread_iaas.start()
            thread_paas.start()
            thread_iaas.join()
            thread_paas.join()
        else:
            print("请输入正确的平台参数: iaas | paas | all")
            return
    time.sleep(2)
    # 先调用get_dirname()，获取到这次需要构建的次数
    buildOrder, old_data = get_dirname()
    date = time.strftime("%Y_%m_%d %X")
    # 报告界面展示环境信息，可以自定义
    with open(f'{ALLURE_PATH}/environment.properties', 'w', encoding='utf8') as f:
        s = f'''
           Platform=Windows
           Python.Version=3.9
           User=Fu
           Time={date}
               '''
        f.write(s)
    """
    报告界面分类展示不同运行状态的用例统计，可自定义
    name：分类名称
    matchedStatuses：测试用例的运行状态，默认["failed", "broken", "passed", "skipped", "unknown"]
    messageRegex：测试用例运行的错误信息，默认是 .* ，通过正则去匹配
    traceRegex：测试用例运行的错误堆栈信息，默认是 .* ，同样通过正则去匹配
    """
    with open(f'{ALLURE_PATH}/categories.json', 'w', encoding='utf8') as f:
        j = '''
                [
         {
           "name": "测试通过",
           "matchedStatuses": ["passed"]
         },
         {
           "name": "测试跳过",
           "matchedStatuses": ["skipped"]
         },
         {
           "name": "Infrastructure problems",
           "matchedStatuses": ["broken", "failed"],
           "messageRegex": ".*bye-bye.*"
         },
         {
           "name": "Outdated tests",
           "matchedStatuses": ["broken"],
           "traceRegex": ".*FileNotFoundException.*"
         },
         {
           "name": "测试失败",
           "matchedStatuses": ["failed"]
         },
         {
           "name": "测试异常",
           "matchedStatuses": ["broken"]
         }
       ]
                '''
        f.write(j)
    # 再命令行执行报告生成命令
    command = f"{os.getcwd()}/allure-2.17.3/bin/allure generate {ALLURE_PATH} -o {os.path.join(ALLURE_HTML_DIR, str(buildOrder))} --clean"
    # command = f"{os.getcwd()}/allure-2.17.3/bin/allure generate {reduce(lambda x, y: x + ' ' + y, results)} -o {os.path.join(ALLURE_HTML_DIR, str(buildOrder))} --clean"
    os.system(command)
    # 执行完毕后再调用update_trend_data()，处理报告数据
    all_data, reportUrl = update_trend_data(buildOrder, old_data, env)
    # 自动打开报告页面
    webbrowser.open(reportUrl)


if __name__ == '__main__':
    main("test", "paas")
    # ALLURE_PATH = os.path.join(ALLURE_RESULT, str(1742374122))
    # command = f"{os.getcwd()}/allure-2.17.3/bin/allure generate {ALLURE_PATH} -o {os.path.join(ALLURE_HTML_DIR, str(27))} --clean"
    # os.system(command)
