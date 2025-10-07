"""
Configuration management for TerraWing system.
"""

import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigManager:
    """
    Configuration manager for TerraWing.
    
    Handles loading, saving, and accessing configuration parameters.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.logger = logging.getLogger("TerraWing.ConfigManager")
        self.config_path = config_path
        self.config: Dict[str, Any] = self._load_defaults()
        
        if config_path:
            self.load_from_file(config_path)
    
    def _load_defaults(self) -> Dict[str, Any]:
        """
        Load default configuration.
        
        Returns:
            Default configuration dictionary
        """
        return {
            'uav': {
                'min_altitude': 5.0,
                'max_altitude': 120.0,
                'safe_battery': 20.0,
                'emergency_battery': 10.0
            },
            'obstacle_detection': {
                'detection_range': 50.0,
                'critical_distance': 10.0,
                'warning_distance': 20.0,
                'confidence_threshold': 0.7
            },
            'terrain_mapping': {
                'resolution': 1.0,
                'elevation_accuracy': 0.1,
                'max_map_age': 86400
            },
            'weather': {
                'update_interval': 300,
                'max_wind_speed': 12.0,
                'max_gust_speed': 15.0,
                'min_visibility': 1000.0,
                'max_precipitation': 2.0
            },
            'coordination': {
                'min_separation': 10.0,
                'max_fleet_size': 10,
                'heartbeat_timeout': 30.0
            },
            'video': {
                'target_fps': 30,
                'resolution': [1920, 1080],
                'buffer_size': 10
            },
            'system': {
                'log_level': 'INFO',
                'data_dir': './data',
                'model_dir': './models'
            }
        }
    
    def load_from_file(self, filepath: str) -> bool:
        """
        Load configuration from JSON file.
        
        Args:
            filepath: Path to configuration file
            
        Returns:
            True if loaded successfully
        """
        try:
            path = Path(filepath)
            if not path.exists():
                self.logger.warning(f"Config file not found: {filepath}")
                return False
            
            with open(filepath, 'r') as f:
                loaded_config = json.load(f)
            
            # Merge with defaults
            self._merge_config(self.config, loaded_config)
            self.config_path = filepath
            
            self.logger.info(f"Configuration loaded from {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return False
    
    def save_to_file(self, filepath: Optional[str] = None) -> bool:
        """
        Save configuration to JSON file.
        
        Args:
            filepath: Path to save configuration (uses loaded path if None)
            
        Returns:
            True if saved successfully
        """
        filepath = filepath or self.config_path
        if not filepath:
            self.logger.error("No filepath specified for saving config")
            return False
        
        try:
            path = Path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            self.logger.info(f"Configuration saved to {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
            return False
    
    def _merge_config(self, base: Dict, update: Dict) -> None:
        """
        Recursively merge configuration dictionaries.
        
        Args:
            base: Base configuration dictionary
            update: Update configuration dictionary
        """
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'uav.min_altitude')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_section(self, section: str) -> Dict:
        """
        Get entire configuration section.
        
        Args:
            section: Section name
            
        Returns:
            Section configuration dictionary
        """
        return self.config.get(section, {})
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults."""
        self.config = self._load_defaults()
        self.logger.info("Configuration reset to defaults")
    
    def validate(self) -> bool:
        """
        Validate configuration values.
        
        Returns:
            True if configuration is valid
        """
        # Add validation logic as needed
        required_sections = ['uav', 'obstacle_detection', 'terrain_mapping', 
                           'weather', 'coordination', 'video', 'system']
        
        for section in required_sections:
            if section not in self.config:
                self.logger.error(f"Missing required section: {section}")
                return False
        
        return True
    
    def to_dict(self) -> Dict:
        """
        Get configuration as dictionary.
        
        Returns:
            Configuration dictionary
        """
        return self.config.copy()
