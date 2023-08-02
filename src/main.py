import gi

from note_picker import NotePicker
from note_file_io import NoteFileIO

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def main():
    NoteFileIO.init_files()
    note_picker = NotePicker()
    note_picker.connect("destroy", Gtk.main_quit)
    note_picker.set_position(Gtk.WindowPosition.CENTER)
    note_picker.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
