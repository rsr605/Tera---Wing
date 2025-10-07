# TerraWing API Documentation

## Overview

TerraWing provides a comprehensive API for UAV control, obstacle detection, terrain mapping, weather integration, multi-drone coordination, and video processing.

## Core Modules

### UAVController

The UAV Controller manages all flight operations and safety features.

#### Initialization

```python
from terrawing import UAVController

uav = UAVController(
    uav_id="UAV-01",
    config={
        'min_altitude': 5.0,
        'max_altitude': 120.0,
        'safe_battery': 20.0,
        'emergency_battery': 10.0
    }
)
```

#### Methods

##### `arm() -> bool`
Arms the UAV for flight.

**Returns:** `True` if armed successfully, `False` otherwise

**Example:**
```python
if uav.arm():
    print("UAV armed and ready")
```

##### `takeoff(target_altitude: float) -> bool`
Initiates takeoff to specified altitude.

**Parameters:**
- `target_altitude`: Target altitude in meters

**Returns:** `True` if takeoff successful

**Example:**
```python
uav.takeoff(target_altitude=15.0)
```

##### `navigate_to(lat: float, lon: float, alt: float) -> bool`
Navigates to specified coordinates.

**Parameters:**
- `lat`: Target latitude
- `lon`: Target longitude
- `alt`: Target altitude in meters

**Returns:** `True` if navigation successful

##### `land() -> bool`
Initiates landing sequence.

**Returns:** `True` if landing initiated

##### `return_to_launch() -> bool`
Returns to launch position and lands.

**Returns:** `True` if RTL initiated

##### `emergency_stop() -> bool`
Triggers emergency stop and landing.

**Returns:** `True` if emergency procedure initiated

---

### ObstacleDetector

AI-powered obstacle detection and classification system.

#### Initialization

```python
from terrawing import ObstacleDetector

detector = ObstacleDetector(
    config={
        'detection_range': 50.0,
        'critical_distance': 10.0,
        'confidence_threshold': 0.7
    }
)
detector.enable()
```

#### Methods

##### `add_obstacle(obstacle_type, position, size, distance) -> Obstacle`
Adds an obstacle to tracking.

**Parameters:**
- `obstacle_type`: Type of obstacle (ObstacleType enum)
- `position`: Tuple of (x, y, z) relative position
- `size`: Tuple of (width, height, depth) in meters
- `distance`: Distance from UAV in meters

**Returns:** Created Obstacle object

**Example:**
```python
from terrawing.core.obstacle_detector import ObstacleType

obstacle = detector.add_obstacle(
    obstacle_type=ObstacleType.TREE,
    position=(10.0, 5.0, 0.0),
    size=(2.0, 5.0, 2.0),
    distance=15.0
)
```

##### `get_obstacles(max_distance=None, min_threat_level=None) -> List[Obstacle]`
Gets list of detected obstacles with optional filtering.

**Parameters:**
- `max_distance`: Maximum distance filter
- `min_threat_level`: Minimum threat level filter

**Returns:** List of Obstacle objects

---

### TerrainMapper

Generates and maintains terrain maps for navigation.

#### Initialization

```python
from terrawing import TerrainMapper

mapper = TerrainMapper(
    config={
        'resolution': 1.0,
        'elevation_accuracy': 0.1
    }
)
```

#### Methods

##### `create_map(map_id, bounds, resolution=None) -> TerrainMap`
Creates a new terrain map.

**Parameters:**
- `map_id`: Unique map identifier
- `bounds`: Tuple of (min_lat, max_lat, min_lon, max_lon)
- `resolution`: Grid resolution in meters (optional)

**Returns:** Created TerrainMap object

**Example:**
```python
terrain_map = mapper.create_map(
    map_id="FIELD-001",
    bounds=(40.0, 40.1, -75.0, -74.9),
    resolution=1.0
)
```

##### `add_terrain_point(lat, lon, elevation, terrain_type="unknown", vegetation_density=0.0) -> bool`
Adds a terrain point to the active map.

**Parameters:**
- `lat`: Latitude
- `lon`: Longitude
- `elevation`: Elevation in meters
- `terrain_type`: Type of terrain (optional)
- `vegetation_density`: Vegetation density 0-1 (optional)

**Returns:** `True` if point added successfully

##### `get_elevation_at(lat, lon, map_id=None) -> Optional[float]`
Gets terrain elevation at coordinates.

**Parameters:**
- `lat`: Latitude
- `lon`: Longitude
- `map_id`: Map identifier (uses active if None)

**Returns:** Elevation in meters or None

---

### WeatherIntegrator

Integrates real-time weather data for flight safety.

#### Initialization

```python
from terrawing import WeatherIntegrator

weather = WeatherIntegrator(
    config={
        'update_interval': 300,
        'max_wind_speed': 12.0,
        'min_visibility': 1000.0
    }
)
```

#### Methods

##### `fetch_weather(lat, lon) -> Optional[WeatherData]`
Fetches current weather data for location.

**Parameters:**
- `lat`: Latitude
- `lon`: Longitude

**Returns:** WeatherData object or None

