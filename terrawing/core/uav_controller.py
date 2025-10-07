"""
UAV Controller - Main controller for drone operations

Handles flight control, navigation, and coordination with other modules.
"""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class FlightMode(Enum):
    """UAV flight modes."""
    IDLE = "idle"
    MANUAL = "manual"
    AUTO = "auto"
    WAYPOINT = "waypoint"
    RTL = "return_to_launch"
    LANDING = "landing"


class FlightStatus(Enum):
    """UAV flight status."""
    GROUNDED = "grounded"
    TAKING_OFF = "taking_off"
    FLYING = "flying"
    HOVERING = "hovering"
    LANDING = "landing"
    EMERGENCY = "emergency"


@dataclass
class UAVState:
    """Current state of the UAV."""
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)  # (lat, lon, alt)
    velocity: Tuple[float, float, float] = (0.0, 0.0, 0.0)  # (vx, vy, vz)
    orientation: Tuple[float, float, float] = (0.0, 0.0, 0.0)  # (roll, pitch, yaw)
    battery_level: float = 100.0
    flight_mode: FlightMode = FlightMode.IDLE
    flight_status: FlightStatus = FlightStatus.GROUNDED
    is_armed: bool = False
    obstacles_detected: List[Dict] = field(default_factory=list)
    
    def __repr__(self):
        return (f"UAVState(pos={self.position}, mode={self.flight_mode.value}, "
                f"status={self.flight_status.value}, battery={self.battery_level:.1f}%)")


