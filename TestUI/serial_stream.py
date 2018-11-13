# -*- coding: utf-8 -*-

import serial

ser = serial.Serial(port='/dev/cu.usbmodemFD1211',
                    baudrate=2000000,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                    )

ser.readline()

import asyncio
import math
import datetime
import json
import websockets



async def time(websocket, path):
    i=0
    while True:
        data = ser.readline().decode().split(',') # gets data, decodes the byte, and splits
        # stream format [Data, x,y,z,x2,y2,z2,... \\r\\n']
        endpoint = data[len(data)-1].split(' ')[0] # strip the \\r\\n
        data[len(data)-1] = endpoint # rewrite end
        data_dict = {}
        count = 1
        i = 1
        for out in data[1:]: # build a dict from the data
            if count == 1:
                data_dict['x_'+str(math.ceil(i*0.3333333))] = out
            if count == 2:
                data_dict['y_'+str(math.ceil(i*0.3333333))] = out
            if count == 3:
                data_dict['z_'+str(math.ceil(i*0.3333333))] = out
                count = 0
            count += 1
            i += 1
        now = json.dumps({
                'Data':data_dict,
                't':datetime.datetime.utcnow().isoformat(),
                'i':i
                })
        i+=1
        await websocket.send(now)
        await asyncio.sleep(1) # Change this to match sample rate

start_server = websockets.serve(time, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

