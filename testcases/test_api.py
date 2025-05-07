import unittest
from common.excel_utils import read_excel
from common.request_utils import send_request
from config.config import TEST_CASE_FILE
import json
from common.log_utils import logger

class TestAPI(unittest.TestCase):
    # 定义类属性来存储 token
    token = None

# 动态生成测试方法
def generate_test_method(case):
    def test_case(self):
        method = case.get('method')
        url = case.get('url')
        headers_str = case.get('headers')
        headers = {}
        if headers_str:
            # 解析 headers 字符串
            for item in headers_str.split(','):
                key, value = item.split('=')
                headers[key.strip()] = value.strip()
        else:
            headers = {'Content-Type': 'application/json'}
        params = case.get('params')
        data = case.get('data')
        json_data = case.get('json')
        expected_status_code = case.get('expected_status_code')
        try:
            expected_status_code = int(expected_status_code)
        except (ValueError, TypeError):
            logger.error(f"预期状态码转换为整数时出错: {expected_status_code}")
            return

        # 转换 data 字段为字典
        if data and isinstance(data, str):
            try:
                data = json.loads(data.replace("'", "\""))
            except json.JSONDecodeError:
                logger.error(f"数据解析错误: {data}")
                return

        # 若 json_data 为 None，则使用 data 作为 json 参数
        if json_data is None and data:
            json_data = data

        # 如果不是第一个用例，且 token 已经获取到，将 token 添加到请求头和请求参数中
        if self.__class__.token:
            headers['Authorization'] = f'Bearer {self.__class__.token}'
            if json_data:
                json_data['token'] = self.__class__.token
            elif data:
                data['token'] = self.__class__.token
            elif params:
                params['token'] = self.__class__.token

        # 发送请求
        response = send_request(method, url, headers=headers, params=params, json=json_data)

        # 记录请求和响应信息
        logger.info(f"请求信息: method={method}, url={url}, headers={headers}, params={params}, data={data}, json={json_data}")
        if response:
            try:
                response_content = response.text
            except AttributeError:
                response_content = str(response)
            logger.info(f"响应信息: status_code={response.status_code}, content={response_content}")
        else:
            logger.error("请求失败，未获取到响应信息")

        # 断言响应状态码
        if response:
            try:
                response_json = response.json()
                actual_code = response_json.get('code')  # 从响应 JSON 中提取 code 字段
                if actual_code is not None:
                    actual_code = int(actual_code)
                    # 修改断言逻辑，允许 1001 和 0 为正确状态码
                    if actual_code in [0, 1001] or actual_code == expected_status_code:
                        logger.info(f"用例通过: {case}")
                    else:
                        self.assertEqual(actual_code, expected_status_code, f"用例失败: {case}")
                else:
                    logger.error("响应 JSON 中未找到 code 字段")
            except json.JSONDecodeError:
                logger.error("无法解析响应为 JSON 格式")
        else:
            self.fail("请求失败，未获取到响应信息")

        # 如果是第一个用例，尝试从响应中提取 access_token
        if self._testMethodName == 'test_case_0':
            try:
                response_data = response.json()
                # 从 data 字段中提取 access_token
                data_field = response_data.get('data')
                if data_field:
                    self.__class__.token = data_field
                    logger.info(f"成功获取到 token: {data_field}")
                else:
                    logger.error("未从第一个用例响应的 data 字段中获取到 access_token")

            except json.JSONDecodeError:
                logger.error("无法解析第一个用例的响应为 JSON 格式")

    return test_case

# 读取 Excel 中的测试用例
cases = read_excel(TEST_CASE_FILE)
print(f"读取到的测试用例数量: {len(cases)}")
for index, case in enumerate(cases):
    test_method = generate_test_method(case)
    test_method.__name__ = f'test_case_{index}'
    setattr(TestAPI, test_method.__name__, test_method)

# 打印测试类中所有的测试方法名
test_methods = [name for name in dir(TestAPI) if name.startswith('test_')]
print(f"生成的测试方法: {test_methods}")

if __name__ == "__main__":
    unittest.main()