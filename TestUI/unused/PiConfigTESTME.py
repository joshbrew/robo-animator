# Pass file locations to this with subprocess.Popen(['python','PiConfigTESTME.py'], shell=True)
# Or os.system('python PiConfigTESTME.py')
import json
import os
import re
import time 
#import sys

# Only Works on Raspberry Pi
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class PiRoboConfig(object):
    
    def __init__(self):
        super(PiRoboConfig, self).__init__()
        
        self.motorCFGPath = 'data//motor.cfg' #sys.argv[2]
        self.animCFGPath = 'data//data.dat' #sys.argv[3]
               
        self.loadConfigs()
        
    # Function definitions
        
    def loadConfigs(self):
        
        self.spi_count = 0
        self.spi_ports = []
        
        self.frame_count = 0
        self.frames = []    
            
        self.stepper_count = 0
        self.stepper_motors = []
        
        self.servo_count = 0
        self.servo_motors = []
        
        self.gpio_count = 0
        self.gpio = []
        
        self.sound_count = 0
        self.sounds = []
        
        with open(self.motorCFGPath,'r') as file:
            self.motorCFG_data = json.load(file)
            
        with open(self.animCFGPath, 'r') as file:
            self.animCFG_data = json.load(file)
        
        for spid in self.motorCFG_data[ 'SPI_cfg' ]:
            try:
                self.spi_ports.append([spid['port'],spid['CS'],spid['speed'],spid['mode'],spid['bits'],spid['drivers']])
                self.spi_count += 1
            except:
                print('Unable to configure spi')
        
        for settings in self.motorCFG_data['motor']:
            try:
                if settings['type'] == 'servo':
                    self.servo_motors.append(settings)
                    self.servo_count += 1
                elif settings['type'] == 'gpio':
                    self.gpio.append(settings)
                    self.gpio_count += 1
                elif settings['type'] == 'sound':
                    self.sounds.append(settings)
                    self.sound_count += 1
            except:
                print('undefined type: ', settings['type'])
                
    def seconds_per_frame(self):
        t1 = self.animCFG_data[1]['Time']
        seconds = int(t1[0:1]) * 3600 + int(t1[3:4]) * 60 + int(t1[6:7]) + int(t1[9:14])*0.000001
        return seconds
        
    def run(self):
        os.system('amixer set PCM -- 400 &')
        
        spf = self.seconds_per_frame()
        
        pwm = []
     
        for servo in self.servo_motors:
            GPIO.setup(int(servo['GPIO']), GPIO.OUT)
            pwm.append(GPIO.PWM(int(servo['GPIO']),100))
        for io in self.gpio:
            GPIO.setup(int(io['GPIO']), GPIO.OUT)
        for p in pwm:
            p.start(2.5)
            
        for frame in range(len(self.animCFG_data)):
            #print(self.animCFG_data[frame]['Frame'])
            count = 0
            for servo in self.servo_motors:
                for data in self.animCFG_data[frame]['data']:
                    if data['name'] == servo['name']:
                        move = float(data[servo['Comp']])
                        duty = move / 10.0 + 2.5
                        pwm[count].ChangeDutyCycle(duty)
                        count += 1
            if self.animCFG_data[frame]['Flags'] != '':
                regExp = re.compile("^\s+|\s*,\s*|\s+$")
                flags = [x for x in regExp.split(self.animCFG_data[frame]['Flags']) if x]
                #print(frame)
                for flag in flags:
                    for io in self.gpio:
                        if flag.startswith(io['name']):
                            #print(flag)
                            if flag.endswith('ON') or flag.endswith('1'):
                                #print(True)
                                GPIO.output(int(io['GPIO']),True)
                            if flag.endswith('OFF') or flag.endswith('0'):
                                #print(False)
                                GPIO.output(int(io['GPIO']),False)
                                
                    for sound in self.sounds:
                        if flag == sound['name']:
                            os.system('aplay ' + '/sounds/' + sound['file'])
            
            time.sleep(spf) # cycles by seconds-per-frame
    
    def BytesToHex(self, Bytes):
        return ''.join(["0x%02X " % x for x in Bytes]).strip()
     
        

if __name__ == '__main__':
    cfg = PiRoboConfig()
    cfg.run()

        