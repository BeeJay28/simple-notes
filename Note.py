import gi

from NoteFileIO import NoteFileIO

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango

class Note(Gtk.Window):
    def __init__(self, parent, note_title, note_content = ""):
        super().__init__()

        self.parent = parent
        self.note_title = note_title
        self.note_file_io = NoteFileIO()
        self.set_transient_for(self.parent)
        self.set_destroy_with_parent(True)

        self.setup_note_window(note_content)


    def setup_note_window(self, note_content):
        self.setup_headerbar()

        self.window_vbox = Gtk.Box()
        self.window_vbox.set_orientation(Gtk.Orientation.VERTICAL)

        self.setup_textview(note_content)

        self.setup_buttons()

        self.window_vbox.pack_start(self.title_entry, True, True, 20)
        self.window_vbox.pack_start(self.scrolled_text_window, True, True, 20)
        self.window_vbox.pack_start(self.bbar_hbox, False, False, 20)

        self.set_titlebar(self.headerbar)
        self.add(self.window_vbox)


    def setup_buttons(self):
        self.bbar_hbox = Gtk.ButtonBox()
        self.bbar_hbox.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.bbar_hbox.set_layout(Gtk.ButtonBoxStyle.SPREAD)

        self.save_button = Gtk.Button(label="Save")
        self.close_button = Gtk.Button(label="Close")
        self.save_button.connect("clicked", self.save_note)
        self.close_button.connect("clicked", self.show_confirmation_dialog)
        self.add_keybinding_for_saving()

        self.bbar_hbox.pack_start(self.save_button, True, False, 20)
        self.bbar_hbox.pack_start(self.close_button, True, False, 100)


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


    def show_confirmation_dialog(self, _):
        """'on_yes' should be a function that runs if the confirmation dialog is confirmed"""
        dialog = Gtk.MessageDialog(
            parent=self,
            flags=Gtk.DialogFlags.MODAL,
            type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            message_format="Are you sure?"
        )

        dialog.connect("response", self.on_dialog_confirmation_response)
        dialog.show()


    def on_dialog_confirmation_response(self, dialog, response_id, on_yes):
        self.parent.show()
        dialog.destroy()
        self.destroy()


    def setup_textview(self, note_content):
        self.title_entry = Gtk.Entry()
        self.title_entry.set_editable(True)
        self.title_entry.set_text(self.note_title)

        # attr_list = Pango.AttrList()
        # font_desc = Pango.FontDescription()
        # font_desc.set_family("Arial")
        # font_desc.set_size(20)
        # font_desc.set_weight(Pango.Weight.BOLD)
        # attr_font_desc = Pango.AttrFontDesc().new(font_desc)
        # attr_list.insert(attr_font_desc)
        # self.title_entry.set_attributes(attr_list)

        self.scrolled_text_window = Gtk.ScrolledWindow()
        self.scrolled_text_window.set_size_request(200, 400)
        # TODO: Add "(edited)" sub_title when buffer is modified

        self.text_view = Gtk.TextView()
        self.text_view.set_wrap_mode(Gtk.WrapMode.NONE)
        self.text_view.set_top_margin(10)
        self.text_view.set_left_margin(10)
        buffer = self.text_view.get_buffer()
        buffer.set_text(note_content, -1)
        buffer.connect("modified-changed", self.show_modified_in_header)

        # Focus on textView AFTER all widgets are created and mapped properly
        self.connect("realize", lambda window : self.text_view.grab_focus())

        self.scrolled_text_window.add(self.text_view)

    
    def show_modified_in_header(self, buffer):
        if buffer.get_modified():
            self.headerbar.set_subtitle("modified")
        else:
            self.headerbar.set_subtitle("asd")


    def setup_headerbar(self):
        self.headerbar = Gtk.HeaderBar()
        self.headerbar.set_title(self.note_title)
        self.headerbar.set_show_close_button(True)
        

    def save_note(self, _):
        buffer = self.text_view.get_buffer()
        if not buffer.get_modified():
            return
        note_content = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True)
        self.note_file_io.save_note(self.note_title, note_content)
        buffer.set_modified(False)