"""
Obstacle Detector - AI-powered obstacle detection and classification

Uses computer vision and machine learning to detect and classify obstacles
in real-time from video feeds.
"""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import time


class ObstacleType(Enum):
    """Types of obstacles that can be detected."""
    UNKNOWN = "unknown"
    TREE = "tree"
    BUILDING = "building"
    POWER_LINE = "power_line"
    TOWER = "tower"
    VEHICLE = "vehicle"
    ANIMAL = "animal"
    PERSON = "person"
    FENCE = "fence"
    TERRAIN = "terrain"
    DRONE = "drone"


class ThreatLevel(Enum):
    """Threat level of detected obstacle."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Obstacle:
    """Detected obstacle information."""
    obstacle_id: str
    obstacle_type: ObstacleType
    position: Tuple[float, float, float]  # (x, y, z) relative to UAV
    distance: float  # meters
    size: Tuple[float, float, float]  # (width, height, depth) in meters
    velocity: Optional[Tuple[float, float, float]] = None  # (vx, vy, vz) if moving
    threat_level: ThreatLevel = ThreatLevel.LOW
    confidence: float = 0.0  # Detection confidence 0-1
    timestamp: float = 0.0
    
    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()


class ObstacleDetector:
    """
    AI-powered obstacle detection and classification system.
    
    Processes video feeds to detect and classify obstacles in real-time,
    providing collision avoidance information to the UAV controller.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize obstacle detector.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.logger = logging.getLogger("TerraWing.ObstacleDetector")
        
        # Detection parameters
        self.detection_range = self.config.get('detection_range', 50.0)  # meters
        self.critical_distance = self.config.get('critical_distance', 10.0)  # meters
        self.warning_distance = self.config.get('warning_distance', 20.0)  # meters
        self.confidence_threshold = self.config.get('confidence_threshold', 0.7)
        
        # Detection state
        self.detected_obstacles: Dict[str, Obstacle] = {}
        self.obstacle_counter = 0
        self.is_enabled = True
        
        # AI model placeholder (would load actual model in production)
        self.model_loaded = False
        
        self.logger.info("Obstacle Detector initialized")
    
    def enable(self) -> None:
        """Enable obstacle detection."""
        self.is_enabled = True
        self.logger.info("Obstacle detection enabled")
    
    def disable(self) -> None:
        """Disable obstacle detection."""
        self.is_enabled = False
        self.logger.info("Obstacle detection disabled")
    
    def load_model(self, model_path: str) -> bool:
        """
        Load AI detection model.
        
        Args:
            model_path: Path to trained model file
            
        Returns:
            True if model loaded successfully
        """
        try:
            # In production, this would load an actual AI model (e.g., YOLO, Faster R-CNN)
            self.logger.info(f"Loading detection model from {model_path}")
            self.model_loaded = True
            return True
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            return False
    
    def process_frame(self, frame_data: Optional[bytes] = None) -> List[Obstacle]:
        """
        Process video frame for obstacle detection.
        
        Args:
            frame_data: Raw frame data from camera
            
        Returns:
            List of detected obstacles
        """
        if not self.is_enabled:
            return []
        
        # In production, this would:
        # 1. Process frame through AI model
        # 2. Extract bounding boxes and classifications
        # 3. Calculate 3D positions using depth estimation
        # 4. Track obstacles across frames
        
        # For now, return empty list (placeholder)
        return []
    
    def detect_obstacles(self, sensor_data: Optional[Dict] = None) -> List[Obstacle]:
        """
        Detect obstacles from sensor data.
        
        Args:
            sensor_data: Data from various sensors (cameras, lidar, radar)
            
        Returns:
            List of detected obstacles
        """
        if not self.is_enabled:
            return []
        
        detected = []
        
        # Simulate detection process
        # In production, this would integrate multiple sensor sources
        
        return detected
    
    def classify_obstacle(self, detection_data: Dict) -> ObstacleType:
        """
        Classify detected obstacle.
        
        Args:
            detection_data: Raw detection data
            
        Returns:
            Classified obstacle type
        """
        # In production, use AI model for classification
        # For now, return UNKNOWN as placeholder
        return ObstacleType.UNKNOWN
    
    def calculate_threat_level(self, obstacle: Obstacle, uav_position: Tuple[float, float, float],
                               uav_velocity: Tuple[float, float, float]) -> ThreatLevel:
        """
        Calculate threat level based on obstacle characteristics and UAV state.
        
        Args:
            obstacle: Detected obstacle
            uav_position: Current UAV position
            uav_velocity: Current UAV velocity
            
        Returns:
            Calculated threat level
        """
        distance = obstacle.distance
        
        # Calculate time to collision if on collision course
        # In production, use more sophisticated collision prediction
        
        if distance < self.critical_distance:
            return ThreatLevel.CRITICAL
        elif distance < self.warning_distance:
            return ThreatLevel.HIGH
        elif distance < self.detection_range * 0.5:
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.LOW
    
    def add_obstacle(self, obstacle_type: ObstacleType, position: Tuple[float, float, float],
                     size: Tuple[float, float, float], distance: float,
                     confidence: float = 1.0) -> Obstacle:
        """
        Manually add an obstacle (for testing or external sensors).
        
        Args:
            obstacle_type: Type of obstacle
            position: Position relative to UAV
            size: Size of obstacle
            distance: Distance from UAV
            confidence: Detection confidence
            
        Returns:
            Created obstacle object
        """
        self.obstacle_counter += 1
        obstacle_id = f"OBS-{self.obstacle_counter:04d}"
        
        obstacle = Obstacle(
            obstacle_id=obstacle_id,
            obstacle_type=obstacle_type,
            position=position,
            distance=distance,
            size=size,
            confidence=confidence,
            threat_level=ThreatLevel.LOW
        )
        
        self.detected_obstacles[obstacle_id] = obstacle
        self.logger.info(f"Obstacle detected: {obstacle_type.value} at {distance:.1f}m")
        
        return obstacle
    
    def update_obstacle(self, obstacle_id: str, position: Optional[Tuple[float, float, float]] = None,
                       velocity: Optional[Tuple[float, float, float]] = None) -> bool:
        """
        Update obstacle information.
        
        Args:
            obstacle_id: ID of obstacle to update
            position: New position
            velocity: Obstacle velocity
            
        Returns:
            True if update successful
        """
        if obstacle_id not in self.detected_obstacles:
            return False
        
        obstacle = self.detected_obstacles[obstacle_id]
        
        if position:
            obstacle.position = position
            # Recalculate distance
            obstacle.distance = (position[0]**2 + position[1]**2 + position[2]**2)**0.5
        
        if velocity:
            obstacle.velocity = velocity
        
        obstacle.timestamp = time.time()
        
        return True
    
    def remove_obstacle(self, obstacle_id: str) -> bool:
        """
        Remove obstacle from tracking.
        
        Args:
            obstacle_id: ID of obstacle to remove
            
        Returns:
            True if removed successfully
        """
        if obstacle_id in self.detected_obstacles:
            del self.detected_obstacles[obstacle_id]
            self.logger.info(f"Obstacle removed: {obstacle_id}")
            return True
        return False
    
    def get_obstacles(self, max_distance: Optional[float] = None,
                     min_threat_level: Optional[ThreatLevel] = None) -> List[Obstacle]:
        """
        Get list of detected obstacles with optional filtering.
        
        Args:
            max_distance: Maximum distance filter
            min_threat_level: Minimum threat level filter
            
        Returns:
            List of obstacles matching criteria
        """
        obstacles = list(self.detected_obstacles.values())
        
        if max_distance:
            obstacles = [obs for obs in obstacles if obs.distance <= max_distance]
        
        if min_threat_level:
            threat_order = [ThreatLevel.LOW, ThreatLevel.MEDIUM, ThreatLevel.HIGH, ThreatLevel.CRITICAL]
            min_index = threat_order.index(min_threat_level)
            obstacles = [obs for obs in obstacles 
                        if threat_order.index(obs.threat_level) >= min_index]
        
        return sorted(obstacles, key=lambda x: x.distance)
    
    def get_critical_obstacles(self) -> List[Obstacle]:
        """
        Get obstacles with critical threat level.
        
        Returns:
            List of critical obstacles
        """
        return self.get_obstacles(min_threat_level=ThreatLevel.CRITICAL)
    
    def clear_old_obstacles(self, max_age: float = 5.0) -> int:
        """
        Clear obstacles that haven't been updated recently.
        
        Args:
            max_age: Maximum age in seconds
            
        Returns:
            Number of obstacles removed
        """
        current_time = time.time()
        to_remove = []
        
        for obstacle_id, obstacle in self.detected_obstacles.items():
            if current_time - obstacle.timestamp > max_age:
                to_remove.append(obstacle_id)
        
        for obstacle_id in to_remove:
            self.remove_obstacle(obstacle_id)
        
        return len(to_remove)
    
    def get_statistics(self) -> Dict:
        """
        Get detection statistics.
        
        Returns:
            Dictionary with statistics
        """
        obstacles = list(self.detected_obstacles.values())
        
        return {
            'total_obstacles': len(obstacles),
            'critical_threats': len([o for o in obstacles if o.threat_level == ThreatLevel.CRITICAL]),
            'high_threats': len([o for o in obstacles if o.threat_level == ThreatLevel.HIGH]),
            'medium_threats': len([o for o in obstacles if o.threat_level == ThreatLevel.MEDIUM]),
            'low_threats': len([o for o in obstacles if o.threat_level == ThreatLevel.LOW]),
            'detection_enabled': self.is_enabled,
            'model_loaded': self.model_loaded
        }
