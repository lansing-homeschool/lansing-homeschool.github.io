import runloop
import motor_pair

LEFT=-100
RIGHT=100

async def turn(degrees, direction, velocity=200, acceleration=400):
    """
    Turn the robot a certain number of degrees in a certain direction, using a calculation to determine the number of degrees of wheel
    rotation that would rotate the robot's facing direction that many degrees. Wheel size and wheelbase would change this value.
    1.8 was the value that the team found by trial and error to be the correct value for the robot they were using.
    :param degrees: The number of degrees to turn. Positive is right, negative is left.
    :param direction: The direction to turn. Use LEFT or RIGHT (defined as constants above).
    """
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, int(degrees * 1.8), direction, velocity=velocity, acceleration=acceleration, deceleration=acceleration)

async def main():
    await turn(90, RIGHT)
    await runloop.sleep_ms(250)
    await turn(90, LEFT)
    await runloop.sleep_ms(250)

    raise SystemExit

runloop.run(main())
