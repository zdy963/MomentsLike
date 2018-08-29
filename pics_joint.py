from PIL import Image, ImageDraw, ImageFont
from math import ceil


def cover_pic(name):
    """
    粘贴封面图片
    :param name: 链接的标题
    :return: 
    """
    cover_path = 'pics/' + str(name) + '.png'
    with Image.open(cover_path) as cover:
        cover_resize = cover.resize((75,75))
    with Image.open('pics/link.png') as background:
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
    with Image.open(bg_path) as background:
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
    with Image.open('pics/head_null.png') as background:
        bg = background.copy()
    head_path = 'pics/portrail/' + str(usrn) + '.jpeg'
    with Image.open(head_path) as head:
        head_resize = head.resize((80,80))
    bg.paste(head_resize,(24,20))
    bg.save('pics/head_mdf.png')


def username(usrn):
    """
    生成用户名图片
    :param username: 用户名
    :return: 
    """
    with Image.open('pics/name.png') as back_ground:
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
    if num > 54:
        num = 53
        count = 53
    else:
        count = num
    row = int(ceil(num / 7))
    # print("total rows:",row)
    bg_path = 'pics/likes/likes' + str(row) + '.png'
    with Image.open(bg_path) as background:
        bg = background.copy()

    index = 1
    for r in range(row-1):
        for i in range(index,index+7):
            prtl_path = 'pics/portrail/' + str(i) + '.jpg'
            xcoor = 20 + 68 + (70+10) * (i-index)
            with Image.open(prtl_path) as prtl:
              bg.paste(prtl,(xcoor,28+ r*80))
        # print("row:",r)
        index += 7
        # print('index:',index)
    for i in range(index,count+1):
        # print(i)
        prtl_path = 'pics/portrail/' + str(i) + '.jpg'
        xcoor = 20 + 68 + (70 + 10) * (i - index)
        with Image.open(prtl_path) as prtl:
            bg.paste(prtl, (xcoor, 28 + (row-1) * 80))
    bg.save('pics/likes_mdf.png')


def combine_pics(ttl):
    """
    将各部分图片进行拼接
    :return: 
    """
    with Image.open('pics/null.png') as background:
        bg = background.copy()

    # 放置顶部状态栏
    with Image.open('pics/TOP.png') as top:
        bg.paste(top,(0,0))

    # 放置头像
    with Image.open('pics/head_mdf.png') as head:
        bg.paste(head,(0,128))

    # 放置昵称
    with Image.open('pics/name_mdf.png')as name:
        bg.paste(name,(124,128))

    # 放置链接
    link_path = 'pics/' + str(ttl) + '.png'
    with Image.open(link_path) as link:
        bg.paste(link,(124,181))

    # 放置时间
    with Image.open('pics/time.png') as time:
        bg.paste(time,(124,299))

    # 放置点赞
    with Image.open('pics/likes_mdf.png') as like:
        bg.paste(like,(0,353))

    # 放置底部评论栏
    with Image.open('pics/BTM.png') as btm:
        bg.paste(btm,(0,1248))

    bg = bg.convert('RGB')
    bg.save('final.jpg')