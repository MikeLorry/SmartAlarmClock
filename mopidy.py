#!/usr/bin/python
import requests
import json

class Mopidy:
    "Mopidy class to allow interaction with mopidy server"

    # Default values
    mopidy_url = "http://127.0.0.1:6680/mopidy/rpc"
    default_playlist = "spotify:user:mikelorry:playlist:0MoNuAV4CztP0gUtFVwovv"
    default_vol = 30

    def __init__(self):
        # Set mopidy URL
        self.url = Mopidy.mopidy_url
        # Set volume to default
        self.current_vol = Mopidy.default_vol
        self.set_volume(self.current_vol)

        # Loading default playlist
        self.current_playlist = Mopidy.default_playlist
        self.load_playlist()

        # Set startup status
        self.status = "pause"
        return

    def set_volume(self, vol):
        self.post_mopidy("mixer.set_volume", {"volume": vol})
        self.current_vol = vol
        print "Mopidy volume: " + str(self.current_vol)
        return

    def volume_up(self):
        new_vol = 0
        if self.current_vol >= 95:
            new_vol = 100
        elif self.current_vol < 95:
            new_vol = self.current_vol + 5
        self.set_volume(new_vol)
        return self.current_vol

    def volume_down(self):
        new_vol = 0
        if self.current_vol <= 5:
            new_vol = 0
        elif self.current_vol > 5:
            new_vol = self.current_vol - 5
        self.set_volume(new_vol)
        return self.current_vol

    def load_playlist(self):
        self.post_mopidy("tracklist.add", {"uri": self.current_playlist})
        print "Mopidy playlist: " + self.current_playlist
        return

    def ctl(self, action):
        if self.status == "pause" and action == "play":
            self.post_mopidy("playback.play")
        elif self.status == "play" and action == "play":    
            self.post_mopidy("playback.pause")
        else:
            self.post_mopidy("playback."+action)
        return

    def post_mopidy(self, method, params = {}):
        payload =  {
            "method": "core." + method ,
            "jsonrpc": "2.0",
            "params": params,
            "id": 1
            }
        r = requests.post(self.url, data = json.dumps(payload))
        return

