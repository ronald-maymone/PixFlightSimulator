import omni.ui as ui
from pegasus.simulator.params import ROBOTS, SIMULATION_ENVIRONMENTS, THUMBNAIL, BACKENDS, WORLD_THUMBNAIL, WINDOW_TITLE, BACKENDS_THUMBMAILS


class PixWidgetWindow(ui.Window):

    LABEL_PADDING = 120
    BUTTON_HEIGHT = 50
    GENERAL_SPACING = 5

    WINDOW_WIDTH = 325
    WINDOW_HEIGHT = 850

    BUTTON_SELECTED_STYLE = {
        "Button": {
            "background_color": cl("#3780ae"),
            "border_color": cl("#29587c"),
            "border_width": 2,
            "border_radius": 5,
            "padding": 2,
        }
    }

    BUTTON_BASE_STYLE = {
        "Button": {
            "background_color": cl("#292929"),
            "border_color": cl("#292929"),
            "border_width": 2,
            "border_radius": 5,
            "padding": 5,
        }
    }

    def __init__(self, title, width, height):
        """
        Constructor for the Window UI widget of the extension. Receives as input a UIDelegate that implements
        all the callbacks to handle button clicks, drop-down menu actions, etc. (abstracting the interface between
        the logic of the code and the ui)
        """

        
        # Setup the base widget window
        super().__init__(
            WINDOW_TITLE, width=WidgetWindow.WINDOW_WIDTH, height=WidgetWindow.WINDOW_HEIGHT, visible=True, **kwargs
        )
        self.deferred_dock_in("Property", ui.DockPolicy.CURRENT_WINDOW_IS_ACTIVE)

        # Setup the delegate that will bridge between the logic and the UI
        self._delegate = delegate

        # Bind the UI delegate to this window
        self._delegate.set_window_bind(self)

        # Auxiliar attributes for getting the transforms of the vehicle and the camera from the UI
        self._camera_transform_models = []
        self._vehicle_transform_models = []

        # Build the actual window UI
        self._build_window()

    def destroy(self):

        # Clear the world and the stage correctly
        self._delegate.on_clear_scene()

        # It will destroy all the children
        super().destroy()

    def _build_window(self):
        # Define the UI of the widget window
        with self.frame:
            with ui.ScrollingFrame(horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_ON, vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_ON):

                # Vertical Stack of menus
                with ui.VStack():
                    # Create a frame for selecting which backend to load
                    self._flight_control_frame()
                    ui.Spacer(height=5)


    def _flight_control_frame(self):
        """
        Method that creates the frame for the flight control of the drone
        """
        with ui.VStack():
            # Takeoff and Land buttons
            with ui.HStack():
                self._takeoff_button = ui.Button("Takeoff", style=WidgetWindow.BUTTON_BASE_STYLE)
                self._takeoff_button.set_on_click(self._delegate.on_takeoff_button_click)
                self._land_button = ui.Button("Land", style=WidgetWindow.BUTTON_BASE_STYLE)
                self._land_button.set_on_click(self._delegate.on_land_button_click)


    def get_selected_vehicle_attitude(self):

        # Extract the vehicle desired position and orientation for spawning
        if len(self._vehicle_transform_models) == 6:
            vehicle_pos = np.array([self._vehicle_transform_models[i].get_value_as_float() for i in range(3)])
            vehicel_orientation = np.array(
                [self._vehicle_transform_models[i].get_value_as_float() for i in range(3, 6)]
            )
            return vehicle_pos, vehicel_orientation

        return None, None

    def get_selected_camera_pos(self):
        """
        Method that returns the currently selected camera position in the camera transform widget
        """

        # Extract the camera desired position and the target it is pointing to
        if len(self._camera_transform_models) == 6:
            camera_pos = np.array([self._camera_transform_models[i].get_value_as_float() for i in range(3)])
            camera_target = np.array([self._camera_transform_models[i].get_value_as_float() for i in range(3, 6)])
            return camera_pos, camera_target

        return None, None