import gi
from Note import Note

gi.require_version("Gtk", "3.0")
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, GdkPixbuf

from NoteFileIO import NoteFileIO

icon = "edit-copy"

class NotePicker(Gtk.Window):
    def __init__(self):
        super().__init__()

        self.note_file_io = NoteFileIO()

        store = self.get_files_store()
        notepicker_window = self.setup_notepicker_window(store)

        self.add(notepicker_window)


    # TODO: Refresh the filesystem by adding newly added notes into it, either by adding it to the store on add
    # OR by reloading the entire thing by using the "map-event" signal from this window
    def get_files_store(self):
        note_files = self.note_file_io.get_note_files()

        liststore = Gtk.ListStore(GdkPixbuf.Pixbuf, str)

        pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 64, 0)
        for note_file in note_files:
            liststore.append([pixbuf, note_file.stem]) # FIXME: oder .split(".")[0]
        
        return liststore
    

    def setup_notepicker_window(self, liststore):
        main_vbox = Gtk.Box()
        main_vbox.set_orientation(Gtk.Orientation.VERTICAL)
        main_vbox.set_spacing(2)

        icon_view = Gtk.IconView()
        icon_view.set_model(liststore)
        icon_view.set_pixbuf_column(0)
        icon_view.set_text_column(1)
        icon_view.set_selection_mode(Gtk.SelectionMode.SINGLE)
        icon_view.set_activate_on_single_click(False)
        icon_view.connect("item-activated", self.on_open_selection_clicked)

        bbar = Gtk.ButtonBox()
        bbar.set_orientation(Gtk.Orientation.HORIZONTAL)
        bbar.set_spacing(2)
        bbar.set_layout(Gtk.ButtonBoxStyle.SPREAD)

        open_button = Gtk.Button(label="Open")
        create_button = Gtk.Button(label="Create")
        exit_button = Gtk.Button(label="Exit")
        open_button.connect("clicked", self.on_open_button_clicked, icon_view)
        create_button.connect("clicked", lambda _ : self.open_note_window())
        bbar.add(open_button)
        bbar.add(create_button)

        main_vbox.pack_start(icon_view, True, True, 20)
        main_vbox.pack_start(bbar, False, False, 20)

        return main_vbox
    
    
    def on_open_button_clicked(self, _, icon_view):
        if len(icon_view.get_selected_items()) == 0:
            return
        
        tree_path = icon_view.get_selected_items()[0]
        model = icon_view.get_model()
        # since we always only have one selected element
        row_number = tree_path.get_indices()[0]
        note_title = model[row_number][1]
        note_content = self.note_file_io.read_note(note_title)
        self.open_note_window(note_title, note_content)


    def on_open_selection_clicked(self, icon_view, tree_path):
        model = icon_view.get_model()
         # since we always only have one selected element
        row_number = tree_path.get_indices()[0]
        note_title = model[row_number][1]
        note_content = self.note_file_io.read_note(note_title)
        self.open_note_window(note_title, note_content)
    

    def open_note_window(self, note_title = "", note_content = ""):
        # TODO: Make note_title selectable when creating new note
        if note_title == "":
            note_title = "Unnamed"
        note_window = Note(self, note_title, note_content)
        note_window.connect("destroy", lambda window : self.show())
        note_window.show_all()
        self.hide()
        