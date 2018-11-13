
#!/usr/bin/python

#import spidev
import time
import json
import csv

# Only Works on Raspberry Pi
import RPi.GPIO as GPIO

import os


GPIO.setmode(GPIO.BCM)





#defin class for stepper motors
class stepper_motor(object):
    
    def __init__(self, name, CS, rot, movement,dir):
        self.name = name
        self.CS = CS
        self.movement = movement
        self.rot = rot
        self.dir = dir
#self.bus = bus
#self.drivernumber = drivernumber

#define class for servos
class servo_motor(object):
    
    def __init__(self, name, GPIO, Comp):
        self.name = name
        self.GPIO = GPIO
        self.Comp = Comp
#define class for GPIO
class gpio(object):
    
    def __init__(self, name, GPIO):
        self.name = name
        self.GPIO = GPIO

#define class for GPIO
class soundfile(object):
    
    def __init__(self, name, file):
        self.name = name
        self.file = file

#define class for SPI Port
class spi_port(object):
    
    def __init__(self, port, cs, speed, mode, bits, drivers):
        self.port = port
        self.cs = cs
        self.speed = speed
        self.mode = mode
        self.bits = bits
        self.drivers = drivers

def BytesToHex(Bytes):
    return ''.join(["0x%02X " % x for x in Bytes]).strip()
#end def


#reading json file
with open('motor.cfg', 'r') as f:
    json_data = json.load(f)

#get spi port data
spiport = []
for spid in json_data[ 'SPI_cfg' ]:
    try:
        spitemp = spi_port(spid['port'],spid['CS'],spid['speed'],spid['mode'],spid['bits'],spid['drivers'])
        #print(spid['port'],spid['CS'],spid['speed'],spid['mode'],spid['bits'])
        spiport.append(spitemp)
    except:
        print('Unable to configure spi')


#get motor data
motortype = {}
motorrot = {}
motordir = {}
motormovement = {}
motorgpio = {}
frames = []
frames.append([])
stepper_count = 0
stepper_motors = []
servo_motors = []
sound=[]
gpio = []
for motor_cfg in json_data[ 'motor' ]:
    try:
        if motor_cfg['type'] == "stepper":
            #print (motor_cfg['CS'], motor_cfg['Rot'], motor_cfg['movement'])
            temp = stepper_motor(motor_cfg['name'], motor_cfg['CS'], motor_cfg['Rot'], motor_cfg['movement'],motor_cfg['Direction'])
            stepper_motors.append(temp)
            stepper_count = stepper_count + 1
            frames.append([])
            motortype[motor_cfg['name']]=motor_cfg['type']
            motorrot[motor_cfg['name']]=motor_cfg['Rot']
            motormovement[motor_cfg['name']]=motor_cfg['movement']
            motordir[motor_cfg['name']]=motor_cfg['Direction']
        
        elif motor_cfg['type'] == "servo":
            temp = servo_motor(motor_cfg['name'],motor_cfg['GPIO'],motor_cfg['Comp'])
            servo_motors.append(temp)
            frames.append([])
        elif motor_cfg['type'] == "gpio":
            temp = gpio(motor_cfg['name'],motor_cfg['GPIO'])
            gpio.append(temp)
            frames.append([])
        elif motor_cfg['type'] == "sound":
            temp = soundfile(motor_cfg['name'],motor_cfg['file'])
            sound.append(temp)
            frames.append([])
        else:
            print(motor_cfg['type'], ' not found for ', motor_cfg['name'])
    except:
        print('motor type not defined for motor ', motor_cfg['name'])




#open csv file
#ifile = open('test1.csv', 'rb')
#reader = csv.reader(ifile)
reader = csv.reader(open('test1.csv'))
#row_count = sum(1 for row in ifile)
#print ('row count=', row_count)
#print ('motor count=',stepper_count)

                    #ifile.seek(0)
frames.append([])
frames.append([])
frames.append([])
frames.append([])

rownum = 0
for row in reader:
    # Save header row.
    if rownum == 0:
        print (row)
        colnum = 0
        header = row
        for col in row:
            #frames[header[colnum]]={}
            frames[colnum].append(col)
            colnum += 1
    #print row
    elif rownum == 1:
        print (row)
        colnum = 0
        header = row
        for col in row:
            #frames[header[colnum]]={}
            frames[colnum].append(col)
            colnum += 1
            print (colnum)
    else:
        colnum = 0
        for col in row:
            #print '%-8s: %s' % (header[colnum], col)
            #print ('colnum', colnum)
            frames[colnum].append(int(col))
            colnum += 1

    rownum += 1
rownum -=1
#ifile.close()
servo_count=0
pwm=[]
os.system('amixer set PCM -- 400 &')
#Setup the servos
for Sevrs in servo_motors:
    GPIO.setup(int(Sevrs.GPIO), GPIO.OUT)
    pwm.append(GPIO.PWM(int(Sevrs.GPIO), 100))

for ios in gpio:
    GPIO.setup(int(ios.GPIO), GPIO.OUT)

for p in pwm:
    p.start(2.5)

for x in range(2, rownum):
    servo_count = 0
    io_count = 0
    for frame in frames:
        print ( frame[0])
        if frame[0] == 'S':
            print('x=',x)
            print(frame[x])
            print('servo = ',servo_count-1)
            move = int(frame[x])
            duty = float(move) / 10.0 + 2.5
            pwm[servo_count-1].ChangeDutyCycle(duty)
            servo_count +=1
        elif frame[0] == 'G':
            print(gpio[io_count].GPIO)
            if int(frame[x]) == 1:
                GPIO.output(int(gpio[io_count].GPIO), True)
                print ('high')
            else:
                GPIO.output(int(gpio[io_count].GPIO), False)
                print ('low')
            io_count += 1
        elif frame[0] == 'A':
            if int(frame[x]) > 0:
                os.system(sound[int(frame[x])-1].file)
        else:
            time.sleep(1)
            print ('sleeping')

        





#time.sleep(5)



print ("end of program")









