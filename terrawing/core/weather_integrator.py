"""
Weather Integrator - Integrates real-time weather data

Fetches and processes weather data to inform flight decisions and
ensure safe UAV operations.
"""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import time


class WeatherCondition(Enum):
    """Weather condition categories."""
    CLEAR = "clear"
    PARTLY_CLOUDY = "partly_cloudy"
    CLOUDY = "cloudy"
    LIGHT_RAIN = "light_rain"
    RAIN = "rain"
    HEAVY_RAIN = "heavy_rain"
    SNOW = "snow"
    THUNDERSTORM = "thunderstorm"
    FOG = "fog"
    WINDY = "windy"


class FlightSafety(Enum):
    """Flight safety assessment."""
    SAFE = "safe"
    CAUTION = "caution"
    UNSAFE = "unsafe"
    GROUNDED = "grounded"


@dataclass
class WeatherData:
    """Current weather information."""
    temperature: float  # Celsius
    humidity: float  # Percentage
    wind_speed: float  # m/s
    wind_direction: float  # Degrees
    pressure: float  # hPa
    visibility: float  # meters
    precipitation: float  # mm/hour
    condition: WeatherCondition
    timestamp: float
    location: Tuple[float, float]  # (lat, lon)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'wind_speed': self.wind_speed,
            'wind_direction': self.wind_direction,
            'pressure': self.pressure,
            'visibility': self.visibility,
            'precipitation': self.precipitation,
            'condition': self.condition.value,
            'timestamp': self.timestamp,
            'location': self.location
        }


