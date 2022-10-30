from configparser import ConfigParser
from typing import Optional, Dict, Any


def read_config(section: str) -> Optional[Dict[str, Any]]:
    config = ConfigParser()
    config.read('config.ini')

    if section not in config.sections():
        return None

    return config[section]
