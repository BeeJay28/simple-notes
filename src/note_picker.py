import gi
from note import Note

gi.require_version("Gtk", "3.0")
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, GdkPixbuf

from note_file_io import NoteFileIO

icon = "edit-copy"

class NotePicker(Gtk.Window):
    def __init__(self):
        super().__init__()

        self.note_file_io = NoteFileIO()

        store = self.get_files_store()
        notepicker_window = self.setup_notepicker_window(store)

        self.add(notepicker_window)
        self.set_size_request(200, 200)
        self.set_default_size(800, 640)


    # Must not be called before finishing initial setup
    def reload(self):
        refreshed_store = self.get_files_store()
        self.icon_view.set_model(refreshed_store)


    def get_files_store(self):
        note_files = self.note_file_io.get_note_files()

        liststore = Gtk.ListStore(GdkPixbuf.Pixbuf, str)

        pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 64, 0)
        for note_file in note_files:
            liststore.append([pixbuf, note_file.stem])
        
        return liststore
    
    def refresh_store(self, note_window):
        store = self.get_files_store()
        self.icon_view.set_model(store)

    def setup_notepicker_window(self, liststore):
        main_vbox = Gtk.Box()
        main_vbox.set_orientation(Gtk.Orientation.VERTICAL)
        main_vbox.set_spacing(2)

        self.icon_view = Gtk.IconView()
        self.icon_view.set_model(liststore)
        self.icon_view.set_pixbuf_column(0)
        self.icon_view.set_text_column(1)
        self.icon_view.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.icon_view.set_activate_on_single_click(False)
        self.icon_view.connect("item-activated", self.on_open_selection_clicked)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(self.icon_view)

        bbar = Gtk.ButtonBox()
        bbar.set_orientation(Gtk.Orientation.HORIZONTAL)
        bbar.set_spacing(2)
        bbar.set_layout(Gtk.ButtonBoxStyle.SPREAD)

        open_button = Gtk.Button(label="Open")
        delete_button = Gtk.Button(label="Delete")
        create_button = Gtk.Button(label="Create")
        open_button.connect("clicked", self.on_open_button_clicked, self.icon_view)
        delete_button.connect("clicked", self.on_delete_button_clicked, self.icon_view)
        create_button.connect("clicked", lambda button : self.open_new_note_window())
        bbar.add(open_button)
        bbar.add(delete_button)
        bbar.add(create_button)

        main_vbox.pack_start(scrolled_window, True, True, 20)
        main_vbox.pack_start(bbar, False, False, 20)

        return main_vbox
    
    
    def on_open_button_clicked(self, button, icon_view):
        if len(icon_view.get_selected_items()) == 0:
            return
        
        tree_path = icon_view.get_selected_items()[0]
        self.open_existing_note(icon_view, tree_path)


    def on_open_selection_clicked(self, icon_view, tree_path):
        self.open_existing_note(icon_view, tree_path)


    def open_existing_note(self, icon_view, tree_path):
        note_title = self.get_note_title(icon_view, tree_path)
        note_content = self.note_file_io.read_note(note_title)
        self.open_existing_note_window(note_title, note_content)

    def get_note_title(self, icon_view, tree_path):
        model = icon_view.get_model()
        # since we always only have one selected element
        row_number = tree_path.get_indices()[0]
        note_title = model[row_number][1]
        return note_title

    def on_delete_button_clicked(self, button, icon_view):
        if len(icon_view.get_selected_items()) == 0:
            return
        
        tree_path = icon_view.get_selected_items()[0]
        note_title = self.get_note_title(icon_view, tree_path)

        dialog = Gtk.MessageDialog(
            text=f"Are you sure you want to delete {note_title}?",
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.YES_NO
        )
        dialog.format_secondary_text("This action cannot be undone!")
        dialog.connect("response", self.on_dialog_confirmation_response, note_title)
        dialog.run() # also turns dialog modal
        dialog.destroy()
        
    def on_dialog_confirmation_response(self, dialog, response_id, note_title):
        if response_id == Gtk.ResponseType.YES:
            self.note_file_io.delete_note(note_title)
            self.reload()


    def open_new_note_window(self):
        note_window = Note(self, "Unnamed", "")
        note_window.connect("destroy", lambda window : self.show())
        note_window.show_all()
        self.hide()

    def open_existing_note_window(self, note_title, note_content):
        note_window = Note(self, note_title, note_content)
        note_window.connect("destroy", lambda window : self.show())
        note_window.show_all()
        self.hide()
        