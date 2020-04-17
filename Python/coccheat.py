"""A simple bot for cheating on clash of clans.

Things to keep in mind:
    This was made for a 1920x1080 screen.
    Clash of clans swipe movements are a bit random.
    This might be outdated
    This requires an active ADB connection
"""
import subprocess
from time import sleep


class CocControler:
    """Handle all motion of the bot"""

    def __init__(self, x=0, y=0, screen_x=1920, screen_y=1080, offset=0.15):
        self._x = x
        self._y = y
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.offset = offset

    def _small_y(self, y):
        """Set tiny steps on the Y axis"""
        xcenter = int(self.screen_x / 2)
        ycenter = int(self.screen_y / 2)

        # This is the safest way of moving the user around.
        # Keep in mind: THE MOVEMENTS HAVE AN OFFSET.
        self._swipe(xcenter, ycenter, xcenter, ycenter+y)
        sleep(0.3)

    def _small_x(self, x):
        """The same as before but for the X axis"""
        xcenter = int(self.screen_x / 2)
        ycenter = int(self.screen_y / 2)
        self._swipe(xcenter, ycenter, xcenter+x, ycenter)
        sleep(0.3)

    def _move_y(self, y):
        """Move Y to a certain location"""
        offset_min = int(self.screen_y * self.offset)

        # Don't move the cursor
        if y == self._y:
            pass

        elif y == 0:
            # Don't use this to return to the 0,0 location
            c = self._y
            self._y = 0
            for _ in range(c // offset_min):
                self._small_y(offset_min)
            self._small_y(c % offset_min)

        elif y < self._y:
            c = y - self._y
            self._y -= y
            for _ in range(c // offset_min):
                self._small_y(offset_min)
            self._small_y(c % offset_min)

        elif y > self._y:
            c = self._y + y
            self._y += y
            for _ in range(c // offset_min):
                self._small_y(- offset_min)
            self._small_y(-(c % offset_min))

    def _move_x(self, x):
        """Move Y to a certain location"""
        offset_min = int(self.screen_x * self.offset)

        # When no movement is required
        if x == self._x:
            pass

        elif x == 0:
            c = self._x
            self._x = 0
            for _ in range(c // offset_min):
                self._small_x(offset_min)
            self._small_x(c % offset_min)

        elif x < self._x:
            c = x - self._x
            self._x -= x
            for _ in range(c // offset_min):
                self._small_x(offset_min)
            self._small_x(c % offset_min)

        elif x > self._x:
            c = self._x + x
            self._x += x
            for _ in range(c // offset_min):
                self._small_x(-offset_min)
            self._small_x(-(c % offset_min))

    def _swipe(self, start_x, start_y, end_x, end_y):
        """Execute swipe command.

        Don't run this command yourself as it will not update the current X, Y location
        """
        subprocess.Popen(
            f'adb shell input swipe {start_x} {start_y} {end_x} {end_y}', shell=True)
        sleep(0.5)

    def _click(self, x=None, y=None):
        """Click on a certain point on the screen
        
        This will not first go to the given location
        """
        if x is None: # Set click location in the center of the screen
            x = int(self.screen_x / 2)
        if y is None:
            y = int(self.screen_y / 2)
        subprocess.Popen(
            f'adb shell input tap {x} {y}', shell=True)
        sleep(0.3)

    def swipe(self, x, y):
        """Move to a given location

        always first move on the X axis
        The bot could click on the boat and break the whole bot
        """
        self._move_x(x)
        self._move_y(y)

    def reset(self, r=1):
        """Use this to reset the X, Y axis.
        
        Don't use swipe(0,0) because all movements have a offset
        """
        xoffset_min = int(self.screen_x * self.offset)
        xoffset_max = self.screen_x - xoffset_min
        yoffset_min = int(self.screen_y * self.offset)
        yoffset_max = self.screen_y - yoffset_min

        # To make sure get in the center
        for _ in range(r):
            self._swipe(xoffset_min, yoffset_min, xoffset_max, yoffset_max)
            sleep(0.3)

        # unselect everything
        self._click(x=300, y=100)
        self._x = 0
        self._y = 0

    def click(self, x, y):
        """Go to a location and click in the middle"""
        self.swipe(x, y)
        self._click()

def main():
    """Values for my village"""
    coc = CocControler()

    while True:
        coc.reset(r=2)
        coc.click(1200, 600)
        coc.reset(r=1)
        coc.click(1000, 1300)
        coc.reset(r=2)
        coc.click(1400, 1300)
        coc.reset(r=2)
        sleep(10)

if __name__ == '__main__':
    main()
