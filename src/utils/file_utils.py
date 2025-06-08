def is_image_file(file_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    return any(file_path.lower().endswith(ext) for ext in image_extensions)

def is_video_file(file_path):
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
    return any(file_path.lower().endswith(ext) for ext in video_extensions)

def validate_file_path(file_path):
    import os
    return os.path.isfile(file_path)

def get_file_extension(file_path):
    import os
    return os.path.splitext(file_path)[1]