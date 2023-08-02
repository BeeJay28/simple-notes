import gi

from NotePicker import NotePicker

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def main():
    note_picker = NotePicker()
    note_picker.connect("destroy", Gtk.main_quit)
    note_picker.set_position(Gtk.WindowPosition.CENTER)
    note_picker.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
