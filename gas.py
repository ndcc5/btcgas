import requests
import time
import smtplib
from email.mime.text import MIMEText

# 配置参数
api_url = "https://mempool.space/api/v1/fees/recommended"
gas_file = "gas.txt"
response = requests.get(api_url)
fastest_fee = response.json()["fastestFee"]

with open(gas_file, "a") as file:
    file.write(str(fastest_fee) + "\n")

interval = 60  # 每隔1分钟运行一次
threshold = 1.2  # 如果比上次增加20%以上，发送邮件通知
sender_email = "你的发送邮箱"
sender_password = "发送邮箱密码"
receiver_email = "你的接收邮箱"

def get_bitcoin_fee():
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()
        fee_per_byte = data["fastestFee"]
        return fee_per_byte
    except (requests.exceptions.RequestException, requests.exceptions.JSONDecodeError) as e:
        print("Error occurred while retrieving Bitcoin fee:", str(e))
        return None

def send_email(subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    with smtplib.SMTP_SSL("smtp.qq.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

def check_gas_increase():
    current_gas = get_bitcoin_fee()
    if current_gas is not None:
        with open(gas_file, "r+") as file:
            content = file.read().strip()
            if content:
                previous_gas = float(content.split("\n")[-1])
                if current_gas > previous_gas * threshold:
                    subject = "Gas Fee Increase Alert"
                    message = f"The gas fee has increased by more than {threshold * 100}%.\n\nPrevious gas fee: {previous_gas}\nCurrent gas fee: {current_gas}"
                    send_email(subject, message)

            file.seek(0)
            file.write(str(current_gas) + "\n")

while True:
    check_gas_increase()
    time.sleep(interval)
