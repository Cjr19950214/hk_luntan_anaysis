'''
2019.12.11
lihkg
https://lihkg.com/thread/1772206/page/1
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
        self.path = r'D:\爬虫\liandeng\data1740000_1750000'
        # ---------------------------------------------
        # 1100000-1800000

        # origin表示起始id
        self.origin = 1748955
        # destination表示终止id
        self.destination = 1750000  #1800000
        # ---------------------------------------------

        self.flag = 0
        self.url = 'https://lihkg.com/api_v2/thread/category?cat_id=5&page=3&count=60&type=now'
        self.pru = 'https://lihkg.com/api_v2/thread/{}/page/{}?order=reply_time'

    def run(self):
        strat = time.time()
        try:
            for nid in range(self.origin, self.destination):
                self.nid = nid
                for text, index in self.get_page(urlid=nid):
                    if text:
                        item = self.parse_page(text, index=index)
                        if index == 1:
                            if len(item[2]) > 0 and len(item) / 4 > 15:
                                print('{}.csv'.format(nid), end=' ')
                                self.save_data(name=nid, item=item)
                                self.flag += 1
                                print('当前已经保存{}个帖子'.format(self.flag))
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
        for index in range(1, 50):
            url = self.pru.format(urlid, index)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
                'referer': 'https://lihkg.com/thread/1772206/page/1',
            }
            print('url is ', url)
            try:
                r = requests.get(url, headers=headers)
            except:
                time.sleep(10)
                r = requests.get(url, headers=headers)
            r.encoding = 'utf-8'

            if not self.json_is_valid(response=r):
                break
            yield r.json(), index
        yield None, None

    def json_is_valid(self, response):
        if int(response.json().get('success')) == 0:
            print(response.json().get('success'))
            return False
        if int(response.json().get('response').get('category').get('cat_id')) != 5:
            print(response.json().get('response').get('category'))
            return False
        if (len(response.json().get('response').get('item_data'))) == 0:
            return False
        return True

    def parse_page(self, text, index):
        if index == 1:
            authorName = text.get('response').get('user_nickname')
            content = ' '.join(i.strip().replace('\n', ' ') for i in
                               etree.HTML(text.get('response').get('item_data')[0].get('msg')).xpath('//text()'))
            messageDate = time.ctime(
                int(text.get('response').get('create_time')))
            marksGood = text.get('response').get('reply_like_count')

            item = [authorName, messageDate, content, marksGood]

            for repley in text.get('response').get('item_data')[1:]:
                item.append(repley.get('user_nickname'))
                item.append(time.ctime(int(repley.get('reply_time'))))
                item.append(
                    ' '.join(i.strip().replace('\n', ' ') for i in etree.HTML(repley.get('msg')).xpath('//text()')))

                item.append(repley.get('like_count'))

            return item

        else:
            item = []
            for repley in text.get('response').get('item_data'):
                item.append(repley.get('user_nickname'))
                item.append(time.ctime(int(repley.get('reply_time'))))
                item.append(
                    ' '.join(i.strip().replace('\n', ' ') for i in etree.HTML(repley.get('msg')).xpath('//text()')))
                item.append(repley.get('like_count'))
            return item

    def save_data(self, name, item):
        '''
        保存文件
        '''
        with open('{}/{}.csv'.format(self.path, name), 'a', encoding='utf_8_sig', newline='') as csvfile:
            print('item >>> ')
            writer = csv.writer(csvfile)
            for i in range(int(len(item) / 4)):
                print(item[4 * i:4 * i + 4])
                writer.writerow(item[4 * i:4 * i + 4])

    @property
    def time(self):
        return '总共用时：{}秒'.format(self.runtime)


if __name__ == '__main__':
    spider = Spider()
    spider.run()
    print(spider.time)  # 运行总时间
