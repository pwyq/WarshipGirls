# -*- coding: utf-8 -*-
import sys
import re
import datetime
import time
import json
import os
import random
import logging
import shutil
import base64
import hashlib
import hmac
import urllib
import urllib3
import zlib


import requests
import requests.exceptions


is_write = False

#=====================================================================================
HEADER = {'Accept-Encoding': 'identity',
          'Connection': 'Keep-Alive',
          'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; mi max Build/LMY48Z)'}


class Session:
    def __init__(self):
        self.session = requests.session()

    def new_session(self):
        self.session = requests.session()
        self.session.keep_alive = False

    def get(self, url, **kwargs):
        for i in range(5):
            try:
                r = self.session.get(url=url, **kwargs)
                r.close()
                return r
            except requests.exceptions.ConnectTimeout:
                if i == 4:
                    raise

    def post(self, url, data=None, json=None, **kwargs):
        for i in range(5):
            try:
                r = self.session.post(url=url, data=data, json=json, **kwargs)
                r.close()
                return r
            except requests.exceptions.ConnectTimeout:
                if i == 4:
                    raise

session = Session()

#=================================================================================

VERSION = "1.7.1.0"
BUILD_VERSION = 3

RES = {2: '油', 3: '弹', 4: '钢', 9: '铝', 10141: "航母核心", 10241: '战列核心', 10341: '巡洋核心', 10441: '驱逐核心',
       10541: '潜艇核心', 141: '快速建造', 241: '建造蓝图', 541: '快速修理', 741: '装备蓝图', 66641: '损管'}

HEADER = {'Accept-Encoding': 'identity',
          'Connection': 'Keep-Alive',
          'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; mi max Build/LMY48Z)'}

UPDATE_URL = "http://update.protector.moe/pc/version.json"
DOWNLOAD_URL = "https://github.com/ProtectorMoe/pc-protector-moe/releases/latest"

class G:
    def __init__(self):
        self.repair_time_limit = 0
        self.all_log = 0

g = G()


class InitData:
    def __init__(self):
        self.init_out_data = False
        self.init_version = None
        self.init_data = dict()
        self.ship_cid = dict()
        self.ship_cid_wu = dict()
        self.error_code = dict()
        self.error_code_1 = dict()
        self.handbook_id = dict()
        self.new_init_version = None
        self.ship_equipmnt = {}
        self.res_url = ""

    def read_init(self):
        if not os.path.exists('data'):
            os.mkdir('data')
        if os.path.exists('data/init.json'):
            with open('data/init.json', 'r') as f:
                data = f.read()
            self.init_data = json.loads(data)
            #对比数据版本默认设置低版本
            self.init_version = '20180927142352'
            if "DataVersion" in self.init_data:
                self.init_version = self.init_data["DataVersion"]
            if "res_url" in self.init_data:
                self.res_url = self.init_data["res_url"]
            # 领导船只cid数据
            for each_ship in self.init_data['shipCard']:
                self.ship_cid[each_ship['cid']] = each_ship
            # 普通船只cid数据
            for each_ship in self.init_data['shipCardWu']:
                self.ship_cid_wu[each_ship['cid']] = each_ship
            # 错误代码
            self.error_code_1 = self.init_data['errorCode']
            for code, message in self.error_code_1.items():
                self.error_code[int(code)] = message
            # 图鉴代号
            for each_ship in self.init_data['shipCard']:
                if 'shipIndex' in each_ship:
                    self.handbook_id[each_ship['cid']] = each_ship['shipIndex']
            # 装备属性
            for equipment in self.init_data['shipEquipmnt']:
                self.ship_equipmnt[equipment["cid"]] = equipment


init_data = InitData()



# ============================================================

