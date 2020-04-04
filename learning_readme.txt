爬虫字符串提取 日常工作之一

字符：是各类文字和符号的总称，包含国家文字，标点符号，图形编号，数字等
字符集：是多个字符的集合
字符集包含：ASCII字符集、GB2312字符集、GB18030、Unicode字符集等

ASCII码1个字节为单位，unicode一般2个字节为单位，UTF-8是unicode的实现方式之一，变化的一种编码方式，根据存储内容可以是1，2，3个字节，汉字一般为3个字节

1.1. 字符串类型区别和转化
分为string（unicode呈现） 和 bytes类型（互联网中数据都是以二进制的方式传输的）

1.2. str 转化成 bytes类型需要 编码encode
反之 需要解码decode，什么编码就需要什么解码，否则会出现乱码

2.1 HTTP和HTTPS 请求
目的：为了更好的发送请求，模拟浏览器发送请求
HTTP：超文本传输协议，默认端口号 80
HTTPS：HTTP + SSL(安全套接字层)，默认端口号 443。 发送数据前会进行加密，接受请求后，解密再进行业务处理
后者更安全，但是性能更低

3.1 url地址 形式
scheme：协议
host：服务器的IP地址 或是 域名
port：服务器的端口
path：访问资源的路径
query-string：参数，发送给 http 服务器的数据
anchor：锚（跳转到网页的指定锚点位置）#xxx
例：http://localhost:4000/file/part01/1.2.html

4.1 HTTP请求形式
请求行：请求方式 空格 URL 空格 协议/版本
请求头部：包含一系列字段（host，connection，user-agent，accept，accept-encoding，accept-language，cookie）等等
请求数据：

5.1 Robots 协议
服务器根目录下，存在robots.txt文件，告诉搜索引擎服务器哪些网页可以抓取，哪些不能抓取

6.1 request and response
爬虫要根据当前url地址对应的响应为准，当前url地址的elements的内容和url的响应不一样
其中页面中的数据在哪里：
1)当前url地址对应的响应中
2)其他的url地址对应的响应中，比如ajax请求中
3)js生成的：部分数据在响应中，或是全部由js生成
注意：浏览器渲染出的数据，和爬虫请求的页面数据不一样，前者经过浏览器APP的再请求，js生成等得到的数据



爬虫requests库：
7.1 发送带headers & 带参数的请求
url = "www.baidu.com/s?"
字典形式 headers = {'User-Agent':'....'}
字典形式 args = {'kw':'骚男'}
响应 response = requests.get(url,headers=headers,params=args)
画外音：字符串格式化的另一种方式 -- '传{}播客'.format(1) ==> '传1播客'

面向对象 编写代码：
class xx：
	def __init__(self):
		pass
	def get_url(self):
		pass
		return
	def prase_url(self):
		pass
		return
	def run(self):
		get_url()
		prase_url()

7.2 发送post请求：表单请求，传输大文件内容时需要post请求
post请求参数字典类型 data = {}
响应 response = requests.post(url,headers=headers,data=data)

7.3 使用代理：前提是检查代理的可用性
知道最终服务器的地址，期间使用的代理为正向代理
不知道，则使用的反向代理，例如客户端访问 => nginx => django服务器
响应 response = requests.get(url,proxies=proxies)

7.3.1 创建一个固定数量的 代理ip池，使用时随机调用即可
调用过程中避免随机到某几个ip重复使用，进行调用次数统计，尽可能调用使用次数低的代理ip
调用前对代理ip进行校验：超时校验，代理ip网站的校验

7.4 session 与 cookie的区别：
session存储在服务器中，较为安全，无上限
cookie存储在客户端中，较不安全，有上限
7.4.1 爬虫请求时带上session cookie的利弊：
利：能够请求到登陆之后的页面
弊：一套cookie只能与一个用户对应，请求太快，太多，会被服务器认为是爬虫
7.4.2 携带cookie 发送请求
准备一定量的cookie，组成cookie池发送请求

7.5 requests模拟登陆的三种方式
1）requests中存在一个session类，实例化后，具备requests的所有方法，这时再次请求时，会携带之前登陆成功的cookie信息
2）headers中添加cookie键，值为cookie字符串
3）在请求方法中添加cookies参数，接收字典类型的cookie，键是name对应的值，值是value对应的值。（其中涉及到字典推导式，需要使用split分段函数）

7.6 为什么使用requests库，而不是urllib
1）requests库底层实现就是urllib
2）requests在python2/3 中方法完全一样
3）requests简单易用
4）Requests能够自动解压（gzip压缩等）网页内容

7.7 响应解码
response.text：返回str类型，解码类型是更具HTTP头部对响应编码做出有根据的推测，推测的文本编码
	修改解码方式：response.encoding = 'gbk'
response.content：返回bytes类型，解码类型没有指定
	定义解码方式：response.content.decode() 默认为utf-8

7.8 requests小技巧
1）requests.utils.dict_from_cookiejar 把cookie对象转化成字典
反之字典也可以转化成cookie格式数据：requests.utils.cookiejar_from_dict
2）requests.utils.unquote("已经编码的url") => 解码成 原始 url
反之亦然 requests.utils.quote("原始 url") => 编码 url（即转化特殊字符，包含各国文字，标点符号等）
3）请求SSL证书验证错误时：response = requests.get(url, verify=False)
4）设置超时：response = requests.get(url,timeout=10)
5）配合状态码判断是否请求成功：assert response.status_code == 200
注：很多情况下，都会存在发送请求，获取响应的步骤，因而可以封装这样的python包，下次使用前，导入直接调用即可

