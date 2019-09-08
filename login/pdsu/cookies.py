import requests
from lxml import etree

PROXY_POOL_URL = 'http://localhost:5555/random'
class Login(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Host': 'jiaowu.pdsu.edu.cn',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q = 0.8',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Cache-Control': 'private',
            'Content-Length': '24780',
            'Content-Type': 'text/html;charset=gb2312',
            'Server': 'Microsoft - IIS / 7.5',
            'X-AspNet-Version': '4.0.30319X - Powered - By: ASP.NET',
            'Referer': 'http://jiaowu.pdsu.edu.cn/'
        }
        self.login_url = 'http://jiaowu.pdsu.edu.cn/'
        self.post_url = 'http://jiaowu.pdsu.edu.cn/_data/login.aspx'
        self.logined_url = 'http://jiaowu.pdsu.edu.cn/MAINFRM.aspx'
        self.session = requests.Session()

    def get_proxy(self):
        try:
            response = requests.get(PROXY_POOL_URL)
            if response.status_code == 200:
                return response.text
            return None
        except ConnectionError:
            return None

    def token(self):
        proxie = self.get_proxy()
        proxies = {
            'http': 'http://' + proxie,
            'https': 'https://' + proxie
        }
        print(proxies)
        res = self.session.get(self.login_url, headers=self.headers, proxies=proxies,timeout= 10)
        print(res.text(encode="utf-8"))
        response = self.session.post(self.post_url, headers=self.headers, proxies=proxies,timeout= 10)
        print(response.text(encode="utf-8"))
        selector = etree.HTML(response.text)
        token = selector.xpath('//*[@id="dsdsdsdsdxcxdfgfg"]/@value')
        return token



    def login(self,stunum,password):
        post_data = {
        '__VIEWSTATE': '/wEPDwULLTIwMzgxMTQzODdkZGAmwRygrt4Qcb1Hzxd2 / qU6uVmT4y0hbVxN8T + RfPNZ',
        '__VIEWSTATEGENERATOR': 'A3147466',
        '__EVENTVALIDATION': '/wEdAAID77BUh0NNvoO8nwozRmoOZ5IuKWa4Qm28BhxLxh2oFCJugR + k627i4gnn4iaV6pCTeVIk / n4o + qRt0SkhLVg9',
        'pcInfo': 'Mozilla / 5.0(WindowsNT10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 53.0.2785.89Safari / 537.36undefined5.0(WindowsNT10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 53.0.2785.89Safari / 537.36SN: NULL',
        'dsdsdsdsdxcxdfgfg': self.token(),
        'Sel_Type':'STU',
        'txt_asmcdefsddsd': stunum,
        'txt_pewerwedsdfsdff':password
        }
        response = self.session.post(self.post_url,data=post_data,headers=self.headers)
        if response.status_code == 200:
            print("登陆成功",response.text(encode="utf-8"))


        response = self.session.get(self.logined_url,headers=self.headers)
        if response.status_code ==200:
            print("首页",response.text)

    def main(self):
        try:
            self.login(stunum=161360132,password='qwertyuiop')
        except:
            self.main()


if __name__ == "__main__":
    login = Login()
    login.main()