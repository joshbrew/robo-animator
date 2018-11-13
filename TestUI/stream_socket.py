# -*- coding: utf-8 -*-
import asyncio
import math
import datetime
import json
import random
import websockets

async def time(websocket, path):
    i=0
    while True:
        DATA = 'Data,'+str(random.randint(1,65535))+','+str(random.randint(1,65535))+','+str(random.randint(1,65535))+' \\r\\n'
        print(DATA)
        DATA = DATA.encode()
        data = DATA.decode().split(',') # gets data, decodes the byte, and splits
        print(data)
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
            
        print(data_dict)
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

"""
#Example multithreading.
MAX_CLIENTS = 3

async def asynchronous():
    start = time.time()
    tasks = [asyncio.ensure_future(
        fetch_async(i)) for i in range(MAX_CLIENTS)]
    await asyncio.wait(tasks)
    print("Process took: {:.2f} seconds".format(time.time() - start))

print('Asynchronous:')
ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()

"""