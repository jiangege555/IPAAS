import requests


def my_request(url, method, data=None, headers=None, verify=False):
    if method == "get":
        response = requests.get(url=url, params=data, headers=headers, verify=verify)
    elif method == "post":
        response = requests.post(url=url, json=data, headers=headers, verify=verify)
    elif method == "delete":
        response = requests.delete(url=url, json=data, headers=headers, verify=verify)
    elif method == "put":
        response = requests.put(url=url, json=data, headers=headers, verify=verify)
    else:
        response = requests.post(url=url, json=data, headers=headers, verify=verify)
    return response