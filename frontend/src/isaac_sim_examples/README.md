# Isaac Sim Examples - Manual Steps

This directory contains examples for setting up environments and generating synthetic data in NVIDIA Isaac Sim. Due to Isaac Sim's nature as a graphical application with its own Python environment, these scripts are typically developed and run within the Isaac Sim Editor.

## Steps to Run/Develop:

1.  **Launch Isaac Sim**: Open the NVIDIA Omniverse Launcher and start Isaac Sim.
2.  **Open Project**: Load or create your project within Isaac Sim.
3.  **Access Script Editor**: Go to `Window -> Script Editor` in Isaac Sim.
4.  **Load/Develop Script**:
    *   You can load `.py` files from this directory into the script editor.
    *   Develop new scripts directly in the editor and save them here.
5.  **Run Simulation**: Use the play/pause controls in Isaac Sim to run the simulation and observe script behavior.

## Script Examples:

-   `simple_perception_env.py`: Sets up a basic scene with a camera and objects, suitable for perception tasks.
-   `humanoid_nav_env.py`: Sets up a humanoid robot in a navigation environment, suitable for Nav2 integration.
