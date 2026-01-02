import time
from signin import HuluxiaSignin
import os
from logger import logger

accounts_str = os.getenv('ACCOUNTS')
if not accounts_str:
    logger.error("环境变量 ACCOUNTS  未设置")
    raise ValueError("环境变量 ACCOUNTS  未设置")

accounts = []
for acc in accounts_str.split('\n'):
    try:
        phone, password = acc.split(',')
        accounts.append((phone.strip(), password.strip()))
    except ValueError:
        logger.warning(f"账号信息格式不正确：{acc}")

huluxia_signin_obj = HuluxiaSignin()

for idx, (phone, password) in enumerate(accounts, 1):
    try:
        huluxia_signin_obj.huluxia_signin(phone, password)
        logger.info(f"账号 {phone} 签到成功")
        if idx < len(accounts):
            time.sleep(60)
    except Exception as e:
        logger.error(f"账号 {phone} 签到失败: {e}")
        if idx < len(accounts):
            time.sleep(10)
