#!/usr/bin/python
import time
import json
from mopidy import Mopidy
from scrollphathd import ScrollpHatHD

def main():

    # Create objects
    mopidy = Mopidy()
    screen = ScrollpHatHD()

    while True:
        screen.show()

        time.sleep(0.1)

    return


if __name__=="__main__":
    main()

