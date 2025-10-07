"""
Basic TerraWing usage example.

Demonstrates how to use the core TerraWing modules for UAV operations.
"""

import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from terrawing import (
    UAVController,
    ObstacleDetector,
    TerrainMapper,
    WeatherIntegrator,
    DroneCoordinator,
    VideoProcessor
)
from terrawing.utils import setup_logging, ConfigManager


def main():
    """Run basic TerraWing example."""
    
    # Setup logging
    setup_logging(level="INFO")
    print("=" * 60)
    print("TerraWing - AI-Powered UAV Solution")
    print("=" * 60)
    
    # Load configuration
    config_manager = ConfigManager()
    config = config_manager.to_dict()
    
    # Initialize UAV Controller
    print("\n[1] Initializing UAV Controller...")
    uav = UAVController(uav_id="UAV-DEMO-01", config=config['uav'])
    print(f"    Status: {uav.get_state()}")
    
    # Initialize Obstacle Detector
    print("\n[2] Initializing Obstacle Detection System...")
    obstacle_detector = ObstacleDetector(config=config['obstacle_detection'])
    obstacle_detector.enable()
    print(f"    Detection range: {obstacle_detector.detection_range}m")
    
    # Initialize Terrain Mapper
    print("\n[3] Initializing Terrain Mapping System...")
    terrain_mapper = TerrainMapper(config=config['terrain_mapping'])
    # Create a test map
    terrain_mapper.create_map(
        map_id="FIELD-001",
        bounds=(40.0, 40.1, -75.0, -74.9),
        resolution=1.0
    )
    print(f"    Map created with resolution: {terrain_mapper.default_resolution}m")
    
    # Initialize Weather Integrator
    print("\n[4] Initializing Weather Integration...")
    weather = WeatherIntegrator(config=config['weather'])
    weather_data = weather.fetch_weather(40.05, -74.95)
    if weather_data:
        print(f"    Weather: {weather_data.condition.value}, "
              f"Wind: {weather_data.wind_speed} m/s, "
              f"Temp: {weather_data.temperature}°C")
        print(f"    Flight safety: {weather.assess_flight_safety().value}")
    
    # Initialize Drone Coordinator
    print("\n[5] Initializing Multi-Drone Coordinator...")
    coordinator = DroneCoordinator(config=config['coordination'])
    coordinator.register_drone("UAV-DEMO-01", (40.05, -74.95, 0.0))
    print(f"    Fleet size: {len(coordinator.drones)}")
    
    # Initialize Video Processor
    print("\n[6] Initializing Video Processing Pipeline...")
    from terrawing.core.video_processor import VideoSource
    video_processor = VideoProcessor(config=config['video'])
    video_processor.add_source("camera_main", VideoSource.CAMERA_PRIMARY)
    video_processor.start()
    print(f"    Video sources: {len(video_processor.video_sources)}")
    
    # Simulate flight operations
    print("\n[7] Simulating Flight Operations...")
    print("    " + "-" * 50)
    
    # Check weather before flight
    if not weather.is_safe_to_fly():
        print("    ⚠ Weather conditions not safe for flight!")
        return
    
    # Arm and takeoff
    print("    → Arming UAV...")
    if uav.arm():
        print("    ✓ UAV armed")
    
    print("    → Taking off to 15m...")
    if uav.takeoff(target_altitude=15.0):
        print("    ✓ Takeoff successful")
        print(f"    Current position: {uav.state.position}")
    
    # Navigate to waypoint
    print("    → Navigating to waypoint...")
    if uav.navigate_to(40.055, -74.945, 15.0):
        print("    ✓ Waypoint reached")
    
    # Simulate obstacle detection
    print("    → Scanning for obstacles...")
    from terrawing.core.obstacle_detector import ObstacleType
    obstacle = obstacle_detector.add_obstacle(
        ObstacleType.TREE,
        position=(10.0, 5.0, 0.0),
        size=(2.0, 5.0, 2.0),
        distance=15.0
    )
    print(f"    ⚠ Obstacle detected: {obstacle.obstacle_type.value} at {obstacle.distance}m")
    
    # Add terrain data
    print("    → Mapping terrain...")
    for i in range(10):
        lat = 40.05 + i * 0.001
        lon = -74.95 + i * 0.001
        elevation = 50.0 + i * 0.5
        terrain_mapper.add_terrain_point(lat, lon, elevation)
    stats = terrain_mapper.get_statistics()
    print(f"    ✓ Terrain points mapped: {stats.get('active_map_points', 0)}")
    
    # Process video frame
    print("    → Processing video feed...")
    frame = video_processor.capture_frame("camera_main")
    if frame:
        result = video_processor.process_frame(frame)
        print(f"    ✓ Frame processed in {result.analytics['processing_time']*1000:.2f}ms")
    
    # Return to launch
    print("    → Returning to launch...")
    if uav.return_to_launch():
        print("    ✓ Landed successfully")
    
    # Disarm
    if uav.disarm():
        print("    ✓ UAV disarmed")
    
    # Display summary
    print("\n[8] Mission Summary:")
    print("    " + "-" * 50)
    print(f"    UAV Status: {uav.state.flight_status.value}")
    print(f"    Battery: {uav.state.battery_level}%")
    print(f"    Obstacles Detected: {len(obstacle_detector.detected_obstacles)}")
    print(f"    Terrain Points: {stats.get('active_map_points', 0)}")
    print(f"    Video Frames: {video_processor.frames_processed}")
    
    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
