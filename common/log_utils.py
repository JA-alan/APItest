import logging
import os
from config.config import BASE_DIR

def setup_logger():
    # 创建一个日志器
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # 创建日志文件的绝对路径
    log_file_path = os.path.join(BASE_DIR, 'logs', 'test.log')
    # 创建日志文件夹（如果不存在）
    log_dir = os.path.dirname(log_file_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 创建一个文件处理器
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # 创建一个控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # 创建一个格式化器并添加到处理器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 将处理器添加到日志器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()