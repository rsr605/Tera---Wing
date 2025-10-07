"""
Terrain Mapper - Generates and maintains terrain maps

Creates detailed 3D terrain maps from sensor data for navigation
and mission planning.
"""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import time
import json


@dataclass
class TerrainPoint:
    """A point in the terrain map."""
    latitude: float
    longitude: float
    elevation: float
    timestamp: float = field(default_factory=time.time)
    terrain_type: str = "unknown"  # grass, crop, soil, water, etc.
    vegetation_density: float = 0.0  # 0-1
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'lat': self.latitude,
            'lon': self.longitude,
            'elevation': self.elevation,
            'timestamp': self.timestamp,
            'terrain_type': self.terrain_type,
            'vegetation_density': self.vegetation_density
        }


@dataclass
class TerrainMap:
    """Terrain map containing grid of terrain points."""
    bounds: Tuple[float, float, float, float]  # (min_lat, max_lat, min_lon, max_lon)
    resolution: float  # meters per grid cell
    grid_data: Dict[Tuple[int, int], TerrainPoint] = field(default_factory=dict)
    metadata: Dict = field(default_factory=dict)
    
    def add_point(self, point: TerrainPoint) -> None:
        """Add a terrain point to the map."""
        # Convert lat/lon to grid coordinates
        grid_x = int((point.latitude - self.bounds[0]) / self.resolution)
        grid_y = int((point.longitude - self.bounds[2]) / self.resolution)
        self.grid_data[(grid_x, grid_y)] = point
    
    def get_point(self, lat: float, lon: float) -> Optional[TerrainPoint]:
        """Get terrain point at coordinates."""
        grid_x = int((lat - self.bounds[0]) / self.resolution)
        grid_y = int((lon - self.bounds[2]) / self.resolution)
        return self.grid_data.get((grid_x, grid_y))
    
    def get_elevation(self, lat: float, lon: float) -> Optional[float]:
        """Get elevation at coordinates."""
        point = self.get_point(lat, lon)
        return point.elevation if point else None
    
    def to_dict(self) -> Dict:
        """Convert map to dictionary for serialization."""
        return {
            'bounds': self.bounds,
            'resolution': self.resolution,
            'point_count': len(self.grid_data),
            'metadata': self.metadata
        }


