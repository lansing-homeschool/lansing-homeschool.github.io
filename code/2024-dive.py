"""
This is the code for the 2024 FLL Season Dive/Submerged Challenge.
Our team uses a single program, but comments out all but one mission at a time in main and
uploads the code to the hub in a specific slot.

Slot | Function   | Description
-----|------------|---------------------------------------------------
1    | whackShark | Hit the shark, hit water sample, flip coral buds, get back home
2    | moveShark  | Drop shark off, get the octopus, go home on the right side
3    | moveOcto   | Drop octo off, get plankton sample, move angler fish, go to left home
4    | liftMast   | Raise the mast of the ship
5    | moveCoral  | Optional mission. Move a coral that is in home, out of home
"""

import runloop
import motor_pair
from hub import port, motion_sensor

import motor

TURN_BY="DEGREES"

LEFT=-100
RIGHT=100

HOOK_RANGE=217

motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)
top_motor=port.F
bottom_motor=port.C
wheel_circumference_inches=6.889764 # 17.5cm / 2.54cm per inch
motion_sensor.set_yaw_face(motion_sensor.TOP)

async def turn(degrees, direction, velocity=200, acceleration=1000):
    """
    Turns the robot by a the number of degrees using the default method (gyro, rotations)
    degrees: The value to turn in degrees
    direction: Either -100 for left or 100 for right (set as the constants LEFT and RIGHT).
    velocity: between -1050 and 1050. default is 200
    acceleration: between 0 and 10000. default is 1000. Also used for deceleration
    """
    if TURN_BY == "DEGREES":
        await turn_gyro(degrees if direction == RIGHT else -degrees, velocity, acceleration)
    else:
        await turn_rotations(degrees, direction, velocity, acceleration)

async def turn_rotations(degrees, direction, velocity=200, acceleration=400):
    """
    Turn the robot a certain number of degrees in a certain direction, using a calculation
    to determine the number of degrees of wheel rotation that would rotate the robot's
    facing direction that many degrees. Wheel size and wheelbase would change this value.
    1.8 was the value that the team found by trial and error to be the correct value for the
    robot they were using.
    
    degrees: The value to turn in degrees
    direction: Either -100 for left or 100 for right (set as the constants LEFT and RIGHT).
    velocity: between -1050 and 1050. default is 200
    acceleration: between 0 and 10000. default is 1000. Also used for deceleration
    """
    # convert the degrees of desired turn to the number of degrees the motors need to turn
    await motor_pair.move_for_degrees(
        motor_pair.PAIR_1, 
        int(degrees * 1.8), 
        direction, 
        velocity=velocity, 
        acceleration=acceleration, 
        deceleration=acceleration
    )
    return

async def turn_gyro(angle, velocity=100, acceleration=1000):
    """
    Turn the robot a certain number of degrees in a certain direction, using yaw value
    from the motion sensor. This should be accurate and not require any adjustments
    for wheel size or surface, but in practice we have noticed anomalies, and in fact we
    occasionally needed to restart the hub to get it to work at all.
    angle: The number of degrees to turn. Positive is right, negative is left.
    velocity: between -1050 and 1050. default is 100
    acceleration: between 0 and 10000. default is 1000
    """

    # try to wait for the robot to be stable with the current direction set to 0
    motion_sensor.reset_yaw(0)
    await runloop.until(motion_sensor.stable)
    await runloop.sleep_ms(200)
    await runloop.until(motion_sensor.stable)

    # set steering for either a left or right turn based on positive or negative angle
    steering = 100 if angle >= 0 else -100

    # start turning
    motor_pair.move(
        motor_pair.PAIR_1, 
        steering, 
        velocity=velocity, 
        acceleration=acceleration
    )

    def done():
        # get yaw in decidegrees (tenths of a degree), flip sign, and convert to degrees
        yaw_deg = motion_sensor.tilt_angles()[0] * -0.1
        # return false until the robot has turned the desired angle
        return abs(yaw_deg) >= abs(angle)

    # sleep until the robot has turned the desired angle and then stop the drive motors
    await runloop.until(done)
    motor_pair.stop(motor_pair.PAIR_1)

async def drive(distance_in_inches, steering=0, velocity=700, acceleration=500):
    """
    distance_in_inches: The value to drive in inches
    steering: between -100 for left and 100 for right. default is 0 for straight
    velocity: between -1050 and 1050. default is 500
    acceleration: between 0 and 10000. default is 500
    deceleration: between 0 and 10000. default is 500
    """
    degrees = int((distance_in_inches/wheel_circumference_inches)*360)

    await motor_pair.move_for_degrees(
        motor_pair.PAIR_1, 
        degrees, 
        steering, 
        velocity=velocity, 
        acceleration=acceleration, 
        deceleration=acceleration, 
        stop=motor.SMART_BRAKE
    )

