from PIL import Image, ImageDraw, ImageFont
from math import ceil


def cover_pic(name):
    """
    粘贴封面图片
    :param name: 链接的标题
    :return: 
    """
    cover_path = 'pics/' + str(name) + '.png'
    cover = Image.open(cover_path)
    cover_resize = cover.resize((75,75))
    background = Image.open('pics/link.png')
    bg = background.copy()
    bg.paste(cover_resize,(10,22))
    # bg.show()
    bg_path = 'pics/' + str(name) + '.png'
    bg.save(bg_path)


def split_title(ttl):
    """
    将标题根据长度进行分行，暂未实现对标题进行省略
    :param ttl: 原标题
    :return: 第一行，第二行
    """
    ttl_len = 0.0
    line1 = ""
    index = 0
    for i in range(len(ttl)):
        if ttl_len > 17:
            break
        char = ttl[i]
        index += 1
        line1 += char
        uni_code = ord(char)
        if uni_code == 12288:  # 全角空格直接转换
            uni_code = 32
        if (uni_code >= 19968 and uni_code <= 40869) or (uni_code>=65 and uni_code<=90):
            ttl_len += 1
        elif (uni_code >= 33 and uni_code <= 64) or (uni_code >= 91 and uni_code <= 126):
            ttl_len+= 0.5
    if len(ttl) <= 17:
        line2 = False
    else:
        line2 = ttl[index:]
    return line1,line2


def paste_title(name):
    """
    对标题进行分行处理
    :param name: 标题
    :return: 
    """
    # count = 0
    bg_path = 'pics/' + name + '.png'
    background = Image.open(bg_path)
    title = ImageDraw.Draw(background)
    Ping = ImageFont.truetype('font/Ping.ttf', 26)
    SFPD = ImageFont.truetype('font/SFPD.otf',26)
    title_color = "#000000"
    line_1,line_2 = split_title(name)

    if line_2:
        # cursor = 97
        # for char in line_1:
        #     uni_code = ord(char)
        #     if (uni_code >= 33 and uni_code <= 64) or (uni_code >= 91 and uni_code <= 126):
        #         title.text((cursor,32),char,font=SFPD,fill=title_color)
        #         cursor += 8    # 半角占18个单位
        #         print(char,cursor)
        #     elif (uni_code >= 19968 and uni_code <= 40869) or (uni_code>=65 and uni_code<=90):
        #         title.text((cursor,27),char,font=Ping,fill=title_color)
        #         cursor += 25
        #         print(char,cursor)
        title.text((97,27),line_1,font=Ping, fill=title_color)
        title.text((97,56),line_2,font=Ping,fill=title_color)
    else:
        title.text((97,48),name,font=Ping,fill=title_color)
    background.save(bg_path)


def userhead(usrn):
    """
    替换用户头像
    :param usrn: 用户名
    :return: 
    """
    background = Image.open('pics/head_null.png')
    bg = background.copy()
    head_path = 'pics/portrail/' + str(usrn) + '.jpeg'
    head = Image.open(head_path)
    head_resize = head.resize((80,80))
    bg.paste(head_resize,(24,20))
    bg.save('pics/head_mdf.png')


def username(usrn):
    """
    生成用户名图片
    :param username: 用户名
    :return: 
    """
    back_ground = Image.open('pics/name.png')
    bg = back_ground.copy()
    name = ImageDraw.Draw(bg)
    Ping = ImageFont.truetype('font/Ping_Bold.ttf',30)
    name_color = "#5B6A92"
    name.text((0,17),usrn,font=Ping,fill=name_color)
    bg.save('pics/name_mdf.png')


def likes(num):
    """
    生成点赞页面
    :param num: 点赞个数
    :return: 
    """
    row = int(ceil(num / 7))
    print("total rows:",row)
    bg_path = 'pics/likes/likes' + str(row) + '.png'
    background = Image.open(bg_path)
    bg = background.copy()
    if num > 49:
        count = 49
    else:
        count = num

    index = 1
    for r in range(row-1):
        for i in range(index,index+7):
            prtl_path = 'pics/portrail/' + str(i) + '.jpg'
            prtl = Image.open(prtl_path)
            xcoor = 20 + 68 + (70+10) * (i-index)
            bg.paste(prtl,(xcoor,28+ r*80))
        print("row:",r)
        index += 7
        print('index:',index)
    for i in range(index,count+1):
        print(i)
        prtl_path = 'pics/portrail/' + str(i) + '.jpg'
        prtl = Image.open(prtl_path)
        xcoor = 20 + 68 + (70 + 10) * (i - index)
        bg.paste(prtl, (xcoor, 28 + (row-1) * 80))
    bg.save('pics/likes_mdf.png')


def combine_pics(ttl):
    """
    将各部分图片进行拼接
    :return: 
    """
    background = Image.open('pics/null.png')
    bg = background.copy()

    # 放置顶部状态栏
    top = Image.open('pics/TOP.png')
    bg.paste(top,(0,0))

    # 放置头像
    head = Image.open('pics/head_mdf.png')
    bg.paste(head,(0,128))

    # 放置昵称
    name = Image.open('pics/name_mdf.png')
    bg.paste(name,(124,128))

    # 放置链接
    link_path = 'pics/' + str(ttl) + '.png'
    link = Image.open(link_path)
    bg.paste(link,(124,181))

    # 放置时间
    time = Image.open('pics/time.png')
    bg.paste(time,(124,299))

    # 放置点赞
    like = Image.open('pics/likes_mdf.png')
    bg.paste(like,(0,353))

    # 放置底部评论栏
    btm = Image.open('pics/BTM.png')
    bg.paste(btm,(0,1248))

    bg = bg.convert('RGB')
    bg.save('final.jpg')