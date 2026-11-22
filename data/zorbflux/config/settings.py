"""
Configuration Settings - Manages settings and configuration for ZorbFlux system.
"""

import os
from typing import Dict, Any


class ZorbConfig:
    """
    Configuration manager for ZorbFlux system.
    
    This class handles loading and managing configuration settings
    from defaults and environment variables.
    
    Attributes:
        settings (Dict[str, Any]): Dictionary of configuration settings.
    """
    
    def __init__(self):
        """Initialize configuration with default values."""
        self.settings: Dict[str, Any] = {}
        self.load_default_config()
    
    def load_default_config(self) -> None:
        """Loads default configuration values."""
        self.settings = {
            "flux_magnitude": 1.0,
            "quantum_threshold": 0.75,
            "network_port": 8888,
            "enable_caching": True,
            "max_zorbs": 100
        }
    
    def load_from_environment(self) -> None:
        """Loads configuration from environment variables."""
        env_flux = os.getenv("ZORB_FLUX_MAGNITUDE")
        if env_flux:
            self.settings["flux_magnitude"] = float(env_flux)
        
        env_threshold = os.getenv("ZORB_QUANTUM_THRESHOLD")
        if env_threshold:
            self.settings["quantum_threshold"] = float(env_threshold)
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a configuration setting.
        
        Args:
            key (str): Setting key to retrieve.
            default (Any): Default value if key not found.
            
        Returns:
            Any: Setting value or default.
        """
        return self.settings.get(key, default)
    
    def set_setting(self, key: str, value: Any) -> None:
        """
        Sets a configuration setting.
        
        Args:
            key (str): Setting key.
            value (Any): Setting value.
        """
        self.settings[key] = value
    
    def get_all_settings(self) -> Dict[str, Any]:
        """
        Returns all configuration settings.
        
        Returns:
            Dict[str, Any]: Copy of all settings.
        """
        return self.settings.copy()

