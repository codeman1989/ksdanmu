# pip install websocket-client
# Get the liveStreamId
# POST
# https://live.kuaishou.com/graphql
# accept: */*
# Origin: https://live.kuaishou.com
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36
# content-type: application/json
# Referer: https://live.kuaishou.com/u/AnGg0402
# Accept-Encoding: gzip, deflate, br
# Accept-Language: zh-CN,zh;q=0.9
# {"operationName":"LiveDetail","variables":{"principalId":"AnGg0402"},"query":"query LiveDetail($principalId: String){\n  liveDetail(principalId: $principalId) {\n    liveStream\n}}"}

import websocket
import struct
import time
import thread

Flag = True
debug = False
def on_message(ws, message):
    data = ""
    for i in message:
        data = data + hex(ord(i)).replace('0x','')
    print(data)

def on_error(ws, error):
    print(error)

def on_close(ws):
    Flag = False
    print("### closed ###")

def on_open(ws):
    part1 = [8,200,1,26,135,1,10,88,57,103,52,112,101,54,81,86,122,106,111,80,47,120,88,65,74,68,71,88,80,116,73,68,71,69,70,115,90,52,78,67,43,73,49,105,48,113,47,66,97,67,82,87,48,47,120,119,43,106,43,70,97,88,66,118,69,85,66,118,116,52,79,87,122,114,117,104,99,65,83,106,110,51,108,104,71,51,103,65,101,102,57,70,43,81,61,61,18,11]
    part3 = [58,30,105,113,85,87,70,115,126,97,49,65,52,65,108,119,49,81,95,49,53,51,54,53,56,54,51,54,55,52,54,57]
    part2 = [115, 73, 70, 111, 71, 116, 105, 103, 76, 66, 119]
    
    d = part1 + part2 + part3
    ws.send(d,0x2)
    
    #heart beat thread start
    def run():
        while(Flag):
            time.sleep(2)
            ws.send([8,1,26,7,8,184,232,190,199,220,44],0x2)
    thread.start_new_thread(run, ())

# debug
websocket.enableTrace(debug)
ws = websocket.WebSocketApp("wss://live-ws-pg.kuaishou.com/websocket",on_message = on_message,on_error = on_error,on_close = on_close)
ws.on_open = on_open
ws.run_forever(skip_utf8_validation=True)
