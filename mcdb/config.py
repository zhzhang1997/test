#public data
app_id_TD="wx3a9952f97ab8dffe"
app_secret_TD="4dcfd5080a03d909e86e4f1c9d4627b0"
app_id_z = "wx42290aa31253c620"       # tiandao: wx3a9952f97ab8dffe, test: wx82c4bcb714123852
app_secret_z = "9c38002b8b0709ea994594a1e980efde"     # tiandao: 4dcfd5080a03d909e86e4f1c9d4627b0, test: 44690b3806dbd0086bc2dcef0d381528
app_id_d="wx82c4bcb714123852"
app_secret_d = "44690b3806dbd0086bc2dcef0d381528"
response_type = "code"
scope = "snsapi_userinfo"
state = "openid_required"

#private
app_id=app_id_z
app_secret=app_secret_z
ROOT_URL="http://zhzhang1997.natapp1.cc/"
redirect2userUri = ROOT_URL+"user/"
#settings.database
database_zzh={
    'default': {
        'ENGINE': 'django.db.backends.mysql',       # 数据库引擎
        'NAME': 'tdsports',
        'USER': 'zzh',
        'PASSWORD': '123456',
        'HOST': 'localhost',    # 主机
        'PORT': 3306,           # 数据库使用的端口
        'TEST_CHARSET': 'utf8mb4',
    }
}
#url
r_oauth=ROOT_URL+'r_oauth/'
user=ROOT_URL+'user/'
test=ROOT_URL+'test/'
robot=ROOT_URL+'robot/'
index=ROOT_URL+'index/'
myinfo=ROOT_URL+'myinfo/'
lessons=ROOT_URL+'lessons/'
mylessons=ROOT_URL+'mylessons/'
subscribe=ROOT_URL+'subscribe/'
cancelSubscribe=ROOT_URL+'cancelSubscribe'

HTML_INDEX={'index':0,'lessons':1,'mylessons':2,'myinfo':3}

DATABASE=database_zzh


