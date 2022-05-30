# AI-in-Airsim-Simulator
In this project, I was able to drive a car in Airsim simulator without using the keyboard. 
AirSim is a simulator for drones, cars and more, built on Unreal Engine. It is open-source, cross platform, and supports software-in-the-loop simulation with popular flight controllers such as PX4 & ArduPilot and hardware-in-loop with PX4 for physically and visually realistic simulations. It is developed as an Unreal plugin that can simply be dropped into any Unreal environment.
In order to achieve the desired goal, i used the MediaPipe for hand detection. MediaPipe Hands utilizes an ML pipeline consisting of multiple models working together: A palm detection model that operates on the full image and returns an oriented hand bounding box. A hand landmark model that operates on the cropped image region defined by the palm detector and returns high-fidelity 3D hand keypoints. 

1-Download AirSimNH Simulator:
In order to achieve that, all you have to do is download it directly from this link provided by Microsoft