**Example:**
```python
weather_data = weather.fetch_weather(lat=40.7128, lon=-74.0060)
if weather_data:
    print(f"Temperature: {weather_data.temperature}°C")
    print(f"Wind speed: {weather_data.wind_speed} m/s")
```

##### `assess_flight_safety(weather_data=None) -> FlightSafety`
Assesses flight safety based on weather conditions.

**Parameters:**
- `weather_data`: Weather data to assess (uses current if None)

**Returns:** FlightSafety enum value (SAFE, CAUTION, UNSAFE, GROUNDED)

##### `is_safe_to_fly() -> bool`
Checks if current weather is safe for flight.

**Returns:** `True` if safe to fly

---

### DroneCoordinator

Multi-drone fleet management and coordination.

#### Initialization

```python
from terrawing import DroneCoordinator

coordinator = DroneCoordinator(
    config={
        'min_separation': 10.0,
        'max_fleet_size': 10
    }
)
```

#### Methods

##### `register_drone(drone_id, position, capabilities=None) -> bool`
Registers a drone with the coordinator.

**Parameters:**
- `drone_id`: Unique drone identifier
- `position`: Tuple of (lat, lon, alt)
- `capabilities`: Set of drone capabilities (optional)

**Returns:** `True` if registration successful

**Example:**
```python
coordinator.register_drone(
    "UAV-01",
    position=(40.0, -75.0, 0.0),
    capabilities={"camera", "lidar"}
)
```

##### `create_mission(mission_type, area_bounds, priority=1) -> Mission`
Creates a new mission.

**Parameters:**
- `mission_type`: Type of mission (TaskType enum)
- `area_bounds`: Tuple of (min_lat, max_lat, min_lon, max_lon)
- `priority`: Mission priority (higher = more important)

**Returns:** Created Mission object

##### `assign_mission(mission_id, drone_ids) -> bool`
Assigns drones to a mission.

**Parameters:**
- `mission_id`: Mission identifier
- `drone_ids`: List of drone identifiers

**Returns:** `True` if assignment successful

---

### VideoProcessor

Real-time video processing pipeline.

#### Initialization

```python
from terrawing import VideoProcessor

processor = VideoProcessor(
    config={
        'target_fps': 30,
        'resolution': (1920, 1080),
        'buffer_size': 10
    }
)
```

#### Methods

##### `start() -> bool`
Starts video processing pipeline.

**Returns:** `True` if started successfully

##### `add_source(source_id, source_type) -> bool`
Adds a video source to the processor.

**Parameters:**
- `source_id`: Unique source identifier
- `source_type`: Type of video source (VideoSource enum)

**Returns:** `True` if source added successfully

**Example:**
```python
from terrawing.core.video_processor import VideoSource

processor.add_source("camera_main", VideoSource.CAMERA_PRIMARY)
```

##### `process_frame(frame) -> ProcessingResult`
Processes a single video frame.

**Parameters:**
- `frame`: VideoFrame object

**Returns:** ProcessingResult object

---

## Plugin System

### BasePlugin

Base class for TerraWing plugins.

#### Creating a Custom Plugin

```python
from terrawing.plugins import BasePlugin

class MyPlugin(BasePlugin):
    def load(self):
        # Initialize plugin
        self.is_loaded = True
        return True
    
    def unload(self):
        # Cleanup
        self.is_loaded = False
        return True
    
    def process(self, data):
        # Process data
        return processed_data
```

### PluginManager

Manages plugin lifecycle.

```python
from terrawing.plugins import PluginManager

manager = PluginManager()
manager.register_plugin(my_plugin)
manager.load_plugin("my-plugin-id")
manager.enable_plugin("my-plugin-id")

# Process with plugin
result = manager.process_with_plugin("my-plugin-id", data)
```

---

## Utilities

### ConfigManager

Configuration management system.

```python
from terrawing.utils import ConfigManager

config = ConfigManager("config/my_config.json")
value = config.get("uav.min_altitude")
config.set("uav.max_altitude", 150.0)
config.save_to_file()
```

### Logging

Setup logging for TerraWing.

```python
from terrawing.utils import setup_logging

setup_logging(level="INFO", log_file="terrawing.log")
```

---

## Error Handling

All methods return appropriate values indicating success/failure. Check return values and handle errors appropriately:

```python
if not uav.arm():
    print("Failed to arm UAV")
    # Handle error

if not uav.takeoff(15.0):
    print("Takeoff failed")
    # Handle error
```

---

## Best Practices

1. **Always check weather before flight**
   ```python
   if not weather.is_safe_to_fly():
       print("Weather not safe for flight")
       return
   ```

2. **Monitor battery levels**
   ```python
   telemetry = uav.get_telemetry()
   if telemetry['battery_level'] < 25.0:
       uav.return_to_launch()
   ```

3. **Enable obstacle detection**
   ```python
   detector.enable()
   # Perform flight operations
   ```

4. **Use proper error handling**
   ```python
   try:
       uav.navigate_to(lat, lon, alt)
   except Exception as e:
       logger.error(f"Navigation failed: {e}")
       uav.emergency_stop()
   ```

5. **Clean up resources**
   ```python
   # After operations
   video_processor.stop()
   uav.land()
   uav.disarm()
   ```
