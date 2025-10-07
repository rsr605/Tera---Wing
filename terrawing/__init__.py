"""
TerraWing - AI-Powered UAV Solution for Agriculture

TerraWing is an intelligent UAV system that provides:
- Obstacle detection and classification
- Terrain mapping
- Weather data integration
- Multi-drone collaboration
- Real-time video processing
- Modular AI plugin architecture
"""

__version__ = "1.0.0"
__author__ = "TerraWing Team"

from .core.uav_controller import UAVController
from .core.obstacle_detector import ObstacleDetector
from .core.terrain_mapper import TerrainMapper
from .core.weather_integrator import WeatherIntegrator
from .core.drone_coordinator import DroneCoordinator
from .core.video_processor import VideoProcessor

__all__ = [
    'UAVController',
    'ObstacleDetector',
    'TerrainMapper',
    'WeatherIntegrator',
    'DroneCoordinator',
    'VideoProcessor',
]
