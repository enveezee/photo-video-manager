from config import load_config, DEFAULT_CONFIG
import os

config = load_config()


def is_image_file(file_path):
    image_extensions = config.get("supported_image_types", DEFAULT_CONFIG["supported_image_types"])
    return any(file_path.lower().endswith(ext) for ext in image_extensions)


def is_video_file(file_path):
    video_extensions = config.get("supported_video_types", DEFAULT_CONFIG["supported_video_types"])
    return any(file_path.lower().endswith(ext) for ext in video_extensions)


def validate_file_path(file_path):
    return os.path.isfile(file_path)


def get_file_extension(file_path):
    return os.path.splitext(file_path)[1]