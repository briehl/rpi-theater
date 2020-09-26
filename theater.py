import subprocess
import time
import os
from curses import wrapper, curs_set
from motor import StepperMotor, CLOCKWISE, COUNTERCLOCKWISE
import RPi.GPIO as GPIO

VIDEO_DIR = "./video"
VLC_CMD_BASE = [
    "vlc",
    "--no-audio",
    "--fullscreen",
    "--no-video-title-show",
    "--play-and-exit"
]
MOTOR_PINS = [11, 13, 15, 16]
MOTOR_STEPS = 4000
MOTOR_SPEED = 0.001
LED_PINS = [12]
OPEN = CLOCKWISE            # also for make the lights go up
CLOSE = COUNTERCLOCKWISE    # or make the lights go down

(_, _, filenames) = next(os.walk(VIDEO_DIR))

def play_all_movies(stdscr):
    try:
        gpio_init()
        motor = StepperMotor(*MOTOR_PINS)
        curs_set(0)
        stdscr.clear()
        for f in filenames:
            video = os.path.join(VIDEO_DIR, f)
            cmd = VLC_CMD_BASE + [video]
            resp = subprocess.check_call(cmd)
            cycle_curtain(motor, stdscr)
    except KeyboardInterrupt:
        GPIO.cleanup()

def gpio_init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(MOTOR_PINS + LED_PINS, GPIO.OUT)

def cycle_curtain(motor: StepperMotor, stdscr):
    curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, "Drawing curtain")
    stdscr.refresh()
    run_curtain(motor, MOTOR_STEPS, OPEN, MOTOR_SPEED)
    motor.run(4000, CLOCKWISE, 0.001)
    stdscr.addstr(1, 0, "Lights up!")
    stdscr.refresh()
    pwm = run_lights(OPEN, 5)
    time.sleep(10)
    stdscr.addstr(2, 0, "Lights down!")
    run_lights(CLOSE, 5, pwm)
    stdscr.refresh()
    stdscr.addstr(3, 0, "Drawing curtain back")
    stdscr.refresh()
    run_curtain(motor, MOTOR_STEPS, CLOSE, MOTOR_SPEED)

def run_curtain(motor: StepperMotor, steps: int, d: bool, step_time: float):
    motor.run(steps, d, step_time)

def run_lights(up: bool, cycle_time: float, pwm=None):
    """
    cycle time should be in seconds - how long it should take to run the cycle.
    as soon as the PWM object goes out of scope, it shuts itself off.
    so we have to return p and make sure to assign it to something.
    smells a little hacky, but why not?
    """
    if pwm is None:
        pwm = GPIO.PWM(LED_PINS[0], 100)
        starting_cycle = 0 if up else 100
        pwm.start(starting_cycle)
    dc_steps = list()
    if up:
        dc_steps = range(0, 101, 1)
    else:
        dc_steps = range(100, -1, -1)
    interval = cycle_time / len(dc_steps)
    for dc in dc_steps:
        pwm.ChangeDutyCycle(dc)
        time.sleep(interval)
    return pwm


if __name__ == "__main__":
    # gpio_init()
    # pwm = run_lights(OPEN, 5)
    # print("done with light?")
    # time.sleep(5)
    # run_lights(CLOSE, 5, pwm)
    # GPIO.cleanup()
    wrapper(play_all_movies)
