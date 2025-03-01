# leetcode_local/config/manager.py
import os
import toml
from pathlib import Path
import shutil

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'default_config.toml')

class ConfigManager:
    """
    Manages configuration for the LeetCode local practice tool
    """
    def __init__(self, config_path=None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to the custom config file. If None, will look for
                         leetcode-local.toml in the current directory or user's home directory.
        """
        self.config = None
        self.config_path = None
        
        # Try to find config file
        if config_path and os.path.exists(config_path):
            self.config_path = config_path
        else:
            # Look in current directory
            if os.path.exists('leetcode-local.toml'):
                self.config_path = 'leetcode-local.toml'
            # Look in user's home directory
            elif os.path.exists(os.path.expanduser('~/.leetcode-local.toml')):
                self.config_path = os.path.expanduser('~/.leetcode-local.toml')
        
        # Load config or use defaults
        if self.config_path:
            self.load_config()
        else:
            self.load_default_config()
    
    def load_config(self):
        """Load configuration from the config file."""
        try:
            self.config = toml.load(self.config_path)
            print(f"Loaded configuration from {self.config_path}")
        except Exception as e:
            print(f"Error loading config file: {e}")
            self.load_default_config()
    
    def load_default_config(self):
        """Load the default configuration."""
        try:
            if os.path.exists(DEFAULT_CONFIG_PATH):
                self.config = toml.load(DEFAULT_CONFIG_PATH)
            else:
                # Hardcoded defaults as fallback
                self.config = {
                    "paths": {
                        "solutions_dir": "solutions",
                        "test_cases_dir": "test_cases"
                    },
                    "preferences": {
                        "default_difficulty": "ALL",
                        "default_category": "ALL",
                        "template_style": "detailed",
                        "page_size": 10
                    },
                    "testing": {
                        "verbose": True,
                        "time_solutions": True,
                        "timeout": 5
                    },
                    "problems": {
                        "include_locked": False,
                        "color_easy": "green",
                        "color_medium": "yellow",
                        "color_hard": "red"
                    },
                    "leetcode75": {
                        "restrict_to_leetcode75": True
                    }
                }
            print("Loaded default configuration")
        except Exception as e:
            print(f"Error loading default config: {e}")
            raise
    
    def get(self, section, key, default=None):
        """
        Get a configuration value.
        
        Args:
            section: The configuration section
            key: The configuration key
            default: Default value if the key doesn't exist
            
        Returns:
            The configuration value or default
        """
        try:
            return self.config[section][key]
        except KeyError:
            return default
    
    def set(self, section, key, value):
        """
        Set a configuration value.
        
        Args:
            section: The configuration section
            key: The configuration key
            value: The value to set
        """
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
    
    def save(self, path=None):
        """
        Save the configuration to a file.
        
        Args:
            path: Path to save to. If None, uses the current config path
                 or creates one in the user's home directory.
        """
        if path:
            save_path = path
        elif self.config_path:
            save_path = self.config_path
        else:
            save_path = os.path.expanduser('~/.leetcode-local.toml')
        
        try:
            with open(save_path, 'w') as f:
                toml.dump(self.config, f)
            print(f"Configuration saved to {save_path}")
            self.config_path = save_path
        except Exception as e:
            print(f"Error saving configuration: {e}")
            raise
    
    def create_default_config(self, path):
        """
        Create a default configuration file at the specified path.
        
        Args:
            path: Path to create the config file
        """
        if os.path.exists(DEFAULT_CONFIG_PATH):
            shutil.copy(DEFAULT_CONFIG_PATH, path)
        else:
            # Create from hardcoded defaults
            with open(path, 'w') as f:
                toml.dump(self.config, f)
        print(f"Created default configuration at {path}")

# Create a singleton instance
config = ConfigManager()

def get_config():
    """Get the global configuration manager instance."""
    return config