"""
Drone Coordinator - Multi-drone collaboration system

Manages coordination between multiple drones for efficient coverage
and collaborative operations.
"""

import logging
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import time


class CoordinationMode(Enum):
    """Coordination modes for multi-drone operations."""
    INDEPENDENT = "independent"
    LEADER_FOLLOWER = "leader_follower"
    SWARM = "swarm"
    DISTRIBUTED = "distributed"


class TaskType(Enum):
    """Types of tasks that can be assigned."""
    SURVEY = "survey"
    PATROL = "patrol"
    MONITORING = "monitoring"
    INSPECTION = "inspection"
    MAPPING = "mapping"
    IDLE = "idle"


@dataclass
class DroneInfo:
    """Information about a drone in the fleet."""
    drone_id: str
    position: Tuple[float, float, float]
    battery_level: float
    status: str
    task: TaskType = TaskType.IDLE
    capabilities: Set[str] = field(default_factory=set)
    last_update: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'drone_id': self.drone_id,
            'position': self.position,
            'battery_level': self.battery_level,
            'status': self.status,
            'task': self.task.value,
            'capabilities': list(self.capabilities),
            'last_update': self.last_update
        }


@dataclass
class Mission:
    """Mission definition for drone operations."""
    mission_id: str
    mission_type: TaskType
    area_bounds: Tuple[float, float, float, float]  # (min_lat, max_lat, min_lon, max_lon)
    assigned_drones: List[str] = field(default_factory=list)
    priority: int = 1
    status: str = "pending"  # pending, active, completed, failed
    created: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'mission_id': self.mission_id,
            'mission_type': self.mission_type.value,
            'area_bounds': self.area_bounds,
            'assigned_drones': self.assigned_drones,
            'priority': self.priority,
            'status': self.status,
            'created': self.created
        }


