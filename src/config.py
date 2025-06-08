import json
import os

DEFAULT_CONFIG = {
    "supported_image_types": [".jpg", ".jpeg", ".png", ".bmp", ".gif"],
    "supported_video_types": [".mp4", ".mov", ".avi"],
    "thumbnail_size": 128,
    "default_directory": os.path.expanduser("~")
}

CONFIG_PATH = os.path.expanduser("~/.photo_video_manager_config.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                config = json.load(f)
                # Ensure new keys are present
                for k, v in DEFAULT_CONFIG.items():
                    if k not in config:
                        config[k] = v
                return config
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(config):
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Failed to save config: {e}")