import requests
import os, time
import json
import re
from lxml import etree
from multiprocessing import Process


class meitulu_spider():
    """img for meitulu_spider"""

    def __init__(self, name):
        self.start_url = "http://www.meitulu.cn/t/" + name
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
        self.name = name

    def send_request(self, next_url):
        meitu_response = requests.get(next_url, headers=self.headers)
        return meitu_response.content

    def first_prase(self, meitu_response):
        """响应转化成element对象，进行xpath解析，提取每个图集link & 图片数 & 模特名 & 图集标签"""
        meitu_html = etree.HTML(meitu_response)
        total_item_num = meitu_html.xpath("//div[@id='pages']/a[1]/text()")[0] if len(
            meitu_html.xpath("//div[@id='pages']/a[1]/text()")) > 0 else 0
        if total_item_num != 0:
            total_item_num = re.match(r'\d+', total_item_num, re.S).group()
        meitu_img_array = meitu_html.xpath("//div[@class='boxs']/ul/li") if len(
            meitu_html.xpath("//div[@class='boxs']/ul/li")) > 0 else None
        page_num = len(meitu_img_array)
        # 遍历组别，提取组别详情信息，以字典形式按组别存入列表中
        meitu_img_list = []
        for item in meitu_img_array:
            meitu_item = {}
            meitu_item["detail_url"] = item.xpath("./a[1]/@href")[0] if len(item.xpath("./a[1]/@href")) > 0 else None
            meitu_item["pcs"] = item.xpath("./p[1]/text()")[0] if len(item.xpath("./p[1]/text()")) > 0 else None
            meitu_item["model"] = item.xpath("./p[3]/a/text()")[0] if len(item.xpath("./p[3]/a/text()")) > 0 else None
            meitu_item["tag"] = item.xpath("./p[4]/a/text()")[0] if len(item.xpath("./p[4]/a/text()")) > 0 else None
            meitu_img_list.append(meitu_item)
        # 获取 next_url 信息
        next_url = meitu_html.xpath("//div[@id='pages']/a[text()='下一页']/@href")[0] if len(
            meitu_html.xpath("//div[@id='pages']/a[text()='下一页']/@href")) > 0 else None
        page_count = meitu_html.xpath("//div[@id='pages']/span/text()")[0] if len(
            meitu_html.xpath("//div[@id='pages']/span/text()")) > 0 else 0
        # print(next_url)
        return meitu_img_list, next_url, total_item_num, page_num, page_count

    def prase_response(self, meitu_response):
        """除第一页外的url 的提取数据方法"""
        meitu_img_list, next_url, total_item_num, page_num, page_count = self.first_prase(meitu_response)
        return meitu_img_list, next_url, page_count

    def save_text(self, meitu_img_list):
        """保存提取出的json类型数据"""
        # tt = str(time.time()).split(".")[1]
        try:
            os.mkdir("D:\\习\\EduDo\\spider\\" + self.name + "\\")
        except:
            pass
        save_path = "D:\\习\\EduDo\\spider\\" + self.name + "\\" + self.name + ".txt"
        with open(save_path, 'a', encoding='utf-8') as f:
            for item in meitu_img_list:
                f.write(json.dumps(item, ensure_ascii=False, indent=2))
                f.write('\n')
        print('保存成功：%s' % save_path)

    def prase_img_response(self, response):
        """提取img_url信息，并得到详情页的下一页url"""
        detail_html = etree.HTML(response)
        want_img_url = detail_html.xpath("//div[@class='content']//img/@src") if len(
            detail_html.xpath("//div[@class='content']//img/@src")) > 0 else None
        want_next_url = detail_html.xpath("//div[@id='pages']/a[last()]/@href")[0] if len(
            detail_html.xpath("//div[@id='pages']/a[last()]/@href")) > 0 else None
        try:
            want_next_url = "https://www.meitulu.com" + want_next_url
        except:
            pass
        compare_num = detail_html.xpath("//div[@id='pages']/span/text()")[0] if len(
            detail_html.xpath("//div[@id='pages']/span/text()")) > 0 else 0
        temp_num = re.match(r".*?/\d+_(\d+)\.html", want_next_url, re.S).group(1)
        if compare_num == temp_num:
            return want_img_url, 0, compare_num
        return want_img_url, want_next_url, compare_num

    def save_img(self, img_response, file_name, tt, compare_num, count):
        """保存提取出的img_url数据"""
        if os.path.exists(file_name + tt + "\\"):
            save_path = file_name + tt + "\\" + str(compare_num) + "_" + str(count) + ".jpg"
        else:
            save_path = file_name.strip() + "\\" + str(compare_num) + "_" + str(count) + ".jpg"
        with open(save_path, 'wb') as f:
            f.write(img_response)
        print('保存成功：%s' % save_path)

    def run(self, save_path):
        # 第一次请求，并获取next_url地址 & total_num & page_num
        meitu_response = self.send_request(self.start_url).decode()
        meitu_img_list, next_url, total_item_num, page_num, page_count = self.first_prase(meitu_response)
        # self.save_text(meitu_img_list)
        if page_count == 0:
            for i in meitu_img_list:
                # 对详情页发送请求
                want_next_url = i["detail_url"]
                model = i["model"]
                tt = str(time.time()).split(".")[1]
                file_name = os.path.join(save_path, self.name, str(model))
                try:
                    os.mkdir(file_name)
                except:
                    os.makedirs(os.path.join(file_name + tt))
                while want_next_url:
                    detail_response = self.send_request(want_next_url).decode()
                    want_img_url, want_next_url, compare_num = self.prase_img_response(detail_response)
                    count = 1
                    for j in want_img_url:
                        img_response = self.send_request(j)
                        self.save_img(img_response, file_name, tt, compare_num, count)
                        count += 1
        while int(total_item_num) > int(page_num) * (int(page_count) + 1):
            # 发送请求，获取响应
            # print(total_item_num,page_num,page_count)
            meitu_response = self.send_request(next_url).decode()
            # 提取数据
            meitu_img_list, next_url, page_count = self.prase_response(meitu_response)
            for i in meitu_img_list:
                # 对详情页发送请求
                want_next_url = i["detail_url"]
                model = i["model"]
                tt = str(time.time()).split(".")[1]
                file_name = os.path.join(save_path, self.name, str(model))
                try:
                    os.mkdir(file_name)
                except:
                    os.makedirs(os.path.join(file_name+tt))
                while want_next_url:
                    detail_response = self.send_request(want_next_url).decode()
                    want_img_url, want_next_url, compare_num = self.prase_img_response(detail_response)
                    count = 1
                    for j in want_img_url:
                        img_response = self.send_request(j)
                        self.save_img(img_response, file_name, tt, compare_num, count)
                        count += 1
            # 保存
            # self.save_text(meitu_img_list)


if __name__ == '__main__':
    index_url = input('你想要爬取的项目：')
    meitu = meitulu_spider(index_url)
    save_path = input('你想要保存的路径：')
    meitu.run(save_path)
