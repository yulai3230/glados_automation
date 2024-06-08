import requests,json,os
# -------------------------------------------------------------------------------------------
# github workflows
# -------------------------------------------------------------------------------------------

if __name__ == '__main__':
# pushplus秘钥 申请地址 http://www.pushplus.plus
    sckey = os.environ.get("PUSHPLUS_TOKEN", "")
# 推送内容
    sendContent = ''
# glados账号cookie 直接使用数组 如果使用环境变量需要字符串分割一下
    cookies = os.environ.get("GLADOS_COOKIE", []).split("&")
    if cookies[0] == "":
        print('未获取到COOKIE变量') 
        cookies = []
        exit(0)
    url= "https://glados.rocks/api/user/checkin"
    url2= "https://glados.rocks/api/user/status"
    referer = 'https://glados.rocks/console/checkin'
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    payload={
        'token': 'glados.one'
    }
    for cookie in cookies:
  
        checkin = requests.post(url,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent,'content-type':'application/json;charset=UTF-8'},data=json.dumps(payload))
        state =  requests.get(url2,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent})
    #--------------------------------------------------------------------------------------------------------#  
        try:
            time = state.json()['data']['leftDays']
            time = time.split('.')[0]
            email = state.json()['data']['email']

            #获取用户信息
            change=checkin.json()['list'][0]['change'].split('.')[0]
            balance=checkin.json()['list'][0]['balance'].split('.')[0]
        except:
            requests.get('http://www.pushplus.plus/send?token=' + sckey + '&title=签到失败！！！'+'&content=出现异常')
            print('出现异常')  # 日志输出
            exit(0)

        if 'message' in checkin.text:
            mess = checkin.json()['message']
            print("签到成功") # 日志输出
            sendContent =f'共计积分:\t\t{balance}\n今日积分:\t\t{change}\n剩余天数:\t\t{time}\n用户账号:\t\t{email}\n\nTip:\t\t{mess}\n'
        else:
            requests.get('http://www.pushplus.plus/send?token=' + sckey + '&title=签到失败！！！'+'&content='+email+'\ncookie已失效')
            print('cookie已失效')  # 日志输出
     #--------------------------------------------------------------------------------------------------------#   
    if sckey != "":
         requests.get('http://www.pushplus.plus/send?token=' + sckey + '&title=Glados 自动签到'+'&content='+sendContent)
