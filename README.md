TerraWing – AI-Powered UAV Obstacle Detection for Agriculture

TerraWing is an intelligent drone-based solution designed to enhance efficiency, safety, and automation in the agro-industrial sector. It provides a service for real-time obstacle recognition, classification, and terrain mapping to assist unmanned aerial vehicles (UAVs) operating in agricultural environments. The project leverages modern computer vision, deep learning, and server-integrated AI modules to ensure reliable performance under diverse conditions.

Overview

The agricultural industry increasingly depends on UAVs for crop monitoring, irrigation planning, pesticide spraying, and land analysis. However, drones face numerous challenges, such as unpredictable terrain, moving obstacles, and weather fluctuations. TerraWing addresses these challenges by creating a robust system that can intelligently detect, classify, and respond to obstacles in the UAV’s path — ensuring safer and more autonomous drone operations.

Built using modern Python-based tools, the system offers high performance, scalability, and modularity, making it adaptable to various agricultural applications. The project has been developed up to the Minimum Viable Product (MVP) stage and includes a complete workflow — from model training to real-time server testing.

Key Features

Real-Time Obstacle Detection:
Uses advanced neural networks to identify and classify objects or barriers during UAV flight.

Specialized Dataset:
A custom agricultural obstacle dataset is used to train and fine-tune models for field environments.

AI Server Plugins:
Modular AI plugins enable flexible task management and easy integration of additional features.

Automatic Terrain Mapping:
Generates interactive maps of the UAV’s working area for better path planning and analytics.

Multi-Drone Coordination:
Supports collaborative operation of multiple UAVs for large-scale field management.

Weather Integration:
Connects with live weather APIs to optimize drone navigation and ensure safe operation.

Technology Stack

Programming Language: Python (≥ 3.11)

Package Management: Poetry

Version Control: Pyenv for Python environments

Frameworks & Libraries:
OpenCV, PyTorch/TensorFlow, FastAPI/Flask, NumPy, Pandas, Matplotlib

Linting & Formatting: Ruff and Black

Testing Tools: Custom drone emulator and video stream simulator

Development and Usage

TerraWing includes full setup documentation for environment configuration using Pyenv and Poetry, ensuring consistency across development environments.
Developers can easily test the system using the built-in drone simulator (test_video_stream.py) to emulate real-time video streaming — from prerecorded files or a live webcam feed.

The model training notebook (TrainNeuralNetwork.ipynb) allows users to experiment with the Kaggle dataset, Obstacles in Flight for Drones
, enabling customization of detection accuracy and performance tuning.

The system can be deployed locally or on a remote server to process UAV feeds, generate terrain maps, and integrate sensor or weather data.

License

This project is distributed under the Creative Commons BY-NC 4.0 License, allowing users to share, adapt, and use the project non-commercially with proper attribution.

Future Scope

Planned enhancements include:

Integration with 3D LiDAR sensors

Improved multi-drone synchronization

Onboard AI inference for edge devices

Cloud-based analytics dashboard

Conclusion

TerraWing is more than a UAV system — it’s a step toward smarter, safer, and data-driven agriculture.
By combining AI, automation, and drone technology, TerraWing paves the way for a new era of precision farming.
