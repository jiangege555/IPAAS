import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.adapters import HTTPAdapter
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()
# 设置连接池和重试策略
adapter = HTTPAdapter(
    pool_connections=20,  # 连接池大小
    pool_maxsize=20,
    max_retries=3,       # 最大重试次数
)
session.mount("http://", adapter)
session.mount("https://", adapter)


def my_request(url, method, data=None, headers=None, verify=False):
    if method == "get":
        response = session.get(url=url, params=data, headers=headers, verify=verify)
    elif method == "post":
        response = session.post(url=url, json=data, headers=headers, verify=verify)
    elif method == "delete":
        response = session.delete(url=url, json=data, headers=headers, verify=verify)
    elif method == "put":
        response = session.put(url=url, json=data, headers=headers, verify=verify)
    else:
        response = session.post(url=url, json=data, headers=headers, verify=verify)
    return response