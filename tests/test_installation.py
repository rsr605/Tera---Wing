"""
Quick test script to verify TerraWing installation and basic functionality.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports():
    """Test that all modules can be imported."""
    print("Testing module imports...")
    try:
        from terrawing import (
            UAVController,
            ObstacleDetector,
            TerrainMapper,
            WeatherIntegrator,
            DroneCoordinator,
            VideoProcessor
        )
        from terrawing.utils import setup_logging, ConfigManager
        from terrawing.plugins import BasePlugin, PluginManager
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_basic_functionality():
    """Test basic functionality of core modules."""
    print("\nTesting basic functionality...")
    
    try:
        from terrawing import UAVController
        from terrawing.utils import setup_logging
        
        # Setup logging
        setup_logging(level="ERROR")  # Suppress logs during tests
        
        # Test UAV Controller
        uav = UAVController("TEST-UAV")
        assert uav.uav_id == "TEST-UAV"
        assert uav.arm() == True
        assert uav.state.is_armed == True
        print("✓ UAVController basic functionality working")
        
        # Test Obstacle Detector
        from terrawing import ObstacleDetector
        from terrawing.core.obstacle_detector import ObstacleType
        
        detector = ObstacleDetector()
        detector.enable()
        obstacle = detector.add_obstacle(
            ObstacleType.TREE,
            (10.0, 5.0, 0.0),
            (2.0, 5.0, 2.0),
            15.0
        )
        assert obstacle.obstacle_type == ObstacleType.TREE
        print("✓ ObstacleDetector basic functionality working")
        
        # Test Terrain Mapper
        from terrawing import TerrainMapper
        
        mapper = TerrainMapper()
        terrain_map = mapper.create_map("TEST-MAP", (40.0, 40.1, -75.0, -74.9))
        assert terrain_map.bounds == (40.0, 40.1, -75.0, -74.9)
        print("✓ TerrainMapper basic functionality working")
        
        # Test Weather Integrator
        from terrawing import WeatherIntegrator
        
        weather = WeatherIntegrator()
        weather_data = weather.fetch_weather(40.0, -75.0)
        assert weather_data is not None
        print("✓ WeatherIntegrator basic functionality working")
        
        # Test Drone Coordinator
        from terrawing import DroneCoordinator
        
        coordinator = DroneCoordinator()
        result = coordinator.register_drone("TEST-DRONE", (40.0, -75.0, 0.0))
        assert result == True
        print("✓ DroneCoordinator basic functionality working")
        
        # Test Video Processor
        from terrawing import VideoProcessor
        from terrawing.core.video_processor import VideoSource
        
        processor = VideoProcessor()
        processor.start()
        assert processor.is_active == True
        print("✓ VideoProcessor basic functionality working")
        
        # Test Config Manager
        from terrawing.utils import ConfigManager
        
        config = ConfigManager()
        value = config.get("uav.min_altitude")
        assert value == 5.0
        print("✓ ConfigManager basic functionality working")
        
        # Test Plugin System
        from terrawing.plugins import PluginManager
        
        manager = PluginManager()
        assert len(manager.list_plugins()) == 0
        print("✓ PluginManager basic functionality working")
        
        return True
        
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("TerraWing Installation Test")
    print("=" * 60)
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    # Test basic functionality
    if not test_basic_functionality():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✓ All tests passed! TerraWing is working correctly.")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    print("=" * 60)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
