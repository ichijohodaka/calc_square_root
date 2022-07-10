from machine import Pin, PWM, Timer
import time

##### constants

SF: int = 10 # sampling frequency in Hz
H: float = 1.0/SF # sampling period in second
NUM_BLADES: int = 3 # the number of blades
PI: float = 3.14159
OUTPUT_FILENAME: str = 'd.csv'
PHOTO_TRANSISTOR_PIN: int = 16 # GP16
PWM_PIN: int = 15 # GP15
PWM_FREQUENCY: int = 10 # PWM frequency in Hz
EX_TIME: int = 10 # recording time in second
DELAY_TIME: int = 5 # delay time to start recording
MAX_DUTY: int = 65535 # for safty and to avoid noisy signals

##### functions

def pulse_count(pin):
    global counter
    counter = counter + 1

def record_control(timer):
    global counter, counter_prev, omega_record
    ##### recording omega
    omega: float = 2 * PI * (counter - counter_prev)/H/NUM_BLADES
    omega_record.append(omega)
    counter_prev = counter
    ##### control
    global Cinput_prev, Coutput_prev, reference_record, mu_record
    reference_record.append(reference)
    mu_record.append(mu)
    Cinput = reference - omega
    Coutput = discrete_output( a0, a1, b0, b1, Cinput, Cinput_prev, Coutput_prev )
    set_duty( Coutput )
    Cinput_prev = Cinput
    Coutput_prev = Coutput
    
def set_duty(d: float):
    d = int(d)
    if d<0:
        d=0
    else:
        d=min(d,MAX_DUTY)
    pwm.duty_u16( d )
    


def discrete_output( a0: float, a1: float, b0: float, b1:float, input_now: float, input_prev: float, output_prev: float) -> float:
    den = a0 + H/2*a1
    c1 = (a0-H/2*a1)/den
    c2 = (b0+H/2*b1)/den
    c3 = - (b0-H/2*b1)/den
    return c1*output_prev + c2*input_now + c3*input_prev

##### paramters

K: float = 0.024
T: float = 2.0
mu: float = 1.0
a0: float = K * mu
a1: float = 0.0
b0: float = T
b1: float = 1.0

##### global state variables which can be changed locally

counter: int = 0
counter_prev: int = 0
omega_record: list(float) = []
Cinput_prev: float = 0.0
Coutput_prev: float = 0.0

reference_record: list(float) = []
mu_record: list(float) = []

##### preparation

pulse_capture = Pin( PHOTO_TRANSISTOR_PIN, mode = Pin.IN, pull = None )
timer = Timer()
pwm = PWM( Pin( PWM_PIN, Pin.OUT) )

set_duty(0)
pwm.freq( PWM_FREQUENCY )
time.sleep( DELAY_TIME )

##### start of recording

reference: float = 500.0 # rad/s
print('reference=',reference)
pulse_capture.irq( handler = pulse_count, trigger = Pin.IRQ_FALLING )
timer.init( freq = SF, mode = Timer.PERIODIC, callback = record_control )

time.sleep( EX_TIME )

##### end of recording

timer.deinit() # stop timer
set_duty(0)

##### write to a file

t: float = 0.0
f = open( OUTPUT_FILENAME, 'w')
for omega, r, m in zip(omega_record, reference_record, mu_record):
    f.write( str(t) + ',' + str(omega) + ',' + str(r) + ',' + str(m) + '\n' )
    t += 1.0*H
f.close()

print('*** finish! ***')