class DroneCoordinator:
    """
    Multi-drone coordination system.
    
    Manages fleet of drones, assigns tasks, coordinates operations,
    and ensures efficient coverage and collaboration.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize drone coordinator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.logger = logging.getLogger("TerraWing.DroneCoordinator")
        
        # Coordination parameters
        self.coordination_mode = CoordinationMode.DISTRIBUTED
        self.min_drone_separation = self.config.get('min_separation', 10.0)  # meters
        self.max_fleet_size = self.config.get('max_fleet_size', 10)
        self.heartbeat_timeout = self.config.get('heartbeat_timeout', 30.0)  # seconds
        
        # Fleet management
        self.drones: Dict[str, DroneInfo] = {}
        self.missions: Dict[str, Mission] = {}
        self.mission_counter = 0
        
        self.logger.info("Drone Coordinator initialized")
    
    def register_drone(self, drone_id: str, position: Tuple[float, float, float],
                      capabilities: Optional[Set[str]] = None) -> bool:
        """
        Register a drone with the coordinator.
        
        Args:
            drone_id: Unique drone identifier
            position: Initial position (lat, lon, alt)
            capabilities: Set of drone capabilities
            
        Returns:
            True if registration successful
        """
        if drone_id in self.drones:
            self.logger.warning(f"Drone already registered: {drone_id}")
            return False
        
        if len(self.drones) >= self.max_fleet_size:
            self.logger.error(f"Fleet size limit reached: {self.max_fleet_size}")
            return False
        
        drone_info = DroneInfo(
            drone_id=drone_id,
            position=position,
            battery_level=100.0,
            status="ready",
            capabilities=capabilities or set()
        )
        
        self.drones[drone_id] = drone_info
        self.logger.info(f"Drone registered: {drone_id}")
        return True
    
    def unregister_drone(self, drone_id: str) -> bool:
        """
        Unregister a drone from the coordinator.
        
        Args:
            drone_id: Drone identifier
            
        Returns:
            True if unregistered successfully
        """
        if drone_id not in self.drones:
            return False
        
        # Remove from any assigned missions
        for mission in self.missions.values():
            if drone_id in mission.assigned_drones:
                mission.assigned_drones.remove(drone_id)
        
        del self.drones[drone_id]
        self.logger.info(f"Drone unregistered: {drone_id}")
        return True
    
    def update_drone_state(self, drone_id: str, position: Optional[Tuple[float, float, float]] = None,
                          battery_level: Optional[float] = None, status: Optional[str] = None) -> bool:
        """
        Update drone state information.
        
        Args:
            drone_id: Drone identifier
            position: Updated position
            battery_level: Updated battery level
            status: Updated status
            
        Returns:
            True if update successful
        """
        if drone_id not in self.drones:
            return False
        
        drone = self.drones[drone_id]
        
        if position:
            drone.position = position
        if battery_level is not None:
            drone.battery_level = battery_level
        if status:
            drone.status = status
        
        drone.last_update = time.time()
        return True
    
    def get_drone_info(self, drone_id: str) -> Optional[DroneInfo]:
        """
        Get information about a drone.
        
        Args:
            drone_id: Drone identifier
            
        Returns:
            DroneInfo or None
        """
        return self.drones.get(drone_id)
    
    def get_fleet_info(self) -> List[DroneInfo]:
        """
        Get information about all drones in fleet.
        
        Returns:
            List of DroneInfo
        """
        return list(self.drones.values())
    
    def create_mission(self, mission_type: TaskType, area_bounds: Tuple[float, float, float, float],
                      priority: int = 1) -> Mission:
        """
        Create a new mission.
        
        Args:
            mission_type: Type of mission
            area_bounds: Area boundaries
            priority: Mission priority (higher = more important)
            
        Returns:
            Created Mission
        """
        self.mission_counter += 1
        mission_id = f"MISSION-{self.mission_counter:04d}"
        
        mission = Mission(
            mission_id=mission_id,
            mission_type=mission_type,
            area_bounds=area_bounds,
            priority=priority
        )
        
        self.missions[mission_id] = mission
        self.logger.info(f"Mission created: {mission_id} ({mission_type.value})")
        
        return mission
    
    def assign_mission(self, mission_id: str, drone_ids: List[str]) -> bool:
        """
        Assign drones to a mission.
        
        Args:
            mission_id: Mission identifier
            drone_ids: List of drone identifiers
            
        Returns:
            True if assignment successful
        """
        if mission_id not in self.missions:
            self.logger.error(f"Mission not found: {mission_id}")
            return False
        
        mission = self.missions[mission_id]
        
        # Verify all drones exist
        for drone_id in drone_ids:
            if drone_id not in self.drones:
                self.logger.error(f"Drone not found: {drone_id}")
                return False
        
        mission.assigned_drones = drone_ids
        mission.status = "active"
        
        # Update drone tasks
        for drone_id in drone_ids:
            self.drones[drone_id].task = mission.mission_type
        
        self.logger.info(f"Mission {mission_id} assigned to {len(drone_ids)} drones")
        return True
    
    def auto_assign_mission(self, mission_id: str) -> bool:
        """
        Automatically assign drones to a mission based on availability and capabilities.
        
        Args:
            mission_id: Mission identifier
            
        Returns:
            True if assignment successful
        """
        if mission_id not in self.missions:
            return False
        
        mission = self.missions[mission_id]
        
        # Find available drones
        available = [
            drone_id for drone_id, drone in self.drones.items()
            if drone.status == "ready" and drone.task == TaskType.IDLE
        ]
        
        if not available:
            self.logger.warning("No available drones for mission assignment")
            return False
        
        # Simple assignment: use first available drone
        # In production, use optimization algorithms
        return self.assign_mission(mission_id, [available[0]])
    
    def complete_mission(self, mission_id: str) -> bool:
        """
        Mark mission as completed.
        
        Args:
            mission_id: Mission identifier
            
        Returns:
            True if successful
        """
        if mission_id not in self.missions:
            return False
        
        mission = self.missions[mission_id]
        mission.status = "completed"
        
        # Free assigned drones
        for drone_id in mission.assigned_drones:
            if drone_id in self.drones:
                self.drones[drone_id].task = TaskType.IDLE
        
        self.logger.info(f"Mission completed: {mission_id}")
        return True
    
    def calculate_separation(self, drone1_id: str, drone2_id: str) -> Optional[float]:
        """
        Calculate separation distance between two drones.
        
        Args:
            drone1_id: First drone identifier
            drone2_id: Second drone identifier
            
        Returns:
            Distance in meters or None
        """
        if drone1_id not in self.drones or drone2_id not in self.drones:
            return None
        
        pos1 = self.drones[drone1_id].position
        pos2 = self.drones[drone2_id].position
        
        # Simple Euclidean distance (in production, use proper geodesic calculation)
        dx = (pos1[0] - pos2[0]) * 111320  # rough lat to meters
        dy = (pos1[1] - pos2[1]) * 111320  # rough lon to meters
        dz = pos1[2] - pos2[2]
        
        return (dx**2 + dy**2 + dz**2)**0.5
    
    def check_collision_risk(self) -> List[Tuple[str, str, float]]:
        """
        Check for collision risks between drones.
        
        Returns:
            List of (drone1_id, drone2_id, distance) tuples for close pairs
        """
        risks = []
        drone_ids = list(self.drones.keys())
        
        for i, id1 in enumerate(drone_ids):
            for id2 in drone_ids[i+1:]:
                distance = self.calculate_separation(id1, id2)
                if distance and distance < self.min_drone_separation:
                    risks.append((id1, id2, distance))
        
        return risks
    
    def optimize_coverage(self, area_bounds: Tuple[float, float, float, float],
                         drone_ids: List[str]) -> Dict[str, Tuple[float, float]]:
        """
        Optimize drone positions for area coverage.
        
        Args:
            area_bounds: Area to cover
            drone_ids: List of drone identifiers
            
        Returns:
            Dictionary mapping drone_id to optimal position
        """
        positions = {}
        
        # In production, use optimization algorithms (e.g., Voronoi tessellation)
        # For now, simple grid distribution
        num_drones = len(drone_ids)
        if num_drones == 0:
            return positions
        
        min_lat, max_lat, min_lon, max_lon = area_bounds
        lat_step = (max_lat - min_lat) / (num_drones + 1)
        
        for i, drone_id in enumerate(drone_ids):
            lat = min_lat + (i + 1) * lat_step
            lon = (min_lon + max_lon) / 2
            positions[drone_id] = (lat, lon)
        
        return positions
    
    def check_inactive_drones(self) -> List[str]:
        """
        Check for drones that haven't sent updates recently.
        
        Returns:
            List of inactive drone IDs
        """
        current_time = time.time()
        inactive = []
        
        for drone_id, drone in self.drones.items():
            if current_time - drone.last_update > self.heartbeat_timeout:
                inactive.append(drone_id)
        
        return inactive
    
    def get_statistics(self) -> Dict:
        """
        Get coordination statistics.
        
        Returns:
            Dictionary with statistics
        """
        active_missions = len([m for m in self.missions.values() if m.status == "active"])
        idle_drones = len([d for d in self.drones.values() if d.task == TaskType.IDLE])
        
        return {
            'total_drones': len(self.drones),
            'idle_drones': idle_drones,
            'active_drones': len(self.drones) - idle_drones,
            'total_missions': len(self.missions),
            'active_missions': active_missions,
            'coordination_mode': self.coordination_mode.value,
            'collision_risks': len(self.check_collision_risk())
        }
