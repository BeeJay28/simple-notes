import gi

from NoteFileIO import NoteFileIO

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class Note(Gtk.Window):
    def __init__(self, note_title, note_content = ""):
        super().__init__()

        self.note_file_io = NoteFileIO()

        self.note_title = note_title

        self.set_headerbar()

        self.window_vbox = Gtk.Box()
        self.window_vbox.set_orientation(Gtk.Orientation.VERTICAL)

        self.set_textview(note_content)

        self.bbar_hbox = Gtk.ButtonBox()
        self.bbar_hbox.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.bbar_hbox.set_layout(Gtk.ButtonBoxStyle.SPREAD)

        self.window_vbox.pack_start(self.scrolled_text_window, True, True, 20)
        self.window_vbox.pack_start(self.bbar_hbox, False, False, 20)

        self.set_buttons()
        self.bbar_hbox.pack_start(self.save_button, True, False, 20)
        self.bbar_hbox.pack_start(self.close_button, True, False, 100)

        self.set_titlebar(self.headerbar)
        self.add(self.window_vbox)

    def set_buttons(self):
        self.save_button = Gtk.Button(label="Save")
        self.close_button = Gtk.Button(label="Cancel")
        self.save_button.connect("clicked", self.save_note)
        self.close_button.connect("clicked", self.show_confirmation_dialog, lambda : self.destroy())
        self.add_keybinding_for_saving()

    def add_keybinding_for_saving(self):
        accel_group = Gtk.AccelGroup()
        self.add_accel_group(accel_group)
        self.save_button.add_accelerator(
            "activate",
            accel_group,
            Gdk.keyval_from_name("S"),
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE
        )

    def show_confirmation_dialog(self, _, on_yes = lambda : None):
        """'on_yes' should be a function that runs if the confirmation dialog is confirmed"""
        dialog = Gtk.MessageDialog(
            parent=self,
            flags=Gtk.DialogFlags.MODAL,
            type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            message_format="Are you sure?"
        )

        dialog.connect("response", self.on_dialog_confirmation_response, on_yes)
        dialog.show()

    def on_dialog_confirmation_response(self, dialog, response_id, on_yes):
        dialog.destroy()

        if response_id == Gtk.ResponseType.YES:
            on_yes()

    def set_textview(self, note_content):
        self.scrolled_text_window = Gtk.ScrolledWindow()
        self.scrolled_text_window.set_size_request(200, 400)
        self.text_view = Gtk.TextView()
        self.text_view.set_wrap_mode(Gtk.WrapMode.NONE)
        self.text_view.set_top_margin(10)
        self.text_view.set_left_margin(10)
        self.text_view.get_buffer().set_text(note_content, -1)
        self.scrolled_text_window.add(self.text_view)

    def set_headerbar(self):
        self.headerbar = Gtk.HeaderBar()
        self.headerbar.set_title(self.note_title)
        self.headerbar.set_show_close_button(True)

    def save_note(self, _):
        buffer = self.text_view.get_buffer()
        note_content = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True)
        self.note_file_io.save_note(self.note_title, note_content)