async def liftArm(degrees=180):
    """
    Lift the arm (with the extra bricks for weight) of the robot.
    degrees: The number of degrees to lift the arm. Default is 180, but can be changed.
    """
    await motor.run_for_degrees(bottom_motor, degrees, 500)

async def dropArm(degrees=180):
    """
    Drop the arm (with the extra bricks for weight) of the robot.
    degrees: The number of degrees to drop the arm. Default is 180, but can be changed.
    """
    await motor.run_for_degrees(bottom_motor, -degrees, 1110, acceleration=10000)

async def lifthook(degrees=HOOK_RANGE, velocity=500):
    """
    Lift the hook (attachment with single curved "hook" pointing down) of the robot.
    degrees: The number of degrees to lift the hook. Default is 217, but can be changed.
    velocity: between -1050 and 1050. default is 500. How fast to lift the hook.
    """
    await motor.run_for_degrees(bottom_motor, -degrees, velocity)

async def drophook(degrees=HOOK_RANGE, velocity=1000, acceleration=1000):
    """
    Drop the hook (attachment with single curved "hook" pointing down) of the robot.
    degrees: The number of degrees to drop the hook. Default is 217, but can be changed.
    velocity: between -1050 and 1050. default is 500. How fast to drop the hook.
    """
    await motor.run_for_degrees(bottom_motor, degrees, velocity, acceleration=acceleration)

async def whackShark():
    """
    Whack the shark, back up into the water sample, flip the coral buds, then get back home
    Line up to cover the d in education with the right side of the robot
    """
    straight_distance = 30
    last_distance = 2.6

    # move to the shark
    await drive(straight_distance)
    await turn(40,LEFT)
    await liftArm()
    await drive(last_distance)

    # hit the shark
    await dropArm()
    await runloop.sleep_ms(500)
    await liftArm()

    # back up
    await drive(-3)
    await dropArm()
    await drive(-9.5, 17)
    await drive(5.2)
    await drive(-2.2)
    await turn_rotations(45, LEFT)
    await drive(25, -10, 700)

async def moveShark():
    """
    Drop the shark off in the habitat, then get the octopus and go to the right side home
    Line up backward, facing the other side of the board. left edge aligned with the boxes.
    Roll robot backwards to preset wheels. Attach pusher attachment and put the octo slide
    on the top of the robot
    """

    await drive(-31,4)
    await drive(10,5)
    await drive(-50,-3)
    await drive(17,5)
    await drive(-17,0)

async def moveOcto():
    """
    Move the octopus to the drop off, then get the plankton sample, head to the angler fish,
    and get back home on the left side of the board
    Line up left side to 1st major line from the left
    """

    # Get to the drop off
    await drive(-19.5)
    await drive(-17,20)
    await drive(-9,0)
    
    # back up to the plankton sample and grab it
    await drive(20,1)
    await drophook()
    
    # pull away to remove the plankton sample
    await drive(-19,-5)
    await drive(-10,4)
    
    # lift the hook and turn to the left
    await lifthook()
    await drive(-3.5,10)
    await turn(73,LEFT)
    
    # drive to the angler fish and turn into the lever
    await drive(-5)
    await turn_rotations(100,RIGHT)

    # get back home
    await drive(-25,11)
    await drive(-28)

async def liftMast():
    """
    Raise the mast of the ship. Flips it all the way up, then pulls it back down
    Line up left side to 2nd major line from the left, facing "north"
    """
    await drophook()
    await drive(20.5)
    await turn_rotations(90,RIGHT)
    await drive(7.8)
    await lifthook(217,102)
    await drive(4.1)
    await drophook(70)
    
    # drive while dropping the hook at the same time
    runloop.run(drive(-3), drophook(70, velocity=100))

    # go back home
    await lifthook(140)
    await drive(-7.8)
    await turn_rotations(90,RIGHT)
    await drive(12)

async def moveCoral():
    """
    Optional mission. Move a coral that is in home, out of home
    Line up close to the edge of home
    """

    await drive(-16,0,500)
    await drive(18,0)

async def main():
    # loaded as #1 - line up to the back, right the right side over the d in education
    #                uses the the flipper attachment
    await whackShark()

    # loaded as #2 - line up in reverse facing the other side of the board.
    #                left side side aligned with the boxes (over the logo).
    #                Roll robot backwards to preset wheels. Attach pusher attachment
    await moveShark()

    # loaded as #3 - line up left side to 1st major line from the left
    await moveOcto()

    # loaded as #4 - line up left side to 2nd major line from the left
    await liftMast()

    # loaded as #5 - line up close to the edge
    await moveCoral()

    raise SystemExit

runloop.run(main())