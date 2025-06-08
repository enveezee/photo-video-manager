class PhotoController:
    def __init__(self, photo_model, ui):
        self.photo_model = photo_model
        self.ui = ui

    def load_photo(self, file_path):
        self.photo_model.load(file_path)
        self.update_ui_with_photo()

    def apply_edits(self, edits):
        self.photo_model.apply_edits(edits)
        self.update_ui_with_photo()

    def save_changes(self, save_path):
        self.photo_model.save(save_path)

    def update_ui_with_photo(self):
        # Update the UI with the current photo data
        self.ui.display_photo(self.photo_model)