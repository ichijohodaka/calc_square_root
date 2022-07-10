from machine import Pin, PWM, Timer
import time
import random

##### constants

SF: int = 10 # sampling frequency in Hz
H: float = 1.0/SF # sampling period in second
NUM_BLADES: int = 3 # the number of blades
PI: float = 3.14159
OUTPUT_FILENAME: str = 'd.csv'
PHOTO_TRANSISTOR_PIN: int = 16 # GP16
PWM_PIN: int = 15 # GP15
PWM_FREQUENCY: int = 10 # PWM frequency in Hz
EX_TIME: int = 15 # recording time in second
DELAY_TIME: int = 5 # delay time to start recording
MAX_DUTY: int = 50000 # for safty and to avoid noisy signals

##### functions

def pulse_count(pin):
    global counter
    counter = counter + 1

def record(timer):
    global counter, counter_prev, omega_record
    ##### recording omega
    omega: float = 2 * PI * (counter - counter_prev)/H/NUM_BLADES
    omega_record.append(omega)
    counter_prev = counter
    
def set_duty(d: float):
    d = int(d)
    if d<0:
        d=0
    else:
        d=min(d,MAX_DUTY)
    pwm.duty_u16( d )

##### global state variables which can be changed locally

counter: int = 0
counter_prev: int = 0
omega_record: list(float) = []

##### preparation

pulse_capture = Pin( PHOTO_TRANSISTOR_PIN, mode = Pin.IN, pull = None )
timer = Timer()
pwm = PWM( Pin( PWM_PIN, Pin.OUT) )

set_duty(0)
pwm.freq( PWM_FREQUENCY )
time.sleep( DELAY_TIME )

##### start of recording

pulse_capture.irq( handler = pulse_count, trigger = Pin.IRQ_FALLING )
timer.init( freq = SF, mode = Timer.PERIODIC, callback = record )

set_duty( 20000 )
time.sleep( EX_TIME )

##### end of recording

timer.deinit() # stop timer
set_duty(0)

##### write to a file

t: float = 0.0
f = open( OUTPUT_FILENAME, 'w')
for omega in omega_record:
    f.write( str(t) + ',' + str(omega) + '\n' )
    t += 1.0*H
f.close()

print('*** finish! ***')
