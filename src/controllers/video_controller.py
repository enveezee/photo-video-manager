class VideoController:
    def __init__(self, video_model, video_editor):
        self.video_model = video_model
        self.video_editor = video_editor

    def load_video(self, file_path):
        self.video_model.load(file_path)

    def apply_edits(self, edits):
        self.video_editor.apply_edits(self.video_model, edits)

    def save_changes(self, output_path):
        self.video_model.save(output_path)