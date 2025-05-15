import requests
import json
from config.config import REPORT_DIR

def send_to_wechatbot(webhook_url):
    # 读取测试报告内容，这里假设报告是 HTML 格式，简单示例读取部分信息
    try:
        with open(REPORT_DIR, 'r', encoding='utf-8') as f:
            report_content = f.read()
            # 从报告中提取测试结果信息，这里简单假设报告中有总用例数、通过数、失败数、错误数
            total_count = 0
            pass_count = 0
            fail_count = 0
            error_count = 0
            # 简单模拟从报告中提取数据，实际需要根据报告格式解析
            if '共 ' in report_content:
                total_count = int(report_content.split('共 ')[1].split('，')[0])
            if '通过 ' in report_content:
                pass_count = int(report_content.split('通过 ')[1].split('，')[0])
            if '失败 ' in report_content:
                fail_count = int(report_content.split('失败 ')[1].split('，')[0])
            if '错误 ' in report_content:
                error_count = int(report_content.split('错误 ')[1].split('，')[0])

            # 构建要发送的消息内容
            message = {
                "msgtype": "text",
                "text": {
                    "content": f"接口自动化测试结果：\n总用例数：{total_count}\n通过数：{pass_count}\n失败数：{fail_count}\n错误数：{error_count}"
                }
            }
            # 发送消息到企业微信机器人
            headers = {'Content-Type': 'application/json'}
            response = requests.post(webhook_url, headers=headers, data=json.dumps(message))
            if response.status_code == 200:
                print("消息发送成功")
            else:
                print(f"消息发送失败，状态码：{response.status_code}，响应内容：{response.text}")
    except Exception as e:
        print(f"读取报告或发送消息时出错：{e}")
