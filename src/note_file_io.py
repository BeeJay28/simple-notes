from pathlib import Path

class NoteFileIO():
    """Naming policy: filename = {note_title}.pln"""
    _NOTES_DIR_NAME = "simple_notes"
    _notes_path = None
    
    @classmethod
    def init_files(cls):
        notes_path = Path.resolve(Path.home() / cls._NOTES_DIR_NAME)
        if not Path.exists(notes_path):
            Path.mkdir(notes_path)
        cls._notes_path = notes_path

    
    def save_note(self, note_title, note_content):
        file_path = self._notes_path.joinpath(Path(f"{note_title}.pln"))
        with file_path.open("w", encoding="UTF-8") as file:
            # TODO: Use the return value to display success or failure
            is_success = file.write(note_content) != 0
        return is_success
    
    def get_note_files(self):
        return self._notes_path.glob("*.pln")
    
    def read_note(self, note_title):
        file_path = self._notes_path.joinpath(Path(f"{note_title}.pln"))
        with open(file_path, "r", encoding="UTF-8") as file:
            note = file.read()
        return note

    def rename_note(self, old_note_title, new_note_title):
        old_file_path = self._notes_path.joinpath(Path(f"{old_note_title}.pln"))
        if not old_file_path.exists():
            return
        new_file_path = self._notes_path.joinpath(Path(f"{new_note_title}.pln"))
        old_file_path.rename(new_file_path)