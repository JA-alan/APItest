import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import logging
from config.config import REPORT_DIR

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='test_report.log',
    filemode='a'
)

def send_email(receiver, subject, body, report_file):
    sender = "1753125530@qq.com"  # 发件人邮箱
    password = "wzwzklxjkxbxbdaj"  # 邮箱授权码

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ', '.join(receiver) if isinstance(receiver, list) else receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # 添加附件
    try:
        with open(report_file, "rb") as file:
            part = MIMEApplication(file.read(), Name="test_report.html")
            part['Content-Disposition'] = f'attachment; filename="test_report.html"'
            msg.attach(part)
    except FileNotFoundError:
        logging.error(f"报告文件 {report_file} 未找到，无法添加附件。")

    # 发送邮件
    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        logging.info("邮件发送成功")
    except Exception as e:
        logging.error(f"邮件发送失败: {e}")

def send_test_report():
    try:
        # 配置邮件信息
        email_info = {
            "receiver": ["819823950@qq.com"],
            "title": "接口自动化测试报告",
            "content": "本次接口自动化测试已完成，详细报告请查看附件。"
        }
        logging.info("邮件信息配置完成")

        # 发送邮件
        report_file = REPORT_DIR  # 直接使用 REPORT_DIR 作为报告文件的路径
        send_email(email_info["receiver"], email_info["title"], email_info["content"], report_file)
        logging.info("邮件发送完成")
    except Exception as e:
        logging.error(f"执行过程中出现错误: {e}", exc_info=True)

if __name__ == "__main__":
    send_test_report()