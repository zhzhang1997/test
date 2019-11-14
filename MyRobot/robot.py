from werobot import WeRoBot

myrobot = WeRoBot(token="tiandaotiyu")

@myrobot.handler
def hello(message):
    return "你好啊"





