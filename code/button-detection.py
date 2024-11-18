# Uses Hub OS 1.6.62 with LEGO Education version 3.4.3
import runloop
from hub import button
from hub import light_matrix

image_index = 1

def udpate_image():
    global image_index
    if image_index > 67:
        image_index = 1
    elif image_index < 1:
        image_index = 67
    light_matrix.show_image(image_index)
    print("Displaying image number ", image_index)

async def main():
    """
    Press the left or right buttons to cycle through the images.
    Press the center button to exit.
    """
    global image_index
    light_matrix.show_image(image_index)
    right_is_down = False
    left_is_down = False
    while True:
        if not button.pressed(button.RIGHT):
            # recognize release of button
            right_is_down = False
        if not button.pressed(button.LEFT):
            # recognize release of button
            left_is_down = False
        if button.pressed(button.LEFT) and not left_is_down:
            # detect initial press
            left_is_down = True
            image_index -= 1
            udpate_image()
        elif button.pressed(button.RIGHT) and not right_is_down:
            # detect initial press
            right_is_down = True
            image_index += 1
            udpate_image()

runloop.run(main())
