import RPi.GPIO as GPIO
import time

STEPS = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

CLOCKWISE = True
COUNTERCLOCKWISE = False

# in1 = 11
# in2 = 13
# in3 = 15
# in4 = 16
# chans = [in1, in2, in3, in4]


# GPIO.setup([in1, in2, in3, in4], GPIO.OUT)
step = 0
direction = True  # True = clockwise, False = counterclockwise

class StepperMotor:
    """
    Provides an interface for the 28BYJ-48 stepper motor.
    Usage:
    motor = StepperMotor(pin1, pin2, pin3, pin4)
    motor.run(direction, num_steps)
    motor.shutdown()

    pin1 through pin4 match up with the IN1 through IN4 on the motor driver board
    Initializing a StepperMotor class will claim control of the pins.
    It's best to run motor.shutdown() before ending your program.
    """
    def __init__(self, pin1: int, pin2: int, pin3: int, pin4: int):
        self.pins = [pin1, pin2, pin3, pin4]

    def _get_next_step(self, step: int, d: bool) -> int:
        step += 1 if d == CLOCKWISE else -1
        if step > 7:
            return 0
        elif step < 0:
            return 7
        else:
            return step

    def _do_step(self, step: int):
        if step < 0 or step > 7:
            GPIO.output(self.pins, [0, 0, 0, 0])
        else:
            GPIO.output(self.pins, STEPS[step])

    def run(self, steps: int, direction: bool, speed: float):
        """
        Run the motor in a direction for a certain number of steps with
        some speed (time between steps).
        e.g.
        motor.run(CLOCKWISE, 4000, 0.01)
        """
        if steps <= 0:
            return
        cur_step = 0
        for i in range(steps):
            self._do_step(cur_step)
            cur_step = self._get_next_step(cur_step, direction)
            time.sleep(speed)
        self._do_step(-1)

if __name__ == "__main__":
    pins = [11, 13, 15, 16]
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pins, GPIO.OUT)
    motor = StepperMotor(*pins)
    motor.run(4000, CLOCKWISE, 0.001)
    GPIO.cleanup()