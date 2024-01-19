# btcgas
检测比特币gas费突然暴涨，邮件通知。
安装扩展组件
npm install time
npm install smtplib 
npm install time
=========================================
修改gas.py文件中的
interval = 60  # 每隔1分钟运行一次
threshold = 1.2  # 如果比上次增加20%以上，发送邮件通知
sender_email = "你的发送邮箱"
sender_password = "发送邮箱密码"
receiver_email = "你的接收邮箱"
==================================================

启动
python gas.py
========================================================
