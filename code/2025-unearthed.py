import runloop
import motor_pair
import motor
from hub import port, motion_sensor

LEFT=-100
RIGHT=100

HOOK_RANGE=223

motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)
top_motor=port.F
bottom_motor=port.C
wheel_circumference_inches=6.889764 # 17.5cm / 2.54cm per inch
motion_sensor.set_yaw_face(motion_sensor.TOP)

active_routine=0

async def turn(degrees, direction, velocity=200, acceleration=1000):
    await turn_rotations(degrees, direction, velocity, acceleration)

async def turn_rotations(degrees, direction, velocity=200, acceleration=400):
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,
                                      int(degrees * 1.8),
                                      direction,
                                      velocity=velocity,
                                      acceleration=acceleration,
                                      deceleration=acceleration)
    return

async def drive(distance_in_inches, steering=0, velocity=700,
                acceleration=500, deceleration=500):
    """
    distance_in_inches: The value to drive in inches
    steering: between -100 for left and 100 for right. default is 0 for straight
    velocity: between -1050 and 1050. default is 500
    acceleration: between 0 and 10000. default is 500
    deceleration: between 0 and 10000. default is 500
    """
    degrees = int((distance_in_inches/wheel_circumference_inches)*360)

    await motor_pair.move_for_degrees(motor_pair.PAIR_1, degrees, steering,
                                      velocity=velocity, acceleration=acceleration,
                                      deceleration=deceleration,
                                      stop=motor.SMART_BRAKE)

def spinWheels(velocity=1000):
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=velocity)

async def lowerForks(degrees=-3360):
    await motor.run_for_degrees(bottom_motor, degrees, 1000)

async def liftForks(degrees=3360):
    await motor.run_for_degrees(bottom_motor, degrees, 1000)

async def lifthook(degrees=HOOK_RANGE, velocity=500):
    await motor.run_for_degrees(bottom_motor, -degrees, velocity)

async def drophook(degrees=HOOK_RANGE, velocity=1000, acceleration=1000):
    await motor.run_for_degrees(bottom_motor, degrees,
                                velocity, acceleration=acceleration)

async def motorsToZero():
    runloop.run(
        motor.run_to_absolute_position(top_motor, 0, 500),
        motor.run_to_absolute_position(bottom_motor, 0, 500)
    )

async def liftArm(degrees=180):
    await motor.run_for_degrees(bottom_motor, degrees, 500)

async def dropArm(degrees=180, velocity=1110):
    await motor.run_for_degrees(bottom_motor, -degrees, velocity, acceleration=10000)

async def easterIsland():
    await liftArm()
    await drive (17)
    for i in range(3):
        await dropArm()
        await liftArm()
        await runloop.sleep_ms(500)
    await drive(-17)
 
async def wackTheTable():
    await liftArm()
    await drive(-1)
    await drive(14)
    await turn(17, LEFT)
    await drive(24.5,-4,500)
    await turn(LEFT,60)
    await drive(9.25)
    await turn(92,LEFT)
    await drive(-2)
    # KicktheBucket
    await dropArm(degrees=90,velocity=500)
    await liftArm(90)
    await turn(75,LEFT)
    await drive(12.5)
    await turn(50,RIGHT)
    await drive(32)

async def theOtherSide():
    await drive(-1)
    await drive(11.2)
    await turn(90, LEFT)
    await drive(21.3)
    await lifthook()
    await turn(90, RIGHT)
    await drive(-0.3)
    await drophook()
    await drive(-2.5)
    await drive(0.2)
    await turn(110, RIGHT)
    await drive(-35, 7)
    await drive(-20,-3)

async def liftTable():
    await drive(17)
    await turn_rotations(45, LEFT)
    await drive(12, -10, 700)

async def brushBrushBrush():
    await liftForks(765)
    await drive(-1.67)
    await drive(24)
    await turn(90,LEFT)
    await turn(45,LEFT)
    await turn(90,RIGHT)
    await liftForks(900)
    await drive(-2.67)
    await turn(150,LEFT)
    await drive(14)
 
async def mineIronOre():
    await drive(-1.67)    
    await drive(30)
    await turn(90,RIGHT)
    await drive(14)
    await turn(90,LEFT)
    await lifthook(160)
    await runloop.sleep_ms(3000)
    await drophook(130)
    await turn(90,LEFT)
    await drive(11)
    await turn(75,LEFT)
    await drive(27.5)

async def raiseTheSails():
    await lifthook()
    await drive(21.2,2)
    await drophook()
    await drive(-1.5)
    await lifthook()
    await drive(-18.5)

async def loopHole():
    await drive(-1)
    await drive(28)
    await turn(40, LEFT)
    await liftForks(500)
    await drive(5)
    await liftForks(1500)
    await drive(-5)
    await turn(40,RIGHT)
    await drive(-29)

async def main():
    # loaded as #1
    # - line up to the left edge of the left back of the robot
    #   to 2nd major line to the left
    await easterIsland()

    # loaded as #2
    # - line up to the back, right the right side at the
    #   second major line from the right
    await wackTheTable()

    # loaded as #3
    await raiseTheSails()

    # loaded as #4
    await theOtherSide()

    # loaded as #5
    await brushBrushBrush()

    # loaded as #6
    await mineIronOre()

    # loaded as #7
    await loopHole()

    raise SystemExit

runloop.run(main())