class GameLogin:
    """
    第一次: channal cookie version server_list
    的二次: 什么也不返回,用于初始化游戏数据
    """
    def __init__(self):
        self.pastport_headers = {
            "Accept-Encoding": "gzip",
            'User-Agent': 'okhttp/3.4.1',
            "Content-Type": "application/json; charset=UTF-8"
        }
        self.init_data_version = "0"
        self.hm_login_server = ""
        self.portHead = ""
        self.key = "kHPmWZ4zQBYP24ubmJ5wA4oz0d8EgIFe"
        self.login_server = ""
        self.res = ""

        # 第一次登录返回值
        self.version = "4.7.0"
        self.channel = '100015'
        self.cookies = None
        self.server_list = []  # 不同服务器的索引
        self.defaultServer = 0
        self.uid = None

        # 状态寄存器

    # 第一次登录,获取cookies和服务器列表
    def first_login_usual(self, server, username, pwd):
        """
        第一次登录,获取cookies和服务器列表
        :return:
    """
        url_version = ""
        if server == 0:  # 安卓服
            url_version = 'http://version.jr.moefantasy.com/' \
                          'index/checkVer/4.5.0/100016/2&version=4.5.0&channel=100016&market=2'
            self.res = 'http://login.jr.moefantasy.com/index/getInitConfigs/'
            self.channel = "100016"
            self.portHead = "881d3SlFucX5R5hE"
            self.key = "kHPmWZ4zQBYP24ubmJ5wA4oz0d8EgIFe"
        elif server == 1:  # ios服
            url_version = 'http://version.jr.moefantasy.com/' \
                          'index/checkVer/4.7.0/100015/2&version=4.7.0&channel=100015&market=2'
            self.res = 'http://loginios.jr.moefantasy.com/index/getInitConfigs/'
            self.channel = "100015"
            self.portHead = "881d3SlFucX5R5hE"
            self.key = "kHPmWZ4zQBYP24ubmJ5wA4oz0d8EgIFe"
        # 请求version
        # -------------------------------------------------------------------------------------------
        # 拉取版本信息
        response_version = session.get(url=url_version, headers=HEADER, timeout=10)
        response_version = response_version.text
        response_version = json.loads(response_version)
        init_data.new_init_version = response_version['DataVersion']
        if is_write and os.path.exists('requestsData'):
            with open('requestsData/version.json', 'w') as f:
                f.write(json.dumps(response_version))

        # 获取版本号, 登录地址
        self.version = response_version["version"]["newVersionId"]
        self.login_server = response_version["loginServer"]
        self.hm_login_server = response_version["hmLoginServer"]

        # -------------------------------------------------------------------------------------------
        # 进行登录游戏
        server_data = self.login_usual(server=server, username=username, pwd=pwd)

        self.defaultServer = int(server_data["defaultServer"])
        self.server_list = server_data["serverList"]
        self.uid = server_data["userId"]

        return_data = {
            "version": self.version,
            "channel": self.channel,
            "cookie": self.cookies,
            "server_list": self.server_list,
            "default_server": self.defaultServer,
            "uid": self.uid
        }
        return True

    # 第二次登录,用于连接对应服务器
    def second_login(self, host, uid):
        # 生成随机设备码
        now_time = str(int(round(time.time() * 1000)))
        random.seed(hashlib.md5(self.uid.encode('utf-8')).hexdigest())
        data_dict = {'client_version': self.version,
                     'phone_type': 'huawei tag-al00',
                     'phone_version': '5.1.1',
                     'ratio': '1280*720',
                     'service': 'CHINA MOBILE',
                     'udid': str(random.randint(100000000000000, 999999999999999)),
                     'source': 'android',
                     'affiliate': 'WIFI',
                     't': now_time,
                     'e': self.get_url_end(now_time),
                     'gz': '1',
                     'market': '2',
                     'channel': self.channel,
                     'version': self.version
                     }
        random.seed()
        # 获取欺骗数据
        login_url_1 = host + 'index/login/' + uid + '?&' + urllib.parse.urlencode(data_dict)
        session.get(url=login_url_1, headers=HEADER, cookies=self.cookies, timeout=10)

        url_cheat = host + 'pevent/getPveData/' + self.get_url_end()
        pevent_getPveData = json.loads(
            zlib.decompress(session.get(url=url_cheat, headers=HEADER, cookies=self.cookies, timeout=10).content))
        if is_write and os.path.exists('requestsData'):
            with open("requestsData/pevent_getPveData.json", 'w') as f:
                f.write(json.dumps(pevent_getPveData))

        url_cheat = host + 'shop/canBuy/1/' + self.get_url_end()
        shop_canbuy = json.loads(
            zlib.decompress(session.get(url=url_cheat, headers=HEADER, cookies=self.cookies, timeout=10).content))
        if is_write and os.path.exists('requestsData'):
            with open("requestsData/shop_canbuy.json", 'w') as f:
                f.write(json.dumps(shop_canbuy))

        url_cheat = host + 'live/getUserInfo' + self.get_url_end()
        shop_canbuy = json.loads(zlib.decompress(
            session.get(url=url_cheat, headers=HEADER, cookies=self.cookies, timeout=10).content))
        if is_write and os.path.exists('requestsData'):
            with open("requestsData/live_getUserInfo.json", 'w') as f:
                f.write(json.dumps(shop_canbuy))

        url_cheat = host + 'live/getMusicList/' + self.get_url_end()
        shop_canbuy = json.loads(zlib.decompress(
            session.get(url=url_cheat, headers=HEADER, cookies=self.cookies, timeout=10).content))
        if is_write and os.path.exists('requestsData'):
            with open("requestsData/live_getMusicList.json", 'w') as f:
                f.write(json.dumps(shop_canbuy))

        url_cheat = host + 'bsea/getData/' + self.get_url_end()
        bsea_getData = json.loads(
            zlib.decompress(session.get(url=url_cheat, headers=HEADER, cookies=self.cookies, timeout=10).content))
        if is_write and os.path.exists('requestsData'):
            with open("requestsData/bsea_getData.json", 'w') as f:
                f.write(json.dumps(bsea_getData))

        url_cheat = host + 'active/getUserData' + self.get_url_end()
        active_getUserData = json.loads(
            zlib.decompress(session.get(url=url_cheat, headers=HEADER, cookies=self.cookies, timeout=10).content))
        if is_write and os.path.exists('requestsData'):
            with open("requestsData/active_getUserData.json", 'w') as f:
                f.write(json.dumps(active_getUserData))

        url_cheat = host + 'pve/getUserData/' + self.get_url_end()
        pve_getUserData = json.loads(
            zlib.decompress(session.get(url=url_cheat, headers=HEADER, cookies=self.cookies, timeout=10).content))
        if is_write and os.path.exists('requestsData'):
            with open("requestsData/pve_getUserData.json", 'w') as f:
                f.write(json.dumps(pve_getUserData))

        self.get_init_data()
        return True

    # 普通登录实现方法
    def login_usual(self, username, pwd, server):

        url_login = self.hm_login_server + "1.0/get/login/@self"
        data = {
            "platform": "0",
            "appid": "0",
            "app_server_type": "0",
            "password": pwd,
            "username": username
        }

        self.refresh_headers(url_login)

        login_response = session.post(url=url_login, data=json.dumps(data).replace(" ", ""),
                                      headers=self.pastport_headers, timeout=10).text

        login_response = json.loads(login_response)

        # print("LOGIN RESPONSE: {}".format(login_response))

        if "error" in login_response and int(login_response["error"]) != 0:
            return False

        # 字段里是否存在存在token
        tokens = ""
        if "access_token" in login_response:
            tokens = login_response["access_token"]
        if "token" in login_response:
            tokens = login_response["token"]


        url_init = self.hm_login_server + "1.0/get/initConfig/@self"
        self.refresh_headers(url_init)
        session.post(url=url_init, data="{}", headers=self.pastport_headers, timeout=10)
        time.sleep(1)

        # Validate token
        while True:
            url_info = self.hm_login_server + "1.0/get/userInfo/@self"

            login_data = json.dumps({"access_token": tokens})

            self.refresh_headers(url_info)
            user_info = session.post(url=url_info, data=login_data, headers=self.pastport_headers, timeout=10).text
            user_info = json.loads(user_info)
            if "error" in user_info and user_info["error"] != 0:
                tokens = ""
                # print("口令失效, 重新获取")
                continue
            else:
                # print("口令正确")
                break

        login_url = self.login_server + "index/hmLogin/" + tokens + self.get_url_end()
        login_response = session.get(url=login_url, headers=HEADER, timeout=10)
        login_text = json.loads(zlib.decompress(login_response.content))

        if is_write and os.path.exists('requestsData'):
            with open("requestsData/login.json", 'w') as f:
                f.write(json.dumps(login_text))
        self.cookies = login_response.cookies.get_dict()
        self.uid = str(login_text['userId'])
        return login_text

    def get_url_end(self, now_time=str(int(round(time.time() * 1000)))):
        url_time = now_time
        md5_raw = url_time + 'ade2688f1904e9fb8d2efdb61b5e398a'
        md5 = hashlib.md5(md5_raw.encode('utf-8')).hexdigest()
        url_end = '&t={time}&e={key}&gz=1&market=2&channel={channel}&version={version}'
        url_end_dict = {'time': url_time, 'key': md5, 'channel': self.channel, 'version': self.version}
        url_end = url_end.format(**url_end_dict)
        return url_end

    def encryption(self, url, method):
        times = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

        data = ""
        data += str(method)
        data += "\n"
        data += times
        data += "\n"
        data += "/" + url.split("/", 3)[-1]
        mac = hmac.new(self.key.encode(), data.encode(), hashlib.sha1)
        data = mac.digest()
        return base64.b64encode(data).decode("utf-8"), times

    def refresh_headers(self, url):
        data, times = self.encryption(url=url, method="POST")
        self.pastport_headers["Authorization"] = "HMS {}:".format(self.portHead) + data
        self.pastport_headers["Date"] = times

    def gfffff_get_init_data(self, res_url, end):
        """
        获取init数据
        :return:
        """
        print("[INFO] Getting init data...")
        user_data = zlib.decompress(session.get(url=res_url + end, headers=HEADER, timeout=30).content)
        user_data = json.loads(user_data)
        user_data["res_url"] = res_url
        user_data = json.dumps(user_data)
        return user_data



    def get_init_data(self):
        print('Getting init data...')
        if not os.path.exists('data'):
            os.mkdir('data')

        need_upgrade = True
        if os.path.exists('data/init.json'):
            init_data.read_init()
            if int(init_data.new_init_version) <= int(init_data.init_version):
                need_upgrade = False
        if init_data.res_url != self.res:
            need_upgrade = True
        if need_upgrade:
            user_data = gfffff_get_init_data(self.res, self.get_url_end())
            if not os.path.exists('data'):
                os.mkdir('data')
            with open('data/init.json', 'w') as f:
                f.write(user_data)
            init_data.read_init()
        return True

    # ============ xie de shi shen me gou shi???

    def get_login_reward(self):
        url = self.server_list[0]["host"] + 'active/getLoginAward/c3ecc6250c89e88d83832e3395efb973/' + self.fffffffffff_get_url_end()
        data=self.Mdecompress(url)
        data = json.loads(data)
        if is_write and os.path.exists('requestsData'):
            with open('requestsData/login_award.json', 'w') as f:
                f.write(json.dumps(data))
        return data

    def get_friend_list(self):
        url = self.server_list[0]["host"] + 'friend/getlist' + self.fffffffffff_get_url_end()
        raw_data = self.Mdecompress(url)
        data = json.loads(raw_data)
        return data["list"]
    
    def friend_feat(self, uid, cook_item):
        url = self.server_list[0]["host"] + 'live/feat/' + uid + '/' + cook_item + self.fffffffffff_get_url_end()
        raw_data = self.Mdecompress(url)
        data = json.loads(raw_data)
        return data

    def visit_friend_kitchen(self, uid):
        url = self.server_list[0]["host"] + 'live/friendKitchen/' + uid + self.fffffffffff_get_url_end()
        raw_data = self.Mdecompress(url)
        data = json.loads(raw_data)
        return data

    def fffffffffff_get_url_end(self):
        url_time = str(int(round(time.time() * 1000)))
        md5_raw = url_time + 'ade2688f1904e9fb8d2efdb61b5e398a'
        md5 = hashlib.md5(md5_raw.encode('utf-8')).hexdigest()
        url_end = '&t={time}&e={key}&gz=1&market=2&channel={channel}&version={version}'
        url_end_dict = {'time': url_time, 'key': md5, 'channel': self.channel, 'version': self.version}
        url_end = url_end.format(**url_end_dict)
        return url_end

    def Mdecompress(self,url,*vdata):
        if  len(vdata)==0:
            content = session.get(url=url, headers=HEADER, cookies=self.cookies, timeout=10).content
        else:
            h=HEADER
            h["Content-Type"]="application/x-www-form-urlencoded"
            content = session.post(url=url,data=str(vdata[0]), headers=h, cookies=self.cookies, timeout=10).content

        try:  # 解码统一
            data = zlib.decompress(content)
        except Exception as e:
            data = content
        return data

