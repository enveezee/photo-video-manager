class VideoEditor:
    def __init__(self, video):
        self.video = video
        self.edits = []

    def trim(self, start_time, end_time):
        self.edits.append({'action': 'trim', 'start': start_time, 'end': end_time})

    def add_effect(self, effect):
        self.edits.append({'action': 'add_effect', 'effect': effect})

    def adjust_properties(self, properties):
        self.edits.append({'action': 'adjust_properties', 'properties': properties})

    def apply_edits(self):
        # Logic to apply edits to the video
        pass

    def revert_edits(self):
        # Logic to revert the last edit
        if self.edits:
            self.edits.pop()

    def save_edits(self, handler):
        # Logic to save edits using the provided handler (XML or JSON)
        pass