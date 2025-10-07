"""
Multi-drone coordination example.

Demonstrates multi-drone coordination and mission planning.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from terrawing import DroneCoordinator
from terrawing.core.drone_coordinator import TaskType
from terrawing.utils import setup_logging


def main():
    """Run multi-drone coordination example."""
    
    setup_logging(level="INFO")
    print("=" * 60)
    print("TerraWing - Multi-Drone Coordination Example")
    print("=" * 60)
    
    # Initialize coordinator
    print("\n[1] Initializing Drone Coordinator...")
    coordinator = DroneCoordinator()
    
    # Register multiple drones
    print("\n[2] Registering Drone Fleet...")
    drone_positions = [
        ("UAV-001", (40.050, -75.000, 0.0), {"camera", "lidar"}),
        ("UAV-002", (40.051, -75.001, 0.0), {"camera", "multispectral"}),
        ("UAV-003", (40.052, -75.002, 0.0), {"camera", "thermal"}),
    ]
    
    for drone_id, position, capabilities in drone_positions:
        coordinator.register_drone(drone_id, position, set(capabilities))
        print(f"    ✓ Registered {drone_id} with capabilities: {capabilities}")
    
    # Display fleet info
    print(f"\n    Fleet Size: {len(coordinator.drones)}")
    
    # Create missions
    print("\n[3] Creating Missions...")
    
    # Survey mission
    survey_mission = coordinator.create_mission(
        mission_type=TaskType.SURVEY,
        area_bounds=(40.05, 40.06, -75.00, -74.99),
        priority=1
    )
    print(f"    ✓ Created {survey_mission.mission_id}: {survey_mission.mission_type.value}")
    
    # Monitoring mission
    monitor_mission = coordinator.create_mission(
        mission_type=TaskType.MONITORING,
        area_bounds=(40.06, 40.07, -75.01, -75.00),
        priority=2
    )
    print(f"    ✓ Created {monitor_mission.mission_id}: {monitor_mission.mission_type.value}")
    
    # Assign missions
    print("\n[4] Assigning Missions...")
    
    # Manual assignment
    coordinator.assign_mission(survey_mission.mission_id, ["UAV-001", "UAV-002"])
    print(f"    ✓ {survey_mission.mission_id} assigned to UAV-001, UAV-002")
    
    # Auto assignment
    coordinator.auto_assign_mission(monitor_mission.mission_id)
    assigned_drone = monitor_mission.assigned_drones[0] if monitor_mission.assigned_drones else "None"
    print(f"    ✓ {monitor_mission.mission_id} auto-assigned to {assigned_drone}")
    
    # Optimize coverage
    print("\n[5] Optimizing Coverage...")
    optimal_positions = coordinator.optimize_coverage(
        area_bounds=(40.05, 40.06, -75.00, -74.99),
        drone_ids=["UAV-001", "UAV-002"]
    )
    
    print("    Optimal positions:")
    for drone_id, position in optimal_positions.items():
        print(f"      {drone_id}: ({position[0]:.6f}, {position[1]:.6f})")
    
    # Check for collision risks
    print("\n[6] Checking Collision Risks...")
    risks = coordinator.check_collision_risk()
    if risks:
        print(f"    ⚠ Found {len(risks)} collision risks:")
        for drone1, drone2, distance in risks:
            print(f"      {drone1} <-> {drone2}: {distance:.1f}m")
    else:
        print("    ✓ No collision risks detected")
    
    # Display fleet statistics
    print("\n[7] Fleet Statistics:")
    stats = coordinator.get_statistics()
    print(f"    Total Drones: {stats['total_drones']}")
    print(f"    Active Drones: {stats['active_drones']}")
    print(f"    Idle Drones: {stats['idle_drones']}")
    print(f"    Total Missions: {stats['total_missions']}")
    print(f"    Active Missions: {stats['active_missions']}")
    
    # Complete missions
    print("\n[8] Completing Missions...")
    coordinator.complete_mission(survey_mission.mission_id)
    print(f"    ✓ {survey_mission.mission_id} completed")
    
    coordinator.complete_mission(monitor_mission.mission_id)
    print(f"    ✓ {monitor_mission.mission_id} completed")
    
    print("\n" + "=" * 60)
    print("Multi-drone coordination demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
