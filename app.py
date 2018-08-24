from flask import Flask,request, Response
from PIL import Image
from get_info import read_url,pic_download,into_square
from pics_joint import cover_pic, paste_title,likes,username,combine_pics,userhead

app = Flask(__name__)


@app.route('/')
def test():
    return 'This is Momens Like Program'


@app.route('/url',methods=['GET'])
def get_url():
    """
    对链接的内容进行提取
    :return: 
    """
    mode = request.args.get('mode')
    likenum = int(request.args.get('num'))
    if not mode:   # testing mode
        url = 'https://mp.weixin.qq.com/s/g-xI1RkU7UUC8pQsDCZD_A'
        usrhead = '0'
        usrname = '葛蒙蒙'
    else:             # regular mode
        url = request.args.get('url')
        usrhead = request.args.get('head')
        usrname = request.args.get('name')

    title, pic_url = read_url(url)  # 从url中读取缩略图url及标题
    pic_download(pic_url, title)    # 下载缩略图
    into_square(title)              # 裁剪缩略图为正方形

    # 生成点赞页面
    cover_pic(title)                # 放置缩略图
    paste_title(title)              # 放置标题
    userhead(usrhead)               # 放置用户头像
    username(usrname)               # 放置用户昵称
    likes(likenum)                  # 放置点赞用户头像
    combine_pics(title)             # 页面拼接
    return url


@app.route('/image/<imageid>')
def get_image(imageid):
    image = open('%s.jpg'%(imageid),'rb')
    resp = Response(image,mimetype="image/jpg")
    return resp


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)