class UAVController:
    """
    Main controller for UAV operations.
    
    Manages flight control, navigation, and integration with detection systems.
    """
    
    def __init__(self, uav_id: str = "UAV-01", config: Optional[Dict] = None):
        """
        Initialize UAV controller.
        
        Args:
            uav_id: Unique identifier for this UAV
            config: Configuration dictionary
        """
        self.uav_id = uav_id
        self.config = config or {}
        self.state = UAVState()
        self.logger = logging.getLogger(f"TerraWing.{uav_id}")
        
        # Safety parameters
        self.min_altitude = self.config.get('min_altitude', 5.0)
        self.max_altitude = self.config.get('max_altitude', 120.0)
        self.safe_battery_threshold = self.config.get('safe_battery', 20.0)
        self.emergency_land_battery = self.config.get('emergency_battery', 10.0)
        
        self.logger.info(f"UAV Controller initialized: {uav_id}")
    
    def arm(self) -> bool:
        """
        Arm the UAV for flight.
        
        Returns:
            True if armed successfully, False otherwise
        """
        if self.state.battery_level < self.safe_battery_threshold:
            self.logger.warning(f"Cannot arm: Battery too low ({self.state.battery_level}%)")
            return False
        
        if self.state.is_armed:
            self.logger.info("UAV already armed")
            return True
        
        self.state.is_armed = True
        self.logger.info("UAV armed successfully")
        return True
    
    def disarm(self) -> bool:
        """
        Disarm the UAV.
        
        Returns:
            True if disarmed successfully
        """
        if self.state.flight_status not in [FlightStatus.GROUNDED, FlightStatus.LANDING]:
            self.logger.warning("Cannot disarm while flying")
            return False
        
        self.state.is_armed = False
        self.state.flight_mode = FlightMode.IDLE
        self.logger.info("UAV disarmed")
        return True
    
    def takeoff(self, target_altitude: float = 10.0) -> bool:
        """
        Initiate takeoff sequence.
        
        Args:
            target_altitude: Target altitude in meters
            
        Returns:
            True if takeoff initiated successfully
        """
        if not self.state.is_armed:
            self.logger.error("Cannot takeoff: UAV not armed")
            return False
        
        if target_altitude < self.min_altitude or target_altitude > self.max_altitude:
            self.logger.error(f"Invalid altitude: {target_altitude}m (range: {self.min_altitude}-{self.max_altitude}m)")
            return False
        
        self.state.flight_status = FlightStatus.TAKING_OFF
        self.state.flight_mode = FlightMode.AUTO
        self.logger.info(f"Takeoff initiated to {target_altitude}m")
        
        # Simulate reaching altitude
        self.state.position = (self.state.position[0], self.state.position[1], target_altitude)
        self.state.flight_status = FlightStatus.HOVERING
        
        return True
    
    def land(self) -> bool:
        """
        Initiate landing sequence.
        
        Returns:
            True if landing initiated successfully
        """
        if self.state.flight_status == FlightStatus.GROUNDED:
            self.logger.info("Already on ground")
            return True
        
        self.state.flight_status = FlightStatus.LANDING
        self.logger.info("Landing sequence initiated")
        
        # Simulate landing
        self.state.position = (self.state.position[0], self.state.position[1], 0.0)
        self.state.flight_status = FlightStatus.GROUNDED
        self.state.flight_mode = FlightMode.IDLE
        
        return True
    
    def set_flight_mode(self, mode: FlightMode) -> bool:
        """
        Set the flight mode.
        
        Args:
            mode: Target flight mode
            
        Returns:
            True if mode set successfully
        """
        if not self.state.is_armed and mode != FlightMode.IDLE:
            self.logger.warning("Cannot change mode: UAV not armed")
            return False
        
        old_mode = self.state.flight_mode
        self.state.flight_mode = mode
        self.logger.info(f"Flight mode changed: {old_mode.value} -> {mode.value}")
        return True
    
    def navigate_to(self, lat: float, lon: float, alt: float) -> bool:
        """
        Navigate to specified coordinates.
        
        Args:
            lat: Target latitude
            lon: Target longitude
            alt: Target altitude
            
        Returns:
            True if navigation successful
        """
        if self.state.flight_status not in [FlightStatus.FLYING, FlightStatus.HOVERING]:
            self.logger.warning("Cannot navigate: Not in flight")
            return False
        
        if alt < self.min_altitude or alt > self.max_altitude:
            self.logger.error(f"Invalid altitude: {alt}m")
            return False
        
        self.logger.info(f"Navigating to ({lat:.6f}, {lon:.6f}, {alt}m)")
        self.state.position = (lat, lon, alt)
        self.state.flight_status = FlightStatus.FLYING
        
        return True
    
    def return_to_launch(self) -> bool:
        """
        Return to launch position.
        
        Returns:
            True if RTL initiated successfully
        """
        if self.state.flight_status == FlightStatus.GROUNDED:
            return True
        
        self.state.flight_mode = FlightMode.RTL
        self.logger.info("Return to launch initiated")
        
        # In a real system, this would navigate back to home position
        return self.land()
    
    def emergency_stop(self) -> bool:
        """
        Trigger emergency stop and landing.
        
        Returns:
            True if emergency procedure initiated
        """
        self.logger.critical("EMERGENCY STOP ACTIVATED")
        self.state.flight_status = FlightStatus.EMERGENCY
        self.state.flight_mode = FlightMode.RTL
        return self.land()
    
    def update_battery(self, level: float) -> None:
        """
        Update battery level and check for critical conditions.
        
        Args:
            level: Battery level percentage (0-100)
        """
        self.state.battery_level = max(0.0, min(100.0, level))
        
        if self.state.battery_level < self.emergency_land_battery:
            self.logger.critical(f"Critical battery level: {self.state.battery_level}%")
            if self.state.flight_status != FlightStatus.GROUNDED:
                self.emergency_stop()
        elif self.state.battery_level < self.safe_battery_threshold:
            self.logger.warning(f"Low battery: {self.state.battery_level}%")
    
    def get_state(self) -> UAVState:
        """
        Get current UAV state.
        
        Returns:
            Current UAVState
        """
        return self.state
    
    def get_telemetry(self) -> Dict:
        """
        Get telemetry data.
        
        Returns:
            Dictionary with telemetry information
        """
        return {
            'uav_id': self.uav_id,
            'position': self.state.position,
            'velocity': self.state.velocity,
            'orientation': self.state.orientation,
            'battery_level': self.state.battery_level,
            'flight_mode': self.state.flight_mode.value,
            'flight_status': self.state.flight_status.value,
            'is_armed': self.state.is_armed,
            'obstacles_detected': len(self.state.obstacles_detected)
        }
