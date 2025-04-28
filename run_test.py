import unittest
from HTMLTestRunner import HTMLTestRunner
from config.config import REPORT_DIR
from common.email_utils import send_test_report

def run_tests():
    try:
        # 加载测试用例
        test_loader = unittest.TestLoader()
        test_suite = test_loader.discover('testcases', pattern='test_*.py')

        # 定义测试报告文件名
        report_file = open(REPORT_DIR, 'wb')

        # 创建 HTMLTestRunner 对象
        runner = HTMLTestRunner(stream=report_file, title='接口自动化测试报告', description='测试用例执行情况')

        # 运行测试用例
        runner.run(test_suite)
        print('测试套件执行成功')
    except Exception as e:
        print(f'执行测试套件时出错：{e}')
    finally:
        # 关闭报告文件
        if 'report_file' in locals():
            report_file.close()

    # 发送测试报告邮件
    try:
        send_test_report()
        print("测试报告邮件发送成功")
    except Exception as e:
        print(f"发送测试报告邮件时出错: {e}")

if __name__ == "__main__":
    run_tests()
