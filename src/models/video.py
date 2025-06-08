class Video:
    def __init__(self, file_path):
        self.file_path = file_path
        self.duration = 0  # Duration in seconds
        self.metadata = {}

    def load(self):
        # Logic to load video file and extract metadata
        pass

    def save(self):
        # Logic to save video file
        pass

    def edit(self, edits):
        # Logic to apply edits to the video
        pass

    def get_duration(self):
        # Logic to return the duration of the video
        return self.duration

    def set_duration(self, duration):
        self.duration = duration

    def get_metadata(self):
        return self.metadata

    def set_metadata(self, metadata):
        self.metadata = metadata