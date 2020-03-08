'''
2019.12.11
高登
https://forum.hkgolden.com/channel/CA
https://api.hkgolden.com/v1/topics/CA/3?thumb=Y&sort=1&sensormode=Y&filtermodeS=N&hideblock=N&limit=1
'''

import requests
import csv
import time
from itertools import count
from lxml import etree


class LoopOver(BaseException):
    def __init__(self):
        super().__init__()


class Spider:
    def __init__(self):
        # 路径
        # .(一个点)表示当前
        # 绝对路径请用如下格式(反斜杠)
        # C:/Program Files (x86)/Dev-Cpp
        # D:/360MoveData/Users/yjc/Documents
        self.path = r'D:\爬虫\gaodeng\data7130000_7141782'
        # ---------------------------------------------
        # 700000,7140000

        # origin表示起始id
        self.origin = 7136226
        # destination表示终止id
        self.destination = 7141782
        # ---------------------------------------------
        self.csvfilenamegbk = ''
        self.csvfilename = 'datas.csv'
        self.flag = 0
        self.url = 'https://api.hkgolden.com/v1/topics/CA/3?thumb=Y&sort=1&sensormode=Y&filtermodeS=N&hideblock=N&limit=1'
        self.pru = 'https://api.hkgolden.com/v1/view/{}/{}?sensormode=Y&hideblock=N'
                  # https://forum.hkgolden.com/thread/7184350/page/1
        

    def run(self):
        strat = time.time()

        try:
            for nid in range(self.origin,self.destination):
                self.nid=nid
                for text, index in self.get_page(urlid=nid):
                    if text:
                        item = self.parse_page(text, index=index)
                        if index == 1:
                            if len(item[2]) > 0 and (len(item) - 4) / 3 > 15:
                                self.save_data(
                                    name=nid, item=item, index=1)
                                self.flag += 1
                            else:
                                break
                        else:
                            self.save_data(name=nid, item=item)
                time.sleep(1)
        except LoopOver:
            print('已经保存{}个帖子，爬取结束!'.format(self.flag))
        finally:
            nt = time.asctime()
            with open('error.log', 'a', encoding='utf-8') as f:
                f.write(str(self.nid)+' '+str(nt)+'\n')
            print(nt)
            end = time.time()
            self.runtime = end - strat
            print('总共用时{}分钟'.format(self.runtime/60))

        end = time.time()

        self.runtime = end - strat

    def get_page(self, urlid):
        for index in range(1, self.destination+1):
            url = self.pru.format(urlid, index)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
            }
            print('url is ', url)
            r = requests.get(url, headers=headers)
            if not self.json_is_valid(response=r):
                break
            yield r.json(), index
        yield None, None

    def json_is_valid(self, response):
        if not response.json().get('result'):
            print(response.json())
            return False
        if (len(response.json().get('data').get('replies'))) == 0 :
            return False
        if response.json().get('data').get('forum') != 'CA' :
            print(response.json().get('data').get('forum'))
            return False
        return True

    def parse_page(self, text, index):
        if index == 1:
            authorName = text.get('data').get('authorName')

            messageDate = time.ctime(
                int(text.get('data').get('messageDate')) / 1000)
            content = '  '.join(etree.HTML(
                text.get('data').get('content')).xpath('//text()'))
            marksGood = text.get('data').get('marksGood')

            item = [authorName, messageDate, content, marksGood]
        else:
            item = []

        for repley in text.get('data').get('replies'):
            item.append(repley.get('authorName'))
            item.append(time.ctime(int(repley.get('replyDate')) / 1000))
            item.append('  '.join(etree.HTML(
                repley.get('content')).xpath('//text()')))

        return item

    def save_data(self, name, item, index=None):
        '''
        保存文件
        '''
        with open('{}/{}.csv'.format(self.path, name), 'a', encoding='utf_8_sig', newline='') as csvfile:
            print('item >>> ', item)
            writer = csv.writer(csvfile)
            if index:
                writer.writerow(item[:4])
                for i in range(int((len(item) - 4) / 3)):
                    writer.writerow(item[4 + 3 * i:4 + 3 * (i + 1)])
            else:
                for i in range(int((len(item)) / 3)):
                    writer.writerow(item[3 * i:3 * (i + 1)])

    @property
    def time(self):
        return '总共用时：{}秒'.format(self.runtime)


if __name__ == '__main__':
    spider = Spider()
    spider.run()
    print(spider.time)  # 运行总时间

    # get_doc()
