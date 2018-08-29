import requests
import re
from PIL import Image


def read_url(url):
    """
    2018.8.15 
    从微信的文章链接读取封面图片
    :param url: 传入的链接
    :return: 封面图片的url
    """
    print("Extrating URL")

    response = requests.get(url)
    html = response.text

    # re.S可以令正则中的.匹配包括换行符在内的任意符号
    pic = re.match('^.*?var msg_title = "(.*?)".*?var msg_cdn_url = "(\S*?)".*?$', html, re.S)
    title = pic.group(1)
    pic_url = pic.group(2)
    return title, pic_url


def pic_download(url, name):
    """
    下载链接的图片
    :param url: 图片url
    :return: 
    """
    print("Downloading picture")
    pic = requests.get(url)
    pic_name = str(name) + '.png'
    pic_path = 'pics/' + pic_name
    with open(pic_path,'wb') as file:
        file.write(pic.content)


def into_square(name):
    """
    对图片进行裁剪，使其为正方形
    :param name: 图片的名称
    :return: 
    """
    pic_name = str(name) + '.png'
    pic_path = 'pics/' + pic_name
    with Image.open(pic_path) as pic:
        size = pic.size     # 返回变量为一个元组(长,宽)
        # print(size)
        x = (size[0]-size[1]) / 2
        y = 0
        w = size[1]
        h = size[1]
        square = pic.crop((x,y,x+w,y+h))
        square.save(pic_path)


# def get_info(url):
#     """
#     从链接中获取文章的信息，并对信息进行处理
#     主要是提取出封面图并裁剪为正方形，提取出文章标题并对标题进行部分省略
#     :param url:
#     :return:
#     """
#     title, pic_url = read_url(url)
#     pic_download(pic_url, title)
#     into_square(title)


if __name__ == '__main__':
    url = "www.baidu.com"
    read_url(url)