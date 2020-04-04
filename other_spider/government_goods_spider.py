# 爬取政府采购网钢制家具，木制家具的商品信息
import requests
import json
from lxml import etree

class GoodSpider():
	"""政府采购网的商品爬虫"""
	def __init__(self, name):
		self.start_url = "http://219.159.250.238:3333/GoodsShowControllerExt.do?method=toGoodsList&rp=20&page=1&goodsClassCode=D01"
		self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"}
		self.name = name

	def send_request(self,next_url):
		"""发送请求，获取响应"""
		response = requests.get(next_url,headers=self.headers)
		return response.content.decode()

	def handle_response(self,ret_response):
		"""处理数据"""
		html_response = etree.HTML(ret_response)
		goods_li = html_response.xpath("//li[@id='list-item-d']")
		goods_detail = []
		for item in goods_li:
			items = {}
			items["name"] = item.xpath("./div[not(@class)]/a/text()")[0] if len(item.xpath("./div[not(@class)]/a/text()"))>0 else None
			items["price"] = item.xpath(".//em[@id='priced']/text()")[0] if len(item.xpath(".//em[@id='priced']/text()"))>0 else None
			items["img_url"] = item.xpath(".//img/@src")[0] if len(item.xpath(".//img/@src"))>0 else None
			goods_detail.append(items)
		return goods_detail

	def save_goods(self,goods_dict):
		"""保存商品信息字典"""
		file_name = 'D:\\习\\EduDo\\spider\\'+self.name+'.txt'
		with open(file_name,'a',encoding='utf-8') as f:
			for good_dict in goods_dict:
				f.write(json.dumps(good_dict,ensure_ascii=False,indent=2))
				# f.write("\n")
		print('保存成功')

	"""爬虫步骤"""
	def run(self):
		next_url = self.start_url
		# 发送首个链接请求，获取响应
		ret_response = self.send_request(next_url)
		# 处理数据，并获取下一个url地址
		goods_dict = self.handle_response(ret_response)
		# 保存数据
		# print(goods_dict,len(goods_dict))
		self.save_goods(goods_dict)
		# 对下一个url地址发送请求，获取响应


def main():
	print('haihaihai...')


if __name__ == '__main__':
	# r = GoodSpider("钢制家具")
	# r.run()
	main()
