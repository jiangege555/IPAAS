# 生成签名sign传给header中的Sign
from enum import Enum
import hashlib
import json

FIELD_SIGN = 'sign'


class SignType(Enum):
    MD5 = 'MD5'
    HMACSHA256 = 'HMACSHA256'


def generate_signature(data: dict, app_id: str, app_security: str, sign_type: SignType) -> str:
    # 去掉 null 和 undefined 的参数
    data = {k: v for k, v in data.items() if v is not None}

    # 排序参数
    sorted_data = sorted(data.items())

    param_list = []

    for item, value in sorted_data:
        if item == FIELD_SIGN:
            continue

        # 处理对象和数组类型的值
        if isinstance(value, (dict, list)):
            # 如果是字典或列表，转换为 JSON 字符串
            str_value = json.dumps(value, separators=(',', ':'), ensure_ascii=False)
        else:
            # 其他类型（字符串、数字、布尔值等），转换为字符串
            str_value = str(value).strip() if value is not None else ""

        # 无论值是否为空，都拼接为 参数名=值 的形式
        param_list.append(f"{item}={str_value}")

    # 拼接参数
    if param_list:
        param_str = '&'.join(param_list)
        param_str += f"&ak={app_id}&sk={app_security}"
    else:
        param_str = f"ak={app_id}&sk={app_security}"

    # 替换特殊字符
    param_str = (
        param_str.replace("'", '"')
        # .replace(" ", "")
        .replace("True", "true")
        .replace("False", "false")
        .replace("None", "null")
    )
    print("Param String:", param_str)

    # 生成签名
    if sign_type == SignType.MD5:
        return md5(param_str).upper()
    else:
        raise ValueError(f"Unsupported sign type: {sign_type}")

def generate_signature1(data, ak, sk, sign_type=SignType.MD5):
    """
    Generate signature for the given data

    Args:
        data: Dictionary of data to sign
        app_id: Application ID (ak)
        app_security: Application security key (sk)
        sign_type: Type of signature to generate (default: MD5)

    Returns:
        str: Generated signature in uppercase
    """
    # Remove null/None values
    data = {k: v for k, v in data.items() if v is not None}

    # Sort parameters
    sorted_data = sorted(data.items())

    param_list = []

    for key, value in sorted_data:
        if key == FIELD_SIGN:
            continue

        # Handle different value types
        if isinstance(value, (dict, list)):
            # Convert objects/arrays to JSON string
            str_value = json.dumps(value, separators=(',', ':'), ensure_ascii=False)
        else:
            # Convert other types to string
            str_value = str(value).strip() if value is not None else ""

        param_list.append(f"{key}={str_value}")

    # Build parameter string
    if param_list:
        param_str = '&'.join(param_list) + f"&ak={ak}&sk={sk}"
    else:
        param_str = f"ak={ak}&sk={sk}"

    print("Param String:", param_str)

    # Generate signature
    if sign_type == SignType.MD5:
        return md5(param_str).upper()
    else:
        raise ValueError(f"Unsupported sign type: {sign_type}")

def md5(data: str) -> str:
    # 计算 MD5 哈希值
    md5_hash = hashlib.md5()
    md5_hash.update(data.encode('utf-8'))
    return md5_hash.hexdigest()


if __name__ == '__main__':
    # ak = "3ef0ac13-8771-4ba7-9ed3-9d7a981ac5fc"
    # sk = "b6067910-934b-440b-8ac7-62afd5048604"
    # ak = "6fe85202-5992-4b10-9b10-eeba5e0124ec"
    # sk = "41be8410-9b8f-40cc-80d9-94acc1cf60f0"
    # ak = "df401528-2ae1-4afc-acbc-6b5bbd249259"
    # sk = "e5056491-6f84-4092-a75c-338cec81f2a3"
    data = {"a":False,"instance_id": ["RK8S30P1202300459_81db32d3-9153-40a4-b1e1-c1c6543d898a", "RK8S30P1202300460_7de45bcf-ee3c-4d8f-a748-a3771a1d32c5", "RK8S30P1202300460_0ce32c1d-b488-4601-946d-3fd9c0f7e271", "RK8S30P1202300460_b53c85b0-ced1-4ab1-8a52-4eb5a60d9c9d", "RK8S30P1202300460_e44eee6f-97cd-4e3e-aa61-2d4c63de9499", "RK8S30P1202300459_16dc229d-3dfd-421e-aa5f-356bbdd71489", "RK8S30P1202300460_a980e05d-72cb-49e6-9b2e-e091f93039b9", "RK8S30P1202300459_a9b3f4f2-47ca-4a4a-a2e9-11580c3a261b", "RK8S30P1202300459_8ddea9ed-19b0-4707-bb46-a369f53d786c", "RK8S30P1202300459_2379de41-54b1-4a51-8f97-37c33305be94"], "image_id": "848", "saveprop": []}
    ak = "05fcc5c8-1d6b-4be2-afce-de3124eed19d"
    sk = "3c4c61c6-baf9-4ead-b1b8-c1cb5d961b8c"
    sign = generate_signature(data, ak, sk, SignType.MD5)
    sign1 = generate_signature1(data, ak, sk, SignType.MD5)
    print("生成的签名为:", sign, sign1)
    # v = ""
    # if v is not None:
    #     print(1)
    # else:
    #     print(2)