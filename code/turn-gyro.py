import runloop
import motor_pair
import motor
from hub import motion_sensor

LEFT=-100
RIGHT=100

async def turn(degrees, direction, velocity=200, acceleration=400, correction=0):
    """
    Turn the robot a certain number of degrees in a certain direction, using yaw measurements from the motion sensor.
    In theory, this should be accurate and not require any adjustments for wheel size or surface, but in practice we have noticed anomalies,
    and in fact we would occasionally need to restart the hub to get it to work at all.
    :param degrees: The number of degrees to turn. Positive is right, negative is left.
    :param direction: The direction to turn. Use LEFT or RIGHT (defined as constants above).
    """
    # wait for the yaw to register as 0 (or at least close)
    while abs(motion_sensor.tilt_angles()[0]) > 2:
        motion_sensor.reset_yaw(0)
        await runloop.sleep_ms(10)

    while abs(motion_sensor.tilt_angles()[0]) < degrees * 10 - correction:
        motor_pair.move(motor_pair.PAIR_1, direction, velocity=velocity, acceleration=acceleration)

    motor_pair.stop(motor_pair.PAIR_1, stop=motor.SMART_BRAKE)

async def main():
    await turn(90, RIGHT)
    await runloop.sleep_ms(250)
    await turn(90, LEFT)
    await runloop.sleep_ms(250)

    raise SystemExit

runloop.run(main())