if __name__ == "__main__":
    MY_ACCOUNTS = {}
    with open('acc2.json', 'r') as f:
        MY_ACCOUNTS = json.load(f)

    account_num = 0
    while account_num < len(MY_ACCOUNTS):
        t = GameLogin()

        res1 = t.first_login_usual(1, MY_ACCOUNTS[account_num]["id"], MY_ACCOUNTS[account_num]["pswd"])
        res2 = t.second_login(t.server_list[0]["host"], MY_ACCOUNTS[account_num]["uid"])
        if res1 is True and res2 is True:
            print("[INFO] Successfully logged in with uid: {}".format(MY_ACCOUNTS[account_num]["uid"]))
        else:
            print("[WARNING] Skip {}".format(MY_ACCOUNTS[account_num]["id"]))
            account_num = account_num + 1
            continue

        print("[INFO] Getting login reward...")
        t.get_login_reward()

        all_friend_list = t.get_friend_list()
        print(all_friend_list)
        for friend in all_friend_list:
            k = t.visit_friend_kitchen(friend['uid'])
            print("[INFO] Kitchen popularity of target account: {}/10000".format(k['popularity']))
            if k['eatTimes'] >= 3:
                print("[ERROR] Reaches quotidian dining limit.")
                continue
            m = k['shipVO']['cookbook']             # get menu, a vector of 3 strings
            for x in range(3):                      # 3 times per day
                # TODO: in future, eat non-max menu to improve proficiency
                t.friend_feat(friend['uid'], m[0])

        account_num = account_num + 1
        print("================================================================")