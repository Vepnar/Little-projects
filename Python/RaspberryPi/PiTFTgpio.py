#!/usr/bin/python3.7
# Author: Arjan de Haan (Vepnar)
# Async button listener for the Adafruit PiTFT 2.2

from contextlib import suppress
from gpiozero import Button
import asyncio

# We first want to make an asynchronous function that will loop forever to capture any button events
async def loop_gpio(buttons):
    # Now we will create the actual part that will loop forever
    # This won't / can't stop until it crashed or it receives an interupt signal 
    while True:
        
        # Now we loop trough all button who are added to the list
        for button, action in buttons.items():

            # Then we check if they are actually pressed and execute their action
            if button.is_pressed:
                await action()

        # And now that part that will make it all asynchronous
        # The asynchronous sleep!
        # In this sleep other pieces of code can do things
        await asyncio.sleep(0.25)

# This function will execute when you press on gpio 17 or the first button on the TFT
async def first_button():
    print('Hey, don\'t touch me I\'m still button 17!')

# This is the same as the function before but for button 22
async def second_button():
    print('You creep! Dont touch me I\'m Button 22!')

# Same for button 23
async def third_button():
    print('What is wrong with you? I\'m button 23')

# And for 27
async def forth_button():
    print('I\'m calling the police! Some human touched me! I\'m at GPIO 27 please help me')


# This will be called when this class isn't imported
if __name__ == '__main__':
    # Now we will a dictionary with the buttons and their actions
    # The GPIO buttons for the PiTFT 2.2 are 17, 22, 23 and 27
    buttons = {
        Button(17) : first_button,
        Button(22) : second_button,
        Button(23) : third_button,
        Button(27) : forth_button
    }

    # Now the real asynchronous part begins :D
    # First we need to create an event loop where our loop will be added
    loop = asyncio.get_event_loop()
    print('Capture started..')

    # Now we need to add our loop_gio function to the event loop
    # And let it run until its done.
    # Also supress() is a cleaner way to ignore a kind of exception for example keyboardinterrupt
    with suppress(KeyboardInterrupt):
        loop.run_until_complete(loop_gpio(buttons))
    
    # Close our asynchronous loop
    loop.close()
