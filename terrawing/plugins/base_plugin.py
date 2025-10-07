"""
Base Plugin System - Modular AI plugin architecture

Provides a framework for extending TerraWing with custom AI modules
and functionality.
"""

import logging
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod


class BasePlugin(ABC):
    """
    Base class for TerraWing plugins.
    
    Plugins can extend functionality for:
    - Custom AI models
    - Specialized detection algorithms
    - Data processing pipelines
    - Integration with external systems
    """
    
    def __init__(self, plugin_id: str, config: Optional[Dict] = None):
        """
        Initialize plugin.
        
        Args:
            plugin_id: Unique plugin identifier
            config: Plugin configuration
        """
        self.plugin_id = plugin_id
        self.config = config or {}
        self.logger = logging.getLogger(f"TerraWing.Plugin.{plugin_id}")
        self.is_loaded = False
        self.is_enabled = False
    
    @abstractmethod
    def load(self) -> bool:
        """
        Load plugin resources and initialize.
        
        Returns:
            True if loaded successfully
        """
        pass
    
    @abstractmethod
    def unload(self) -> bool:
        """
        Unload plugin and cleanup resources.
        
        Returns:
            True if unloaded successfully
        """
        pass
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        """
        Process data through plugin.
        
        Args:
            data: Input data
            
        Returns:
            Processed output
        """
        pass
    
    def enable(self) -> bool:
        """Enable plugin."""
        if not self.is_loaded:
            self.logger.warning("Cannot enable: Plugin not loaded")
            return False
        
        self.is_enabled = True
        self.logger.info(f"Plugin enabled: {self.plugin_id}")
        return True
    
    def disable(self) -> bool:
        """Disable plugin."""
        self.is_enabled = False
        self.logger.info(f"Plugin disabled: {self.plugin_id}")
        return True
    
    def get_info(self) -> Dict:
        """
        Get plugin information.
        
        Returns:
            Dictionary with plugin metadata
        """
        return {
            'plugin_id': self.plugin_id,
            'is_loaded': self.is_loaded,
            'is_enabled': self.is_enabled,
            'config': self.config
        }


class PluginManager:
    """
    Plugin manager for loading and managing TerraWing plugins.
    """
    
    def __init__(self):
        """Initialize plugin manager."""
        self.logger = logging.getLogger("TerraWing.PluginManager")
        self.plugins: Dict[str, BasePlugin] = {}
        self.logger.info("Plugin Manager initialized")
    
    def register_plugin(self, plugin: BasePlugin) -> bool:
        """
        Register a plugin with the manager.
        
        Args:
            plugin: Plugin instance
            
        Returns:
            True if registered successfully
        """
        if plugin.plugin_id in self.plugins:
            self.logger.warning(f"Plugin already registered: {plugin.plugin_id}")
            return False
        
        self.plugins[plugin.plugin_id] = plugin
        self.logger.info(f"Plugin registered: {plugin.plugin_id}")
        return True
    
    def unregister_plugin(self, plugin_id: str) -> bool:
        """
        Unregister a plugin.
        
        Args:
            plugin_id: Plugin identifier
            
        Returns:
            True if unregistered successfully
        """
        if plugin_id not in self.plugins:
            return False
        
        plugin = self.plugins[plugin_id]
        if plugin.is_loaded:
            plugin.unload()
        
        del self.plugins[plugin_id]
        self.logger.info(f"Plugin unregistered: {plugin_id}")
        return True
    
    def load_plugin(self, plugin_id: str) -> bool:
        """
        Load a plugin.
        
        Args:
            plugin_id: Plugin identifier
            
        Returns:
            True if loaded successfully
        """
        if plugin_id not in self.plugins:
            self.logger.error(f"Plugin not found: {plugin_id}")
            return False
        
        plugin = self.plugins[plugin_id]
        return plugin.load()
    
    def unload_plugin(self, plugin_id: str) -> bool:
        """
        Unload a plugin.
        
        Args:
            plugin_id: Plugin identifier
            
        Returns:
            True if unloaded successfully
        """
        if plugin_id not in self.plugins:
            return False
        
        plugin = self.plugins[plugin_id]
        return plugin.unload()
    
    def enable_plugin(self, plugin_id: str) -> bool:
        """
        Enable a plugin.
        
        Args:
            plugin_id: Plugin identifier
            
        Returns:
            True if enabled successfully
        """
        if plugin_id not in self.plugins:
            return False
        
        return self.plugins[plugin_id].enable()
    
    def disable_plugin(self, plugin_id: str) -> bool:
        """
        Disable a plugin.
        
        Args:
            plugin_id: Plugin identifier
            
        Returns:
            True if disabled successfully
        """
        if plugin_id not in self.plugins:
            return False
        
        return self.plugins[plugin_id].disable()
    
    def get_plugin(self, plugin_id: str) -> Optional[BasePlugin]:
        """
        Get plugin by ID.
        
        Args:
            plugin_id: Plugin identifier
            
        Returns:
            Plugin instance or None
        """
        return self.plugins.get(plugin_id)
    
    def list_plugins(self) -> List[str]:
        """
        List all registered plugins.
        
        Returns:
            List of plugin IDs
        """
        return list(self.plugins.keys())
    
    def get_enabled_plugins(self) -> List[str]:
        """
        Get list of enabled plugins.
        
        Returns:
            List of enabled plugin IDs
        """
        return [pid for pid, plugin in self.plugins.items() if plugin.is_enabled]
    
    def process_with_plugin(self, plugin_id: str, data: Any) -> Optional[Any]:
        """
        Process data with a specific plugin.
        
        Args:
            plugin_id: Plugin identifier
            data: Input data
            
        Returns:
            Processed output or None if plugin not available
        """
        if plugin_id not in self.plugins:
            return None
        
        plugin = self.plugins[plugin_id]
        if not plugin.is_enabled:
            self.logger.warning(f"Plugin not enabled: {plugin_id}")
            return None
        
        return plugin.process(data)
    
    def get_statistics(self) -> Dict:
        """
        Get plugin manager statistics.
        
        Returns:
            Dictionary with statistics
        """
        return {
            'total_plugins': len(self.plugins),
            'loaded_plugins': len([p for p in self.plugins.values() if p.is_loaded]),
            'enabled_plugins': len([p for p in self.plugins.values() if p.is_enabled]),
            'plugin_list': self.list_plugins()
        }
