from dingtalkchatbot.chatbot import DingtalkChatbot
from django.conf import settings

def send(messgae,at_mobiles=[]):
    # 引用settings里面配置的钉钉消息通知的WebHook地址：
    webhook = settings.DINGTALK_WEB_HOOK
    # 初始化机器人大小 #方式一： 通常初始化方式
    xiaoding = DingtalkChatbot(webhook)
    # 方式二： 勾选 “加签” 选项时使用（v1.5 以上）
    # xiaoding = DingtalkChatbot(webhook,secret=secret)

    # Text消息 @所有人
    xiaoding.send_text(msg=('通知: %s'%messgae),at_mobiles=at_mobiles)