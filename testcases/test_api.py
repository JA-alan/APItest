import unittest
from common.excel_utils import read_excel
from common.request_utils import send_request
from config.config import TEST_CASE_FILE
import json
from common.log_utils import logger

class TestAPI(unittest.TestCase):
    # 定义类属性来存储 token
    token = None

    def test_api_cases(self):
        # 读取 Excel 中的测试用例
        cases = read_excel(TEST_CASE_FILE)
        for index, case in enumerate(cases):
            method = case.get('method')
            url = case.get('url')
            headers = case.get('headers') or {'Content-Type': 'application/json'}
            params = case.get('params')
            data = case.get('data')
            json_data = case.get('json')
            expected_status_code = case.get('expected_status_code')

            # 转换 data 字段为字典
            if data and isinstance(data, str):
                try:
                    data = json.loads(data.replace("'", "\""))
                except json.JSONDecodeError:
                    logger.error(f"数据解析错误: {data}")
                    continue

            # 若 json_data 为 None，则使用 data 作为 json 参数
            if json_data is None and data:
                json_data = data

            # 如果不是第一个用例，且 token 已经获取到，将 token 添加到请求头中
            if index > 0 and self.token:
                headers['Authorization'] = f'Bearer {self.token}'

            # 发送请求
            response = send_request(method, url, headers=headers, params=params, json=json_data)

            # 记录请求和响应信息
            logger.info(f"请求信息: method={method}, url={url}, headers={headers}, params={params}, data={data}, json={json_data}")
            if response:
                logger.info(f"响应信息: status_code={response.status_code}, content={response.text}")
            else:
                logger.error("请求失败，未获取到响应信息")

            # 断言响应状态码
            if response:
                self.assertEqual(response.status_code, expected_status_code, f"用例失败: {case}")

            # 如果是第一个用例，尝试从响应中提取 access_token
            if index == 0:
                try:
                    response_data = response.json()
                    # 从 data 字段中提取 access_token
                    data_field = response_data.get('data')
                    if data_field:
                        self.token = data_field.get('token')
                        if self.token:
                            logger.info(f"成功获取到 token: {self.token}")
                        else:
                            logger.error("未从第一个用例响应的 data 字段中获取到 access_token")
                    else:
                        logger.error("第一个用例的响应中没有 data 字段")
                except json.JSONDecodeError:
                    logger.error("无法解析第一个用例的响应为 JSON 格式")

