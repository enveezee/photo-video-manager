class XMLHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_metadata(self):
        import xml.etree.ElementTree as ET
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            metadata = {}
            for child in root:
                metadata[child.tag] = child.text
            return metadata
        except Exception as e:
            print(f"Error reading XML metadata: {e}")
            return None

    def write_metadata(self, metadata):
        import xml.etree.ElementTree as ET
        root = ET.Element("metadata")
        for key, value in metadata.items():
            child = ET.SubElement(root, key)
            child.text = str(value)
        tree = ET.ElementTree(root)
        try:
            tree.write(self.file_path)
        except Exception as e:
            print(f"Error writing XML metadata: {e}")