class TerrainMapper:
    """
    Terrain mapping system for generating detailed terrain maps.
    
    Processes sensor data to create 3D terrain maps for navigation,
    mission planning, and agricultural analysis.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize terrain mapper.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.logger = logging.getLogger("TerraWing.TerrainMapper")
        
        # Mapping parameters
        self.default_resolution = self.config.get('resolution', 1.0)  # meters
        self.elevation_accuracy = self.config.get('elevation_accuracy', 0.1)  # meters
        self.max_map_age = self.config.get('max_map_age', 86400)  # 24 hours
        
        # Current maps
        self.maps: Dict[str, TerrainMap] = {}
        self.active_map_id: Optional[str] = None
        
        self.logger.info("Terrain Mapper initialized")
    
    def create_map(self, map_id: str, bounds: Tuple[float, float, float, float],
                   resolution: Optional[float] = None) -> TerrainMap:
        """
        Create a new terrain map.
        
        Args:
            map_id: Unique identifier for the map
            bounds: Map boundaries (min_lat, max_lat, min_lon, max_lon)
            resolution: Grid resolution in meters
            
        Returns:
            Created TerrainMap
        """
        resolution = resolution or self.default_resolution
        
        terrain_map = TerrainMap(
            bounds=bounds,
            resolution=resolution,
            metadata={
                'created': time.time(),
                'map_id': map_id
            }
        )
        
        self.maps[map_id] = terrain_map
        self.active_map_id = map_id
        
        self.logger.info(f"Created terrain map: {map_id} with resolution {resolution}m")
        return terrain_map
    
    def set_active_map(self, map_id: str) -> bool:
        """
        Set the active terrain map.
        
        Args:
            map_id: Map identifier
            
        Returns:
            True if map exists and was set as active
        """
        if map_id in self.maps:
            self.active_map_id = map_id
            self.logger.info(f"Active map set to: {map_id}")
            return True
        
        self.logger.warning(f"Map not found: {map_id}")
        return False
    
    def get_map(self, map_id: Optional[str] = None) -> Optional[TerrainMap]:
        """
        Get terrain map by ID.
        
        Args:
            map_id: Map identifier (uses active map if None)
            
        Returns:
            TerrainMap or None if not found
        """
        if map_id is None:
            map_id = self.active_map_id
        
        return self.maps.get(map_id) if map_id else None
    
    def process_sensor_data(self, sensor_data: Dict) -> int:
        """
        Process sensor data to update terrain map.
        
        Args:
            sensor_data: Data from LiDAR, stereo cameras, etc.
            
        Returns:
            Number of points added to map
        """
        if not self.active_map_id:
            self.logger.warning("No active map to update")
            return 0
        
        terrain_map = self.maps[self.active_map_id]
        points_added = 0
        
        # In production, this would process actual sensor data:
        # 1. LiDAR point clouds
        # 2. Stereo vision depth maps
        # 3. Photogrammetry data
        # 4. Process and filter points
        # 5. Update map grid
        
        return points_added
    
    def add_terrain_point(self, lat: float, lon: float, elevation: float,
                         terrain_type: str = "unknown",
                         vegetation_density: float = 0.0) -> bool:
        """
        Add a terrain point to the active map.
        
        Args:
            lat: Latitude
            lon: Longitude
            elevation: Elevation in meters
            terrain_type: Type of terrain
            vegetation_density: Vegetation density (0-1)
            
        Returns:
            True if point added successfully
        """
        if not self.active_map_id:
            self.logger.warning("No active map")
            return False
        
        terrain_map = self.maps[self.active_map_id]
        
        # Check if point is within map bounds
        if not (terrain_map.bounds[0] <= lat <= terrain_map.bounds[1] and
                terrain_map.bounds[2] <= lon <= terrain_map.bounds[3]):
            return False
        
        point = TerrainPoint(
            latitude=lat,
            longitude=lon,
            elevation=elevation,
            terrain_type=terrain_type,
            vegetation_density=vegetation_density
        )
        
        terrain_map.add_point(point)
        return True
    
    def get_elevation_at(self, lat: float, lon: float,
                        map_id: Optional[str] = None) -> Optional[float]:
        """
        Get terrain elevation at coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            map_id: Map identifier (uses active map if None)
            
        Returns:
            Elevation in meters or None if not available
        """
        terrain_map = self.get_map(map_id)
        if not terrain_map:
            return None
        
        return terrain_map.get_elevation(lat, lon)
    
    def generate_elevation_profile(self, start: Tuple[float, float],
                                   end: Tuple[float, float],
                                   num_samples: int = 100) -> List[float]:
        """
        Generate elevation profile between two points.
        
        Args:
            start: Start coordinates (lat, lon)
            end: End coordinates (lat, lon)
            num_samples: Number of sample points
            
        Returns:
            List of elevations along the path
        """
        if not self.active_map_id:
            return []
        
        terrain_map = self.maps[self.active_map_id]
        profile = []
        
        for i in range(num_samples):
            t = i / (num_samples - 1)
            lat = start[0] + t * (end[0] - start[0])
            lon = start[1] + t * (end[1] - start[1])
            
            elevation = terrain_map.get_elevation(lat, lon)
            if elevation is not None:
                profile.append(elevation)
        
        return profile
    
    def calculate_slope(self, lat: float, lon: float, radius: float = 1.0) -> Optional[float]:
        """
        Calculate terrain slope at a point.
        
        Args:
            lat: Latitude
            lon: Longitude
            radius: Radius for slope calculation
            
        Returns:
            Slope in degrees or None
        """
        terrain_map = self.get_map()
        if not terrain_map:
            return None
        
        # In production, calculate slope from neighboring points
        # For now, return placeholder
        return 0.0
    
    def find_safe_landing_zones(self, area_bounds: Tuple[float, float, float, float],
                               min_area_size: float = 25.0,
                               max_slope: float = 5.0) -> List[Dict]:
        """
        Identify safe landing zones within an area.
        
        Args:
            area_bounds: Area to search (min_lat, max_lat, min_lon, max_lon)
            min_area_size: Minimum landing zone size in square meters
            max_slope: Maximum acceptable slope in degrees
            
        Returns:
            List of safe landing zones with coordinates and characteristics
        """
        landing_zones = []
        
        # In production, analyze terrain for:
        # 1. Flat areas
        # 2. Obstacle-free zones
        # 3. Sufficient size
        # 4. Accessibility
        
        return landing_zones
    
    def export_map(self, map_id: Optional[str] = None,
                  format: str = "json") -> Optional[str]:
        """
        Export terrain map to specified format.
        
        Args:
            map_id: Map identifier (uses active map if None)
            format: Export format (json, geotiff, etc.)
            
        Returns:
            Exported map data as string or None
        """
        terrain_map = self.get_map(map_id)
        if not terrain_map:
            return None
        
        if format == "json":
            data = terrain_map.to_dict()
            return json.dumps(data, indent=2)
        
        # Add support for other formats as needed
        return None
    
    def import_map(self, map_data: str, map_id: str, format: str = "json") -> bool:
        """
        Import terrain map from data.
        
        Args:
            map_data: Map data string
            map_id: Identifier for imported map
            format: Data format
            
        Returns:
            True if import successful
        """
        try:
            if format == "json":
                data = json.loads(map_data)
                terrain_map = TerrainMap(
                    bounds=tuple(data['bounds']),
                    resolution=data['resolution'],
                    metadata=data.get('metadata', {})
                )
                self.maps[map_id] = terrain_map
                self.logger.info(f"Imported map: {map_id}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to import map: {e}")
        
        return False
    
    def get_statistics(self) -> Dict:
        """
        Get terrain mapping statistics.
        
        Returns:
            Dictionary with statistics
        """
        active_map = self.get_map()
        
        stats = {
            'total_maps': len(self.maps),
            'active_map': self.active_map_id,
            'default_resolution': self.default_resolution
        }
        
        if active_map:
            stats['active_map_points'] = len(active_map.grid_data)
            stats['active_map_bounds'] = active_map.bounds
        
        return stats
