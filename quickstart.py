#!/usr/bin/env python3
"""
TerraWing Quick Start Script

This script provides an interactive introduction to TerraWing's capabilities.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from terrawing import (
    UAVController,
    ObstacleDetector,
    TerrainMapper,
    WeatherIntegrator,
    DroneCoordinator,
    VideoProcessor
)
from terrawing.utils import setup_logging


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60 + "\n")


def demo_uav_controller():
    """Demonstrate UAV Controller."""
    print_header("UAV Controller Demo")
    
    uav = UAVController("DEMO-UAV")
    print(f"✓ UAV initialized: {uav.uav_id}")
    print(f"  Current state: {uav.state.flight_status.value}")
    print(f"  Battery: {uav.state.battery_level}%")
    
    # Demonstrate arming
    if uav.arm():
        print(f"✓ UAV armed")
    
    # Get telemetry
    telemetry = uav.get_telemetry()
    print(f"  Telemetry: Position={telemetry['position']}, "
          f"Mode={telemetry['flight_mode']}")


def demo_obstacle_detector():
    """Demonstrate Obstacle Detector."""
    print_header("Obstacle Detection Demo")
    
    from terrawing.core.obstacle_detector import ObstacleType
    
    detector = ObstacleDetector()
    detector.enable()
    print(f"✓ Obstacle detector enabled")
    print(f"  Detection range: {detector.detection_range}m")
    
    # Add sample obstacles
    detector.add_obstacle(
        ObstacleType.TREE,
        position=(15.0, 10.0, 0.0),
        size=(3.0, 8.0, 3.0),
        distance=18.0
    )
    
    detector.add_obstacle(
        ObstacleType.BUILDING,
        position=(25.0, 5.0, 0.0),
        size=(10.0, 15.0, 10.0),
        distance=26.0
    )
    
    obstacles = detector.get_obstacles()
    print(f"✓ Detected {len(obstacles)} obstacles:")
    for obs in obstacles:
        print(f"  - {obs.obstacle_type.value}: {obs.distance:.1f}m away")


def demo_terrain_mapper():
    """Demonstrate Terrain Mapper."""
    print_header("Terrain Mapping Demo")
    
    mapper = TerrainMapper()
    print(f"✓ Terrain mapper initialized")
    
    # Create a map
    terrain_map = mapper.create_map(
        map_id="DEMO-FIELD",
        bounds=(40.0, 40.1, -75.0, -74.9),
        resolution=1.0
    )
    print(f"✓ Created map: {terrain_map.metadata['map_id']}")
    print(f"  Bounds: {terrain_map.bounds}")
    print(f"  Resolution: {terrain_map.resolution}m")
    
    # Add sample terrain points
    for i in range(5):
        mapper.add_terrain_point(
            lat=40.05 + i * 0.01,
            lon=-74.95 + i * 0.01,
            elevation=50.0 + i * 2.0,
            terrain_type="crop"
        )
    
    stats = mapper.get_statistics()
    print(f"✓ Added {stats.get('active_map_points', 0)} terrain points")


def demo_weather_integrator():
    """Demonstrate Weather Integrator."""
    print_header("Weather Integration Demo")
    
    weather = WeatherIntegrator()
    print(f"✓ Weather integrator initialized")
    
    # Fetch weather
    weather_data = weather.fetch_weather(lat=40.7128, lon=-74.0060)
    if weather_data:
        print(f"✓ Weather data retrieved:")
        print(f"  Temperature: {weather_data.temperature}°C")
        print(f"  Wind speed: {weather_data.wind_speed} m/s")
        print(f"  Humidity: {weather_data.humidity}%")
        print(f"  Condition: {weather_data.condition.value}")
        
        safety = weather.assess_flight_safety()
        print(f"✓ Flight safety: {safety.value}")
        
        if weather.is_safe_to_fly():
            print(f"  ✓ Conditions are safe for flight")
        else:
            print(f"  ⚠ Conditions require caution")


def demo_drone_coordinator():
    """Demonstrate Drone Coordinator."""
    print_header("Multi-Drone Coordination Demo")
    
    from terrawing.core.drone_coordinator import TaskType
    
    coordinator = DroneCoordinator()
    print(f"✓ Drone coordinator initialized")
    
    # Register drones
    drones = [
        ("UAV-ALPHA", (40.050, -75.000, 0.0)),
        ("UAV-BETA", (40.051, -75.001, 0.0)),
        ("UAV-GAMMA", (40.052, -75.002, 0.0)),
    ]
    
    for drone_id, position in drones:
        coordinator.register_drone(drone_id, position)
    
    print(f"✓ Registered {len(coordinator.drones)} drones")
    
    # Create a mission
    mission = coordinator.create_mission(
        mission_type=TaskType.SURVEY,
        area_bounds=(40.05, 40.06, -75.00, -74.99),
        priority=1
    )
    print(f"✓ Created mission: {mission.mission_id}")
    
    # Assign mission
    coordinator.assign_mission(mission.mission_id, ["UAV-ALPHA", "UAV-BETA"])
    print(f"✓ Mission assigned to {len(mission.assigned_drones)} drones")
    
    stats = coordinator.get_statistics()
    print(f"  Active drones: {stats['active_drones']}")
    print(f"  Active missions: {stats['active_missions']}")


def demo_video_processor():
    """Demonstrate Video Processor."""
    print_header("Video Processing Demo")
    
    from terrawing.core.video_processor import VideoSource
    
    processor = VideoProcessor()
    print(f"✓ Video processor initialized")
    print(f"  Target FPS: {processor.target_fps}")
    print(f"  Resolution: {processor.resolution}")
    
    # Add video sources
    processor.add_source("main_camera", VideoSource.CAMERA_PRIMARY)
    processor.add_source("thermal_camera", VideoSource.THERMAL)
    
    processor.start()
    print(f"✓ Started processing with {len(processor.video_sources)} sources")
    
    # Capture and process a frame
    frame = processor.capture_frame("main_camera")
    if frame:
        result = processor.process_frame(frame)
        print(f"✓ Processed frame #{result.frame_id}")
        print(f"  Processing time: {result.analytics['processing_time']*1000:.2f}ms")


def main():
    """Run all demos."""
    # Setup logging (suppress most output)
    setup_logging(level="ERROR")
    
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "TerraWing Quick Start" + " " * 22 + "║")
    print("║" + " " * 10 + "AI-Powered UAV for Agriculture" + " " * 17 + "║")
    print("╚" + "═" * 58 + "╝")
    
    print("\nThis interactive demo showcases TerraWing's core capabilities.")
    print("Each section demonstrates a different module of the system.\n")
    
    try:
        demo_uav_controller()
        demo_obstacle_detector()
        demo_terrain_mapper()
        demo_weather_integrator()
        demo_drone_coordinator()
        demo_video_processor()
        
        print_header("Quick Start Complete!")
        print("All modules demonstrated successfully!")
        print("\nNext steps:")
        print("  1. Explore examples/basic_usage.py for detailed usage")
        print("  2. Read docs/API.md for complete API documentation")
        print("  3. Check README.md for installation and configuration")
        print("  4. Visit examples/multi_drone.py for fleet management")
        print("\nHappy flying with TerraWing! 🚁\n")
        
    except Exception as e:
        print(f"\n✗ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
