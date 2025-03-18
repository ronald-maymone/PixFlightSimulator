"""
| File: ui_delegate.py
| Author: Marcelo Jacinto (marcelo.jacinto@tecnico.ulisboa.pt)
| Pix Force version: Ronald M. (ronald.maymone@pixforce.ai)
| License: BSD-3-Clause. Copyright (c) 2023, Marcelo Jacinto. All rights reserved.
| Description: Definition of the UiDelegate which is an abstraction layer betweeen the extension UI and code logic features
"""

# External packages
import os
import asyncio
from scipy.spatial.transform import Rotation

# Omniverse extensions
import carb
import omni.ui as ui

# Extension Configurations
from pegasus.simulator.params import ROBOTS, SIMULATION_ENVIRONMENTS, BACKENDS, WORLD_SETTINGS
from pegasus.simulator.logic.interface.pegasus_interface import PegasusInterface

# Vehicle Manager to spawn Vehicles
from pegasus.simulator.logic.backends import Backend, BackendConfig, PX4MavlinkBackend, PX4MavlinkBackendConfig, ArduPilotMavlinkBackend, ArduPilotMavlinkBackendConfig
from pegasus.simulator.logic.vehicles.multirotor import Multirotor, MultirotorConfig
from pegasus.simulator.logic.vehicle_manager import VehicleManager
from pegasus.simulator.logic.graphical_sensors.monocular_camera import MonocularCamera

try:
    from pegasus.simulator.logic.backends import ROS2Backend
    ROS2_available = True
except ImportError:
    ROS2_available = False
    carb.log_warn("ROS2 backend not available. Please install the ROS2 extension to use this feature.")


class PixUiDelegate:
    """
    Object that will interface between the logic/dynamic simulation part of the extension and the Widget UI
    """

    def __init__(self):

        # The window that will be bound to this delegate
        self._window = None

        # Get an instance of the pegasus simulator
        self._pegasus_sim: PegasusInterface = PegasusInterface()

        # Attribute that holds the currently selected scene from the dropdown menu
        self._scene_dropdown: ui.AbstractItemModel = None
        self._scene_names = list(SIMULATION_ENVIRONMENTS.keys())

        # Selected latitude, longitude and altitude
        self._latitude_field: ui.AbstractValueModel = None
        self._latitude = PegasusInterface().latitude
        self._longitude_field: ui.AbstractValueModel = None
        self._longitude = PegasusInterface().longitude
        self._altitude_field: ui.AbstractValueModel = None
        self._altitude = PegasusInterface().altitude

        # Attribute that hold the currently selected vehicle from the dropdown menu
        self._vehicle_dropdown: ui.AbstractItemModel = None
        self._vehicles_names = list(ROBOTS.keys())

        # Get an instance of the vehicle manager
        self._vehicle_manager = VehicleManager()

        # Selected option for broadcasting the simulated vehicle (PX4+ROS2 or just ROS2)
        # By default we assume PX4
        self._streaming_backend: str = BACKENDS['px4']

        # Selected value for the the id of the vehicle
        self._vehicle_id_field: ui.AbstractValueModel = None
        self._vehicle_id: int = 0

        # Attribute that will save the model for the px4-autostart checkbox
        self._px4_autostart_checkbox: ui.AbstractValueModel = None
        self._autostart_px4: bool = True

        # Atributes to store the path for the Px4 directory
        self._px4_directory_field: ui.AbstractValueModel = None
        self._px4_dir: str = PegasusInterface().px4_path

        # Atributes to store the PX4 airframe
        self._px4_airframe_field: ui.AbstractValueModel = None
        self._px4_airframe: str = self._pegasus_sim.px4_default_airframe

        # Attribute that will save the model for the ardupilot-autostart checkbox
        self._ardupilot_autostart_checkbox: ui.AbstractValueModel = None
        self._autostart_ardupilot: bool = True

        # Atributes to store the path for the ArduPilot directory
        self._ardupilot_directory_field: ui.AbstractValueModel = None
        self._ardupilot_dir: str = PegasusInterface().ardupilot_path

        # Atributes to store the ArduPilot airframe
        self._ardupilot_airframe_field: ui.AbstractValueModel = None
        self._ardupilot_airframe: str = self._pegasus_sim.ardupilot_default_airframe

    def set_window_bind(self, window):
        self._window = window

    def set_scene_dropdown(self, scene_dropdown_model: ui.AbstractItemModel):
        self._scene_dropdown = scene_dropdown_model
    
    def set_latitude_field(self, latitude_model: ui.AbstractValueModel):
        self._latitude_field = latitude_model
    
    def set_longitude_field(self, longitude_model: ui.AbstractValueModel):
        self._longitude_field = longitude_model

    def set_altitude_field(self, altitude_model: ui.AbstractValueModel):
        self._altitude_field = altitude_model

    def set_vehicle_dropdown(self, vehicle_dropdown_model: ui.AbstractItemModel):
        self._vehicle_dropdown = vehicle_dropdown_model

    def set_vehicle_id_field(self, vehicle_id_field: ui.AbstractValueModel):
        self._vehicle_id_field = vehicle_id_field

    def set_streaming_backend(self, backend: str = BACKENDS['px4']):
        self._streaming_backend = backend

    def set_px4_autostart_checkbox(self, checkbox_model:ui.AbstractValueModel):
        self._px4_autostart_checkbox = checkbox_model

    def set_px4_directory_field(self, directory_field_model: ui.AbstractValueModel):
        self._px4_directory_field = directory_field_model

    def set_px4_airframe_field(self, airframe_field_model: ui.AbstractValueModel):
        self._px4_airframe_field = airframe_field_model
    
    def set_ardupilot_autostart_checkbox(self, checkbox_model: ui.AbstractValueModel):
        self._ardupilot_autostart_checkbox = checkbox_model

    def set_ardupilot_directory_field(self, directory_field_model: ui.AbstractValueModel):
        self._ardupilot_directory_field = directory_field_model

    def set_ardupilot_airframe_field(self, airframe_field_model: ui.AbstractValueModel):
        self._ardupilot_airframe_field = airframe_field_model

    def on_takeoff_button_click(self):
        pass

    def on_land_button_click(self):
        pass
