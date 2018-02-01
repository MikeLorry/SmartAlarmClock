#!/usr/bin/python
import time
import json
from mopidy import Mopidy
from screen import ScrollpHatHD
from switches import Switches

def main():

    # Create objects
    mopidy = Mopidy()
    screen = ScrollpHatHD()
    switches = Switches()


    while True:
        screen.show()
        switches.check_input()

        time.sleep(0.05)

    return


if __name__=="__main__":
    main()

