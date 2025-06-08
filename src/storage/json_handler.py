class JSONHandler:
    import json

    def __init__(self, file_path):
        self.file_path = file_path

    def read_metadata(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading JSON metadata: {e}")
            return None

    def write_metadata(self, metadata):
        try:
            with open(self.file_path, 'w') as file:
                json.dump(metadata, file, indent=4)
        except IOError as e:
            print(f"Error writing JSON metadata: {e}")