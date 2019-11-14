from werobot import WeRoBot
import mcdb.config as CONFIG


robot = WeRoBot(token="tiandaotiyu")
robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 8000
robot.config["APP_ID"] = CONFIG.app_id
robot.config["APP_SECRET"] = CONFIG.app_secret

client = robot.client
#url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx42290aa31253c620&redirect_uri=http://zhzhang1997.natapp1.cc/user&response_type=code&scope=snsapi_userinfo&state=123&connect_redirect=1#wechat_redirect"

client.create_menu({
    "button":[
        {
            "type": "view",
            "name": "进入主页",
            "url": CONFIG.r_oauth
        },
        {
            "type": "click",
            "name": "关于我们",
            "key": "aboutus"
        }
    ]
})