class WeatherIntegrator:
    """
    Weather data integration system.
    
    Fetches, processes, and analyzes weather data to provide
    flight safety assessments and recommendations.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize weather integrator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.logger = logging.getLogger("TerraWing.WeatherIntegrator")
        
        # API configuration
        self.api_key = self.config.get('api_key', '')
        self.api_endpoint = self.config.get('api_endpoint', '')
        self.update_interval = self.config.get('update_interval', 300)  # 5 minutes
        
        # Safety thresholds
        self.max_wind_speed = self.config.get('max_wind_speed', 12.0)  # m/s
        self.max_gust_speed = self.config.get('max_gust_speed', 15.0)  # m/s
        self.min_visibility = self.config.get('min_visibility', 1000.0)  # meters
        self.max_precipitation = self.config.get('max_precipitation', 2.0)  # mm/hour
        
        # Current weather data
        self.current_weather: Optional[WeatherData] = None
        self.last_update: float = 0.0
        self.forecast_data: List[WeatherData] = []
        
        self.logger.info("Weather Integrator initialized")
    
    def fetch_weather(self, lat: float, lon: float) -> Optional[WeatherData]:
        """
        Fetch current weather data for location.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            WeatherData or None if fetch failed
        """
        try:
            # In production, this would call a weather API (e.g., OpenWeatherMap, NOAA)
            # For now, return simulated data
            
            weather_data = WeatherData(
                temperature=22.0,
                humidity=60.0,
                wind_speed=5.0,
                wind_direction=180.0,
                pressure=1013.0,
                visibility=10000.0,
                precipitation=0.0,
                condition=WeatherCondition.CLEAR,
                timestamp=time.time(),
                location=(lat, lon)
            )
            
            self.current_weather = weather_data
            self.last_update = time.time()
            
            self.logger.info(f"Weather updated for ({lat:.4f}, {lon:.4f})")
            return weather_data
            
        except Exception as e:
            self.logger.error(f"Failed to fetch weather data: {e}")
            return None
    
    def fetch_forecast(self, lat: float, lon: float, hours: int = 24) -> List[WeatherData]:
        """
        Fetch weather forecast.
        
        Args:
            lat: Latitude
            lon: Longitude
            hours: Forecast hours ahead
            
        Returns:
            List of forecasted weather data
        """
        # In production, fetch actual forecast data
        self.forecast_data = []
        self.logger.info(f"Forecast fetched for {hours} hours")
        return self.forecast_data
    
    def get_current_weather(self) -> Optional[WeatherData]:
        """
        Get current weather data.
        
        Returns:
            Current WeatherData or None
        """
        return self.current_weather
    
    def assess_flight_safety(self, weather_data: Optional[WeatherData] = None) -> FlightSafety:
        """
        Assess flight safety based on weather conditions.
        
        Args:
            weather_data: Weather data to assess (uses current if None)
            
        Returns:
            Flight safety assessment
        """
        if weather_data is None:
            weather_data = self.current_weather
        
        if weather_data is None:
            self.logger.warning("No weather data available for safety assessment")
            return FlightSafety.CAUTION
        
        # Check critical conditions
        if weather_data.condition in [WeatherCondition.THUNDERSTORM, WeatherCondition.HEAVY_RAIN]:
            return FlightSafety.GROUNDED
        
        if weather_data.wind_speed > self.max_wind_speed:
            return FlightSafety.GROUNDED
        
        if weather_data.visibility < self.min_visibility:
            return FlightSafety.UNSAFE
        
        if weather_data.precipitation > self.max_precipitation:
            return FlightSafety.UNSAFE
        
        # Check caution conditions
        if weather_data.wind_speed > self.max_wind_speed * 0.75:
            return FlightSafety.CAUTION
        
        if weather_data.condition in [WeatherCondition.RAIN, WeatherCondition.FOG]:
            return FlightSafety.CAUTION
        
        return FlightSafety.SAFE
    
    def is_safe_to_fly(self) -> bool:
        """
        Check if current weather is safe for flight.
        
        Returns:
            True if safe to fly
        """
        safety = self.assess_flight_safety()
        return safety in [FlightSafety.SAFE, FlightSafety.CAUTION]
    
    def get_wind_info(self) -> Optional[Dict]:
        """
        Get detailed wind information.
        
        Returns:
            Dictionary with wind data
        """
        if not self.current_weather:
            return None
        
        return {
            'speed': self.current_weather.wind_speed,
            'direction': self.current_weather.wind_direction,
            'speed_status': 'low' if self.current_weather.wind_speed < 5.0 else 
                          'moderate' if self.current_weather.wind_speed < 10.0 else 'high'
        }
    
    def check_weather_alerts(self) -> List[str]:
        """
        Check for weather alerts and warnings.
        
        Returns:
            List of alert messages
        """
        alerts = []
        
        if not self.current_weather:
            alerts.append("No weather data available")
            return alerts
        
        if self.current_weather.wind_speed > self.max_wind_speed:
            alerts.append(f"High wind speed: {self.current_weather.wind_speed:.1f} m/s")
        
        if self.current_weather.visibility < self.min_visibility:
            alerts.append(f"Low visibility: {self.current_weather.visibility:.0f} m")
        
        if self.current_weather.precipitation > self.max_precipitation:
            alerts.append(f"Heavy precipitation: {self.current_weather.precipitation:.1f} mm/h")
        
        if self.current_weather.condition == WeatherCondition.THUNDERSTORM:
            alerts.append("Thunderstorm warning - Do not fly!")
        
        return alerts
    
    def recommend_flight_window(self, hours_ahead: int = 24) -> List[Tuple[float, float]]:
        """
        Recommend optimal flight time windows based on forecast.
        
        Args:
            hours_ahead: Hours to look ahead
            
        Returns:
            List of (start_time, end_time) tuples for safe flight windows
        """
        windows = []
        
        # In production, analyze forecast data to find safe windows
        if self.is_safe_to_fly():
            current_time = time.time()
            # Suggest current window if safe
            windows.append((current_time, current_time + 3600))  # 1 hour window
        
        return windows
    
    def needs_update(self) -> bool:
        """
        Check if weather data needs updating.
        
        Returns:
            True if update needed
        """
        if not self.current_weather:
            return True
        
        return (time.time() - self.last_update) > self.update_interval
    
    def get_statistics(self) -> Dict:
        """
        Get weather system statistics.
        
        Returns:
            Dictionary with statistics
        """
        stats = {
            'has_current_data': self.current_weather is not None,
            'last_update': self.last_update,
            'forecast_entries': len(self.forecast_data),
            'update_interval': self.update_interval
        }
        
        if self.current_weather:
            stats['current_condition'] = self.current_weather.condition.value
            stats['flight_safety'] = self.assess_flight_safety().value
            stats['safe_to_fly'] = self.is_safe_to_fly()
        
        return stats
