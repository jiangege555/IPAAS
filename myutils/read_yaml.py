import json
import os
import yaml, random
from jinja2 import Environment

"""
自定义过滤器，yaml文件中使用模板语法传递、处理变量，过滤器默认接受一个参数value，为 "|" 符号前面的输出内容，可以多传参数，过滤器使用时传入
相关资料：https://wenku.csdn.net/column/8b43ap1qar#1.2%20Jinja2%E7%9A%84%E5%9F%BA%E6%9C%AC%E7%94%A8%E6%B3%95
自带的过滤器大全：https://blog.csdn.net/weixin_56670311/article/details/146240387
"""


# class KeepTemplateUndefined(Undefined):
#     def __str__(self):
#         # 返回未渲染的变量，但用引号包裹避免 YAML 报错
#         return f'"{{{{{self._undefined_name}}}}}"'


def random_one_from_list(value):
    return random.choice(value)


def remove_one_from_list(value, item):
    value.remove(item)
    return value


def get_random_int(value, min_value, max_value):
    value = random.randint(min_value, max_value)
    return value


# env = Environment(undefined=KeepTemplateUndefined)
env = Environment()
# 将自定义的过滤器添加到env中,在yaml文件中使用{{ value | random_one }}的方式调用
env.filters['random_one'] = random_one_from_list
env.filters['remove_one'] = remove_one_from_list
env.filters['random_int'] = get_random_int


def read_testcase_yaml(path: str, name, new_data:dict=None):
    with open(path, mode='r', encoding='utf-8') as f:
        string_var = f.read()
        if new_data:
            response = env.from_string(string_var).render(new_data)
            data = yaml.safe_load(response)
            # return [case for case in data[name]]
        else:
            data = yaml.safe_load(string_var)
        for case in data[name]:
            if 'mark' in case:
                case['mark'] = [case.pop('mark')] if isinstance(case['mark'], str) else case.pop('mark')
            case.setdefault('mark', [])
        return data[name]
        # return response


def check_info_yaml(case_info):
    # 获取列表所有的key
    # case_info = case_info[0]
    case_info_keys = case_info.keys()
    # 首先判断caseInfo中是否包含必填的字段
    if 'name' in case_info_keys and 'request' in case_info_keys:
        # 获取request中所有的key
        request_keys = case_info['request'].keys()
        # 判断request中是否包含url、headers、params
        if 'url' in request_keys and 'headers' in request_keys and 'params' in request_keys:
            print("yaml用例标准化格式：校验通过")
        else:
            print("二级关键词必须包含：url,headers,params")
    else:
        print("一级关键词必须包含：name,request,assert")


if __name__ == '__main__':
    from string import Template
    global_data_paas = {"instance_ids": ["aaa","22bb2","33b3","bb"],"brand":"111","model":"222"}
    res = read_testcase_yaml("../test_case_auth_paas/204d.yaml", "test_204d", global_data_paas)
    # print(res)
    print(json.dumps(res[3].get("request")))
    temp = Template(json.dumps(res[3].get("request")))
    # print(temp)
    data = json.loads(temp.safe_substitute(global_data_paas))
    print(data)
    # case_info = res[0]
    # print(case_info)
    # name = case_info.get("name")
    # mark = case_info.get("mark")
    # url = case_info.get("request").get("url")
    # method = case_info.get("request").get("method")
    # is_async = case_info.get("request").get("async")
    # data = case_info.get("request").get("data")
    # extract = case_info.get("extract")
    # validate = case_info.get("validate")
    # before_request = case_info.get("before_request")
    # if not is_async:
        # print("异步")
        # print(case_info)
        # print(name)
        # print(mark)
        # print(url)
        # print(method)
        # print(is_async)
        # print(data)
        # print(extract)
        # print(validate)
    # print(before_request)
    # if before_request:
    #     print(before_request)
    # ret = var_rendering(res.get("request").get("datas"), global_data_paas)
    # ret = {'test_stream_create': [{'name': '创建群控会话', 'request': {'url': '/v1/multiple/stream/session/create', 'method': 'post', 'async': "False", 'datas': {'masterInstanceId': '111', 'slaveInstanceIds': ['222', '333']}}, 'extract': {'sessionId': {'path': '$.data.sessionId', 'index': 0, 'key': 'session_id'}}, 'validate': {'status': {'path': '$.status', 'index': 0, 'way': '==', 'value': 0}, 'sessionId': {'path': '$.data.sessionId', 'index': -1, 'way': '!=', 'value': "False"}, 'failInstanceIds': {'path': '$.data.failInstanceIds', 'index': 0, 'way': '==', 'value': []}}}]}
    # print(ret)
    # print(json.loads(str(ret)))
    # si = res.get("test_stream_create")[0].get("validate").get("status").get("way")
    # print(si)
    # assert eval(f"1 {si} 2")
