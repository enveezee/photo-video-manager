class PhotoEditor:
    def __init__(self, photo):
        self.photo = photo

    def apply_filter(self, filter_type):
        # Logic to apply the specified filter to the photo
        pass

    def crop(self, x, y, width, height):
        # Logic to crop the photo to the specified dimensions
        pass

    def adjust_properties(self, brightness=None, contrast=None, saturation=None):
        # Logic to adjust the photo properties
        pass

    def save_edits(self, metadata_handler):
        # Logic to save the edits using the provided metadata handler
        pass

    def revert_edits(self):
        # Logic to revert the edits made to the photo
        pass