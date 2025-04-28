import requests

def send_request(method, url, headers=None, params=None, data=None, json=None):
    """
    发送 HTTP 请求
    :param method: 请求方法，如 GET、POST 等
    :param url: 请求 URL
    :param headers: 请求头
    :param params: 请求参数（GET 请求使用）
    :param data: 请求数据（表单数据）
    :param json: 请求数据（JSON 格式）
    :return: 响应对象
    """
    try:
        print(f"请求信息: method={method}, url={url}, headers={headers}, params={params}, data={data}, json={json}")
        response = requests.request(method, url, headers=headers, params=params, data=data, json=json, verify=False)
        print(f"响应信息: status_code={response.status_code}, content={response.text}")
        return response
    except Exception as e:
        print(f"请求出错: {e}")
        return None