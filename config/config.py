# 配置文件
import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Excel 测试用例文件路径
TEST_CASE_FILE = os.path.join(BASE_DIR, 'testcases', 'test_cases.xlsx')

# 测试报告文件路径
REPORT_FILE = os.path.join(BASE_DIR, 'reports', 'test_report.html')