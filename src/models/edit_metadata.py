class EditMetadata:
    def __init__(self):
        self.edits = []

    def apply_edit(self, edit):
        self.edits.append(edit)

    def revert_edit(self):
        if self.edits:
            self.edits.pop()

    def copy_edits(self):
        return self.edits.copy()