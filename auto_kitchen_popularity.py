from urllib import request, parse, error
import json
import base64
import time
import random
import hashlib
import math
import zlib

class Utility(Exception):
    def __init__(self, username, password):
        self.version = "4.7.0"
        self.channel = "100014" # iOS server

        self.versionlink = "http://version.jr.moefantasy.com/" \
            "index/checkVer/" + self.version + "/" + self.channel + "/2&version=" + self.version + \
            "&channel=" + self.channel + "&market=2"

        self.HEADER = {
                'Accept-Encoding': 'identity',
                'Connection': 'Keep-Alive',
                'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; GT-P5210 Build/LMY48Z)'
        }
        self.userId = None
        self.login_url = None
        self.login_data = None
        self.login_server = None
        self.nowNode = 0
        self.working_fleet = 4
        self.get_init_data()
        self.get_login_data(username, password)
        self.fleet_info = {}
        self.defaultUrlSettings = '&gz=1&market=2&channel=100014'
        self.secretKey = 'ade2688f1904e9fb8d2efdb61b5e398a'

    def get_init_data(self):
        _data = request.urlopen(self.versionlink).read().decode()
        _data = json.loads(_data)
        self.version = _data["version"]["newVersionId"]
        self.login_url = _data["loginServer"]

    def get_login_data(self, username, password):
        username = str(username)
        password = str(password)
        _tmp = {}
        _tmp["username"] = base64.encodebytes(username.encode())
        _tmp["pwd"] = base64.encodebytes(password.encode())
        self.login_data = parse.urlencode(_tmp).encode()
        _tmp.clear()

    def login(self):
        login_url = "/index/passportLogin"
        server_url = "/index/login/{}"
        _res = request.urlopen(url=self.login_url + login_url, data=self.login_data)
        _cookie = _res.getheader("Set-Cookie")

        if "hf_skey" not in _cookie:
            print("[ERROR] Incorrect ID or Password.")
            # print(dir(_res))
            print(dir(_cookie))
            return False

        self.HEADER["Cookie"] = "{};".format(_cookie.split(";")[0])
        _data = json.loads(_res.read().decode())
        self.userId = _data["userId"]

        print("[INFO] Successfully logged in uid: {}".format(self.userId))

        # 101 - 列克星顿
        self.login_server = _data["serverList"][0]["host"]
        print("[INFO] Getting server list...")

        while int(_data["serverList"][0]["status"]) != 0:
            print("[ERROR] Servers are under maintenance.")
            time.sleep(60 * 30)
        print("[INFO] Starting login...")
        _res = self.httpget(server_url.format(self.userId))
        return _res

    def completeurl(self, url):
        ts = str(math.trunc(time.time()))
        rand = ''.join([str(random.randint(0, 9)) for __i in range(3)])
        checksum = hashlib.md5((ts + rand + self.secretKey).encode('utf-8')).hexdigest()
        return url + '&t=' + ts + rand + '&e=' + checksum + self.defaultUrlSettings + '&version=' + self.version

    def httpget(self, url, *, data=None, header=False, timeout=0, host=None):
        """
        :param url: 不包括http://host，host由可定参数host决定
        :param data: 要发送的数据，需要先编码为byte格式
        :param header: 影响返回数据
        :param timeout: 延迟
        :param host: 如果没指定这个参数，则默认host为server，否则为所给host
        :return: 如果header没指定值，那么返回请求后content，否则，返回：http报头，content
        """
        url = self.completeurl(url)
        # debug_print(url)
        time.sleep(timeout)

        if host is None:
            url = self.login_server + url
        else:
            url = host + url

        if data is None:
            _req = request.Request(url=url, headers=self.HEADER)
        else:
            _req = request.Request(url=url, headers=self.HEADER, data=data)

        _res = request.urlopen(_req)

        if header is False:
            try:
                return zlib.decompress(_res.read()).decode()
            except zlib.error:
                return _res.read().decode()

        return _res.getheader(header), _res.read().decode()

    def get_user_info(self):
        url = "/bsea/getData/"
        _res = self.httpget(url)
        # debug_print(_res)
        return _res

    def data(self):
        _url = "/api/initGame"
        _res = self.httpget(_url)
        return _res

    def test(self):
        _url = "/boat/getUserData/"
        _res = self.httpget(_url)
        debug_print(_res)

    def retry(self, target, *args):
        while True:
            _tmp = target(*args)
            if _tmp is None:
                continue
            _res = json.loads(_tmp)
            try:
                if _res["eid"] == -103:
                    # 操作过快
                    time.sleep(2)
                    continue
                elif _res["eid"] == -9999:
                    # 全服维护
                    time.sleep(10 * 60)
                    continue
                elif _res["eid"] == -101:
                    # 战斗跳转地图时，表示是待机点
                    return
                elif _res["eid"] == -408:
                    # 舰队中有船没补给了
                    self.supply(self.working_fleet)
                elif _res["eid"] == -215:
                    # 船舱满了
                    self.house_full(1)
                elif _res["eid"] == -407:
                    # 队伍中有大破船只
                    self.instance_repair(self.check_broken(fleet=self.working_fleet))
                else:
                    print("unknown error: {0} in {1}".format(_res["eid"], target.__name__))
                    raise LookupError
            except KeyError:
                return _res
            except error.URLError:
                print("Network error,waiting for recovery")
                time.sleep(10 * 60)

    def get_friend_list(self):
        _url = '/friend/getlist'
        _raw_res = self.httpget(_url)
        _res = json.loads(_raw_res)
        return _res["list"]

    def visit_friend(self, uid):
        # friend/visitorFriend/{uid}/
        _url = '/friend/visitorFriend/' + uid
        _raw_res = self.httpget(_url)
        _res = json.loads(_raw_res)
        return _res

    def visit_friend_kitchen(self, uid):
        _url = '/live/friendKitchen/' + uid
        _raw_res = self.httpget(_url)
        _res = json.loads(_raw_res)
        return _res

    def friend_feat(self, uid, cook_item):
        _url = '/live/feat/' + uid + '/' + cook_item
        _raw_res = self.httpget(_url)
        _res = json.loads(_raw_res)
        return _res

    def get_login_reward(self):
        
        _url = 'active/getLoginAward/c3ecc6250c89e88d83832e3395efb973/'
        _raw_res = self.httpget(_url)
        _res = json.loads(_raw_res)     # eid -1206 = already got login reward
        return _res


if __name__ == "__main__":
    MY_ACCOUNTS = {}
    with open('acc.json', 'r') as f:
        MY_ACCOUNTS = json.load(f)

    account_num = 0
    while account_num < len(MY_ACCOUNTS):
        t = Utility(MY_ACCOUNTS[account_num]["id"], MY_ACCOUNTS[account_num]["pswd"])
        if t.login() is False:
            print("[WARNING] Skip {}".format(MY_ACCOUNTS[account_num]["id"]))
            account_num = account_num + 1
            continue

        print("[INFO] Getting login reward...")
        print(t.get_login_reward())

        all_friend_list = t.get_friend_list()
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