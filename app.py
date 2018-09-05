from flask import Flask,request, Response
from get_info import read_url,pic_download,into_square
from pics_joint import cover_pic, paste_title,likes,username,combine_pics,userhead
from portrait_service import download_portrait
from users_service import register,wx_login, update_portrait

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
        print("Testing mode")
        url = 'https://mp.weixin.qq.com/s/g-xI1RkU7UUC8pQsDCZD_A'
        uid = '0'
        usrname = '葛蒙蒙'
    else:             # regular mode
        print("Regular mode")
        uid = request.args.get('uid')
        url = request.args.get('url')
        usrname = request.args.get('name')
    print("Getting info as:----------\nurl:%s\nuid:%s\nusername:%s\n------------------"%(url,uid,usrname))

    title, pic_url = read_url(url)  # 从url中读取缩略图url及标题
    pic_download(pic_url, title)    # 下载缩略图
    into_square(title)              # 裁剪缩略图为正方形

    # 生成点赞页面
    cover_pic(title)                # 放置缩略图
    paste_title(title)              # 放置标题
    userhead(uid)               # 放置用户头像
    username(usrname)               # 放置用户昵称
    likes(likenum)                  # 放置点赞用户头像
    combine_pics(title)             # 页面拼接
    return url


@app.route('/image/<imageid>')
def get_image(imageid):
    """
    通过url访问最后生成的点赞页面的sjpg
    :param imageid: 
    :return: 
    """
    print("Opening image.")
    image = open('%s.jpg'%(imageid),'rb')
    resp = Response(image,mimetype="image/jpg")
    # image.close()
    return resp


@app.route('/login')
def login():
    """
    非常偷懒的登陆方式，使用wx_id换user的id
    如果没有注册就帮用户注册了再登陆
    最后为用户更新头像
    :return: userid
    """
    wx_id = request.args.get('wxid')
    avatar = request.args.get('avatar')
    username = request.args.get('username')
    print("wxid:",wx_id)

    uid = wx_login(wx_id,avatar)
    if uid is False:
        uid = register(wx_id,avatar,username)
    else:
        # Automatically update user's portrait url
        update_portrait(uid, avatar)

    download_portrait(avatar, uid)

    return uid


@app.route('/update')
def update():
    """
    更新用户的头像
    这个动作应该在用户每次登陆的时候进行
    :return: 
    """
    avatar = request.args.get('avatar')
    uid = request.args.get('uid')
    suc = update_portrait(uid,avatar)
    if suc:
        return avatar


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)