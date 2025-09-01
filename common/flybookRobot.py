import urllib.parse
import requests
import time
import hmac
import hashlib
import base64


def gen_sign():
    # 当前时间戳
    timestamp = str(round(time.time() * 1000))
    secret='JPlEw3j9z7NdoUPKMUy3yg'
    secret = secret.encode('utf-8')
    # 拼接timestamp和secret
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return timestamp,sign


def send_fb_msg(content_str):
    """
    向飞书机器人推送结果
    :param content_str: 发送的内容
    :param at_all: @全员，默认为True
    :return:
    """                                                                                 
    timestamp_and_sign = gen_sign()
    # url(飞书机器人Webhook地址) + timestamp + sign
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    url='https://open.feishu.cn/open-apis/bot/v2/hook/2c7e6f0e-0537-4fac-b7f3-c0a36638ba68'
    data = {
                "timestamp": timestamp_and_sign[0],
                "sign": timestamp_and_sign[1],
                "msg_type": "text",
                "content": {
                        "text": f"<at user_id=\"all\">所有人</at> {content_str}"
                }
        }
    res = requests.post(url,json=data, headers=headers)
    return res.text

if __name__ == '__main__':
    content="""
    各位好，本次电商项目的测试报告执行结果如下：
    测试用例总共：110
    通过：100
    失败：7
    跳过：4
    异常：7
    点击查看测试报告：www.baidu.com
    """
    send_fb_msg(content)
