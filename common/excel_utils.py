import openpyxl

def read_excel(file_path):
    """
    读取 Excel 文件中的测试用例数据
    :param file_path: Excel 文件路径
    :return: 测试用例数据列表
    """
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    cases = []
    headers = [cell.value for cell in sheet[1]]
    for row in sheet.iter_rows(min_row=2, values_only=True):
        case = dict(zip(headers, row))
        cases.append(case)
    return cases