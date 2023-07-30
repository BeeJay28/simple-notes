from pathlib import Path

class NoteFileIO():
    """Naming policy: filename = {note_title}.pln"""
    _notes_path = Path("/home/artur/projects/simple_notes/notes/")

    @property
    def notes_path(self):
        return self._notes_path
    
    def save_note(self, note_title, note_content):
        file_path = self.notes_path.joinpath(Path(f"{note_title}.pln"))
        with open(file_path, "w", encoding="UTF-8") as file:
            # TODO: Use the return value to display success or failure
            is_success = file.write(note_content) != 0
        return is_success
    
    def get_note_files(self):
        return self.notes_path.glob("*.pln")
    
    def read_note(self, note_title):
        file_path = self.notes_path.joinpath(Path(f"{note_title}.pln"))
        with open(file_path, "r", encoding="UTF-8") as file:
            note = file.read()
        return note