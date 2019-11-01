#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.gua
from avango.script import field_has_changed

# import application libraries
from lib.GuaVE import GuaVE

# constant pixel resolution of the window to display the render result
WINDOW_RESOLUTION = avango.gua.Vec2ui(1920, 1080)

# renders the given scenegraph
class Renderer:

    def __init__(self, scenegraph, viewing_setup):
        # window
        self.window = avango.gua.nodes.GlfwWindow(Title="window")
        self.window.Size.value = WINDOW_RESOLUTION
        self.window.LeftResolution.value = self.window.Size.value
        viewing_setup.register_window(self.window)

        # viewer
        self.viewer = avango.gua.nodes.Viewer()
        self.viewer.SceneGraphs.value = [scenegraph]
        self.viewer.Windows.value = [self.window]
        self.viewer.DesiredFPS.value = 250.0

        # render pipeline description
        self.pipeline_description = avango.gua.nodes.PipelineDescription(Passes=[
        ])
        self.pipeline_description.EnableABuffer.value = False
        self.pipeline_description.Passes.value.append(
            avango.gua.nodes.TriMeshPassDescription())
        self.pipeline_description.Passes.value.append(
            avango.gua.nodes.LightVisibilityPassDescription())

        self.resolve_pass = avango.gua.nodes.ResolvePassDescription()
        self.resolve_pass.EnvironmentLightingColor.value = avango.gua.Color(
            0.1, 0.1, 0.1)
        self.resolve_pass.ToneMappingMode.value = avango.gua.ToneMappingMode.UNCHARTED
        self.resolve_pass.Exposure.value = 1.0
        self.resolve_pass.EnableSSAO.value = True
        self.resolve_pass.SSAOIntensity.value = 4.0
        self.resolve_pass.SSAOFalloff.value = 10.0
        self.resolve_pass.SSAORadius.value = 7.0
        self.resolve_pass.BackgroundMode.value = avango.gua.BackgroundMode.SKYMAP_TEXTURE
        self.resolve_pass.BackgroundTexture.value = "data/textures/water-painted.jpg"

        self.pipeline_description.Passes.value.append(self.resolve_pass)
        self.pipeline_description.Passes.value.append(
            avango.gua.nodes.SSAAPassDescription())
        viewing_setup.register_pipeline_description(self.pipeline_description)

        # init fps toggler
        self.fps_toggler = FPSToggler()
        self.fps_toggler.set_viewer(self.viewer)

        # interactive shell
        self.interactive_shell = GuaVE()

    # blocking function: enters the main application loop of avango-guacamole
    def run(self, local_variables, global_variables):
        self.interactive_shell.start(local_variables, global_variables)
        self.viewer.run()

# Field Container toggling between normal and slow framerate on button press
class FPSToggler(avango.script.Script):

    # input field
    sf_fps_toggle = avango.SFBool()
    sf_fps_toggle.value = False

    def __init__(self):
        self.super(FPSToggler).__init__()
        self.viewer = None

        # init keyboard sensor for fps toggle
        self.device_service = avango.daemon.DeviceService()
        self.keyboard_sensor = avango.daemon.nodes.DeviceSensor(
            DeviceService=self.device_service)
        self.keyboard_sensor.Station.value = 'gua-device-keyboard'
        self.sf_fps_toggle.connect_from(self.keyboard_sensor.Button4)

    # sets the viewer on which fps changes are to be toggled
    def set_viewer(self, viewer):
        self.viewer = viewer

    # called whenever sf_fps_toggle changes
    @field_has_changed(sf_fps_toggle)
    def sf_fps_toggle_changed(self):
        if self.sf_fps_toggle.value and self.viewer is not None:
            if self.viewer.DesiredFPS.value > 20.0:
                print("Slow framerate activated")
                self.viewer.DesiredFPS.value = 20.0
            else:
                print("Normal framerate activated")
                self.viewer.DesiredFPS.value = 250.0