获取响应后，解析提取数据
分为：基础知识，Json知识点复习，正则表达式的复习，xpath和lxml
8 数据分类
结构化数据：Json，xml 传化成python数据类型，典型是json.loads()
非结构化数据：html 正则表达式、xpath进行数据处理

9.1 处理 Json数据类型
能找到返回Json数据的URL，尽量使用这类URL，处理这类的响应会方便很多
Json是一种轻量级的数据交换格式，更易阅读和编写，适用于数据交互场景
寻找返回Json的URL的方法：1）使用chrome浏览器，切换到手机模式浏览  2）抓包手机app的软件

9.2 json模块
1）json.loads(Jsonresponse.content)：json字符串转化成python数据类型
2）json.dumps()：python数据类型转化成json字符串（其中包含功能选项）
3）json.load()：提取类文件对象中的数据，例：with open('a.json','r',encoding='utf-8') as f: \r\n ret = json.load(f)
4）json.dump()：能够把python类型放入类文件对象中

10 正则表达式处理 html/xml 数据
正则的定义：
定义好一些特殊字符，及这些字符的组合，组成一个"规则字符串"，通过这个规则字符串用来表达对字符串的一种过滤逻辑。
常用方法：
re.compile(编译)
pattern.match(从头开始匹配)
pattern.search(找第一个符合规则的结果)
pattern.findall(找所有符合规则的结果)
pattern.sub(将找到的结果，自定义替换)
注：re.S(可以使 . 能匹配到换行符)，r"a\nb"(表达原始字符串，即len个数为4，忽略转义符转义后的效果) 

11.1 xpath 处理数据
xPath 在chrome 或是Firebox 浏览器中都有对应的功能插件
专门使用路径表达式 来选取XML 文档中的节点或是节点集

11.2 xpath方法(以a标签为例)
1）获取标签中的文本：a/text() 获取a标签下所有的文本：a//text()
2）获取标签中的属性：a/@href
3）获取限定条件的标签内容：//ul[@id='limit']/li
4）// 符的应用：在xpath开始的时候表示当前html中任意位置开始选择
5）节点选择语法：
/book[1] 第一个符合的节点
/book[last()] 最后一个符合的节点
/book[position>3] 前三个符合的节点
/book[contains(@class,'i')]  选取所有class包含i的book标签
通配符选择未知节点 * @*
逻辑或 | 

11.3 代码中使用xpath获取节点
使用第三方库 lxml.etree
etree.HTML(text)会将response内容转化成html的element对象，这类对象有xpath方法

11.4 lxml库使用
lxml会自动修正HTML代码，但有时可能会改错
一般使用etree.tostring 观察修改后的html代码后，再进行xpath编写

11.5 获取页面数据思路
先进行分组，避免节点间数据串线：
1）分组，xpath取到一个包含分组的标签列表
2）对element列表遍历，取其中一元素数据，不会影响其他元素数据内容

12 selenium（web自动化测试工具） 和 phantomjs（headless）driver
12.1 某网站登陆账户需要验证码识别输入，可以解除selenium 完成
方法：
1）url 不变，验证码 也不变时：
请求验证码地址，存入本地，或是直接将二进制的response相应，传入云打码(第三方解码平台)API，获取相应的识别码
2）url 不变，验证码 变化时：
思路1：对方服务器返回验证码时，会将验证码信息和每个用户的信息（非cookie）进行一个对应，之后在用户post发送登陆请求时，会校验用户信息及对应的验证码信息，均相同时才能通过验证完成登陆
实行：实例化requests.session类，使用session类请求登陆页面，获取验证码地址，session发送验证码请求，获取验证码response后，交由云打码 平台进行解析，后再在登陆页面输入解析验证码后，完成登陆
思路2：利用第三方库 PIL，即python中的ps库，可以对图像进行一系列的操作
此间，利用 PIL 在设置固定大小的 selenium driver界面中进行验证码 区域的定向截图，存入本地，再转交给 云打码解析

12.2 selenium使用注意点：
1）获取元素文本和属性：先定位到元素，后.text & .get_attribute 方法获取，因为定位方法find_elemnet_by_id/class等，返回的对象都是webelement(object text)对象，而非一个element元素
2）find_elemnet 和 find_elemnets 返回对象的区别：前者返回webelement 对象，后者返回列表
3）iframe、frame：若包含前两者标签，表示该标签中的内容与当前网页属于两个网页，嵌套在当前网页而已，需要将selenium 实例化的一个driver类进行一个转化，driver.	switch_to.frame("id or name[iframe 标签]")后才能定位元素
4）selenium请求第一页时，会等数据加载完后进行元素定位，但是操作点击下一页时，不会等下一页数据加载完才会进行后续代码的定位，而是会直接进行查找定位，这事需要time.sleep一段时间后再进行后续的元素查找定位

13 Tesseract
Tesseract 是一个将图像翻译成文字的OCR库（光学文字识别）