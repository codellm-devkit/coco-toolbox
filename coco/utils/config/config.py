import os
import re
from typing import Any
from pathlib import Path

import toml


class Config:
    """This is singleton class to hold the configuration information.

    By virtue of it's singleton nature, it can be configured once and used anywhere. Every time a new instance is created,
    we have overriden the `__new__` magic method to return a pre-existing instance of this class.
    """

    _instance = None

    # Save the configuration information across sessions.
    _CONFIG_FILE = Path(os.getenv("COCO_CONFIG")).absolute()

    def __new__(cls):
        """Create a new instance of the config class

        Args:
            conf_data (str, optional): JSON string with the config data. Defaults to None.
            reuse (bool, optional): If this is true, we will load the config from the local raptor.lock file. Defaults to True.

        Returns:
            Config: This class, fully populated.
        """
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)

            # Initial load
            cls._instance._load_config()

        return cls._instance

    def _load_config(self):
        """Load the configurations from the TOML file. If nothing exists, then return an empty dict.

        Args:
            reuse (bool): Reuse forces the use of the lock file.
        """
        # Check to see if the config file has been modified, if so, reload the file.
        if self._CONFIG_FILE.exists():
            with open(self._CONFIG_FILE, "r") as config_file:
                self.config = toml.load(config_file)
                return
        else:
            self.config = {}

    def _expand_env_variables(self, value):
        """Expand environment variables in a given value."""
        if isinstance(value, str):
            # Using regex for various formats like $VAR, env:VAR, ${VAR}
            return re.sub(
                r"(?i)\$(\w+)|env:(\w+)|\$\{(\w+)\}",
                lambda match: os.environ.get(match.group(1) or match.group(2) or match.group(3), match.group(0)),
                value,
            )
        else:
            return value

    def get(self, section: str, key: str) -> Any:
        """Get any value in a given section.

        Args:
            section (str): Configuration section.
            key (str): Configuration key.

        Returns:
            Any: Value associated with that section.
        """
        if section not in self.config:
            value = None
        elif key not in self.config[section]:
            value = None
        else:
            value = self._expand_env_variables(self.config[section][key])

        return value

    def set(self, section: str, key: str, val: Any) -> None:
        """Set any value in a given section.

        Args:
            section (str): Configuration section.
            key (str): Configuration key.
            value (str): Configuration value to be set.
        """
        if section not in self.config:
            self.config[section] = {}

        self.config[section][key] = val
