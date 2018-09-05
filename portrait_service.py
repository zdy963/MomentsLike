from PIL import Image
import requests


def thumbnail(name):
    """
    图像压缩，保存为同一个名字的文件
    压缩后，图片的分辨率为70*70
    :param name: 图片名
    :return: 
    """
    print("---------Thumbnailing---------")
    img = Image.open('pics/portrait/%s.jpg' % name)
    x,y = img.size
    if x > 70 or y > 70:
        print('Compressing')
        img.thumbnail((70,70))
        img.save('pics/portrait/%s.jpg' % name)
        print("---------Thumbnailing as %s.jpg---------" % name)


def download_portrait(url,uid):
    """
    下载用户的头像，并保存至u+uid.png
    :param url: 用户头像的url
    :param uid: 用户ID
    :return: 
    """
    pic = requests.get(url,stream=True)
    print("---------Downloading portrait---------")
    with open('pics/portrait/u%s.jpg' % uid, 'wb') as img:
        for chunk in pic.iter_content():
            img.write(chunk)
    name = 'u%s' % uid
    print("---------Successed! Portrait name is %s.jpg---------" % name)
    thumbnail(name)


if __name__ == '__main__':
    # url = 'http://ww1.sinaimg.cn/large/4399c9a5gy1fiacj5micyj21zm10213z.jpg'
    # download_portrait(url,12)
    thumbnail('default')