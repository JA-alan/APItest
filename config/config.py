import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 定义一个函数来扫描指定目录下的所有 xlsx 文件
def scan_xlsx_files(directory):
    xlsx_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xlsx'):
                xlsx_files.append(os.path.join(root, file))
    return xlsx_files

# 测试用例文件所在目录
TEST_CASE_DIR = os.path.join(BASE_DIR, 'testcases')

# 自动扫描测试用例目录下的所有 xlsx 文件
TEST_CASE_FILES = scan_xlsx_files(TEST_CASE_DIR)

# 测试报告文件路径
REPORT_DIR = os.path.join(BASE_DIR, 'reports', 'test_report.html')

# 输出 REPORT_DIR 的值，用于调试
print(f"测试报告文件路径: {REPORT_DIR}")