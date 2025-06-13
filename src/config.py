import json
import os

DEFAULT_CONFIG = {
    "supported_image_types": [".avif", ".bmp", ".gif", ".heic", ".jpg", ".jpeg", ".png", ".tiff", ".webp"],
    "supported_video_types": [".3gp", ".avi", ".flv", ".m4v",  ".mkv", ".mov", ".mp4", ".mpg", ".mpeg",  ".wmv"],
    "thumbnail_size": 128,
    "default_directory": os.path.expanduser("~")
}

CONFIG_PATH = os.path.expanduser("~/.config/pixelporter/p3_config.json")
_config_cache = None

def load_config():
    global _config_cache
    if _config_cache is not None:
        return _config_cache
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                config = json.load(f)
                # Ensure new keys are present
                for k, v in DEFAULT_CONFIG.items():
                    if k not in config:
                        config[k] = v
                _config_cache = config
                return config
        except Exception:
            pass
    else:
        os.makedirs(os.path.dirname(CONFIG_PATH))
    _config_cache = DEFAULT_CONFIG.copy()
    return _config_cache

def save_config(config=None):
    global _config_cache
    if config is None:
        config = _config_cache
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)
        _config_cache = config
    except Exception as e:
        print(f"Failed to save config: {e}")

def set_config_value(key, value):
    config = load_config()
    config[key] = value
    save_config(config)