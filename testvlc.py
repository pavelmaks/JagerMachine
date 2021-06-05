import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#gi.require_version('GdkX11', '3.0')
#from gi.repository import GdkX11

import vlc

MRL = "./video/1.mp4"  # File to play
WIDTH = 300
HEIGHT = 300


class ApplicationWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Python-Vlc Media Player")
        self.player_paused = False
        self.is_player_active = False
        self.connect("destroy", Gtk.main_quit)

    def show(self):
        self.show_all()

    def setup_objects_and_events(self):

        self.draw_area = Gtk.DrawingArea()
        self.draw_area.set_size_request(WIDTH, HEIGHT)

        self.draw_area.connect("realize", self._realized)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.vbox)
        self.vbox.pack_start(self.draw_area, True, True, 0)


    def _realized(self, widget, data=None):
        self.vlcInstance = vlc.Instance("--no-xlib", "--input-repeat=-1")
        self.player = self.vlcInstance.media_player_new()
        win_id = widget.get_window().get_xid()
        self.player.set_xwindow(win_id)
        self.player.set_mrl(MRL)
        self.player.play()
        self.playback_button.set_image(self.pause_image)
        self.is_player_active = True


if __name__ == '__main__':
        window = ApplicationWindow()
        window.setup_objects_and_events()
        window.show()
        Gtk.main()
        print(1)
        window.player.stop()
        print(2)
        window.vlcInstance.release()
        print(3)