from conn import dbconn


def wx_login(wx_id):
    """
    使用wx_id找uid
    :param wx_id: 用户的微信id
    :return: uid
    """
    print("---------Loging in---------")
    with dbconn() as db:
        cursor = db.cursor()
        query_id = "SELECT ID FROM USERS WHERE WX_ID='%s'" %(wx_id)
        cursor.execute(query_id)
        uid = str(cursor.fetchone()[0])

        # 顺手注册
        if not uid:
            print("---------User doesn't exist---------")
            return False
        else:
            print("---------Login success!---------")
            print("uid:",uid)
            return uid


def register(wx_id,avatar,username):
    """
    使用wx_id注册
    :param wx_id: 微信id
    :param avatar: 用户头像url
    :param username: 用户名
    :return: 新用户的uid
    """
    print("---------Registering---------")
    if avatar is None:
        avatar = 'default'
    with dbconn() as db:
        cursor = db.cursor()
        create_users = "INSERT INTO USERS (WX_ID,USERNAME,AVATAR) VALUE ('%s','%s','%s')" %(wx_id,avatar,username)
        # try:
        cursor.execute(create_users)
        db.commit()
        print("---------Register success!---------")
        # except:
        uid = wx_login(wx_id)
        print("---------Login success!---------")
        print("uid:",uid)
        return uid