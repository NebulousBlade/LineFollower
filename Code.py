from machine import Pin, ADC, PWM
import time

# Motor pins with PWM
left_motor_pwm1, left_motor_pwm2 = PWM(Pin(11)), PWM(Pin(10))
right_motor_pwm1, right_motor_pwm2 = PWM(Pin(8)), PWM(Pin(9))

# Set PWM frequency
for pwm in [left_motor_pwm1, left_motor_pwm2, right_motor_pwm1, right_motor_pwm2]:
    pwm.freq(1000)
    
# Sensor pins
left_sensor, middle_sensor, right_sensor = ADC(26), ADC(27), ADC(28)

# Calibration values
DUTY_LEFT = 43000
DUTY_RIGHT = 41000
REVERSE_DUTY = 24000
THRESHOLD = 30000

# Motors Function
def set_motors(left, right):
    if left > 0:
        left_motor_pwm1.duty_u16(min(left, 65535))
        left_motor_pwm2.duty_u16(0)
    elif left < 0:
        left_motor_pwm1.duty_u16(0)
        left_motor_pwm2.duty_u16(min(abs(left), 65535))
    else:
        left_motor_pwm1.duty_u16(0)
        left_motor_pwm2.duty_u16(0)

    if right > 0:
        right_motor_pwm1.duty_u16(min(right, 65535))
        right_motor_pwm2.duty_u16(0)
    elif right < 0:
        right_motor_pwm1.duty_u16(0)
        right_motor_pwm2.duty_u16(min(abs(right), 65535))
    else:
        right_motor_pwm1.duty_u16(0)
        right_motor_pwm2.duty_u16(0)

# Modified turn functions
def move_forward():
    set_motors(DUTY_LEFT, DUTY_RIGHT)

def slight_left():
    set_motors(int(DUTY_LEFT * 0.86), DUTY_RIGHT)

def slight_right():
    set_motors(DUTY_LEFT, int(DUTY_RIGHT * 0.86))

def turn_left():
    set_motors(-REVERSE_DUTY, DUTY_RIGHT)
    time.sleep_ms(30)
    set_motors(0, DUTY_RIGHT)

def turn_right():
    set_motors(DUTY_LEFT, -REVERSE_DUTY)
    time.sleep_ms(30)
    set_motors(DUTY_LEFT, 0)

def stop_motors():
    set_motors(0, 0)
    
    
#Main Loop
while True:
    s_left = left_sensor.read_u16()
    s_middle = middle_sensor.read_u16()
    s_right = right_sensor.read_u16()

    left_detected = s_left < THRESHOLD
    middle_detected = s_middle < THRESHOLD
    right_detected = s_right < THRESHOLD


    if middle_detected and not left_detected and not right_detected:
        move_forward()
    elif left_detected and not right_detected:
        turn_left()
    elif right_detected and not left_detected:
        turn_right()
    elif left_detected and middle_detected and not right_detected:
        slight_right()
    elif right_detected and middle_detected and not left_detected:
        slight_left()
    elif not left_detected and not middle_detected and not right_detected:
        stop_motors()
    elif left_detected and middle_detected and right_detected:
        stop_motors()
    else:
        move_forward()

    time.sleep_ms(2)
