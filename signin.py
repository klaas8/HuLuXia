import hashlib
import json
import os
import random
import time
import requests
from logger import logger

phone_brand_type_list = list(["MI", "Huawei", "UN", "OPPO", "VO"])
device_code_random = random.randint(111, 987)

platform = '2'
gkey = '000000'
app_version = '4.3.1.5.2'
versioncode = '398'
market_id = 'floor_web'
device_code = '%5Bd%5D5125c3c6-f' + str(device_code_random) + '-4c6b-81cf-9bc467522d61'
phone_brand_type = random.choice(phone_brand_type_list)
_key = ''
cat_id = ''
userid = ''
signin_continue_days = ''
headers = {
    "Connection": "close",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "User-Agent": "okhttp/3.8.1",
    "Host": 'floor.huluxia.com'
}
session = requests.Session()
with open('cat_id.json', 'r', encoding='UTF-8') as f:
    content = f.read()
    cat_id_dict = json.loads(content)

class HuluxiaSignin:
    def __init__(self):
        self._key = ''
        self.cat_id = ''
        self.userid = ''
        self.signin_continue_days = ''

    def psd_login(self, account, password):
        device_model = f"iPhone{random.randint(14, 17)}%2C{random.randint(1, 6)}"
        login_url = 'https://floor.huluxia.com/account/login/IOS/1.0?' \
                    'access_token=&app_version=1.2.2&code=' \
                    '&device_code=' + device_code + \
                    '&device_model=' + device_model + \
                    '&email=' + account + \
                    '&market_id=floor_huluxia&openid=&' \
                    'password=' + self.md5(password) + \
                    '&phone=' \
                    '&platform=1'
        login_res = session.get(url=login_url, headers=headers)
        return login_res.json()

    def set_config(self, acc, psd):
        data = self.psd_login(acc, psd)
        status = data['status']
        if status != 0:
            self._key = data['_key']
            self.userid = data['user']['userID']
            return self._key

    def user_info(self):
        get_info_url = 'http://floor.huluxia.com/user/info/ANDROID/4.1.8?' \
                       'platform=' + platform + \
                       '&gkey=' + gkey + \
                       '&app_version=' + app_version + \
                       '&versioncode=' + versioncode + \
                       '&market_id=' + market_id + \
                       '&_key=' + self._key + \
                       '&device_code=' + device_code + \
                       '&phone_brand_type=' + phone_brand_type + \
                       '&user_id=' + str(self.userid)
        get_info_res = requests.get(url=get_info_url, headers=headers).json()
        nick = get_info_res['nick']
        level = get_info_res['level']
        exp = get_info_res['exp']
        next_exp = get_info_res['nextExp']
        return nick, level, exp, next_exp

    def md5(self, text: str) -> str:
        _md5 = hashlib.md5()
        _md5.update(text.encode())
        return _md5.hexdigest()

    def timestamp(self) -> int:
        return int(time.time())

    def sign_get(self) -> str:
        n = self.cat_id
        i = str(self.timestamp())
        r = 'fa1c28a5b62e79c3e63d9030b6142e4b'
        result = "cat_id" + n + "time" + i + r
        c = self.md5(result)
        return c

    def huluxia_signin(self, acc, psd):
        self.set_config(acc, psd)
        info = self.user_info()
        initial_msg = f'正在为{info[0]}签到\n等级：Lv.{info[1]}\n经验值：{info[2]}/{info[3]}'
        logger.info(initial_msg)
        total_exp = 0
        for ct in cat_id_dict.keys():
            self.cat_id = ct
            sign = self.sign_get().upper()
            signin_url = (
                f"http://floor.huluxia.com/user/signin/ANDROID/4.1.8?"
                f"platform={platform}&gkey={gkey}&app_version={app_version}&versioncode={versioncode}"
                f"&market_id={market_id}&_key={self._key}&device_code={device_code}"
                f"&phone_brand_type={phone_brand_type}&cat_id={self.cat_id}&time={self.timestamp()}"
            )
            post_data = {"sign": sign}
            try:
                signin_res = session.post(url=signin_url, headers=headers, data=post_data).json()
            except Exception as e:
                error_msg = f"签到过程中出现错误：{e}"
                logger.error(error_msg)
                break
            if signin_res.get('status') == 0:
                fail_msg = f'【{cat_id_dict[self.cat_id]}】签到失败，请手动签到。'
                logger.warning(fail_msg)
                time.sleep(3)
                continue
            signin_exp = signin_res.get('experienceVal', 0)
            self.signin_continue_days = signin_res.get('continueDays', 0)
            success_msg = f'【{cat_id_dict[self.cat_id]}】签到成功，经验值 +{signin_exp}'
            logger.info(success_msg)
            total_exp += signin_exp
            time.sleep(3)
        summary_msg = f'本次为{info[0]}签到共获得：{total_exp} 经验值'
        logger.info(summary_msg)
        final_info = self.user_info()
        final_msg = f'已为{final_info[0]}完成签到\n等级：Lv.{final_info[1]}\n经验值：{final_info[2]}/{final_info[3]}\n已连续签到 {self.signin_continue_days} 天\n'
        remaining_days = (int(final_info[3]) - int(final_info[2])) // total_exp + 1 if total_exp else "未知"
        final_msg += f'还需签到 {remaining_days} 天'
        logger.info(final_msg)