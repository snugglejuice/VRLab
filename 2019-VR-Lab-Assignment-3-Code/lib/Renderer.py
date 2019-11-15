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
        self.pipeline_description = avango.gua.nodes.PipelineDescription(Passes=[])
        self.pipeline_description.EnableABuffer.value = False
        self.pipeline_description.Passes.value.append(
            avango.gua.nodes.TriMeshPassDescription())
        self.pipeline_description.Passes.value.append(
            avango.gua.nodes.LightVisibilityPassDescription())

        self.resolve_pass = avango.gua.nodes.ResolvePassDescription()
        self.resolve_pass.EnvironmentLightingColor.value = avango.gua.Color(
            0.2, 0.2, 0.2)
        self.resolve_pass.ToneMappingMode.value = avango.gua.ToneMappingMode.UNCHARTED
        self.resolve_pass.Exposure.value = 1.0
        self.resolve_pass.EnableSSAO.value = True
        self.resolve_pass.SSAOIntensity.value = 2.0
        self.resolve_pass.SSAOFalloff.value = 1.0
        self.resolve_pass.SSAORadius.value = 10.0
        self.resolve_pass.BackgroundMode.value = avango.gua.BackgroundMode.SKYMAP_TEXTURE
        self.resolve_pass.BackgroundTexture.value = "data/textures/water-painted.jpg"

        self.pipeline_description.Passes.value.append(self.resolve_pass)
        self.pipeline_description.Passes.value.append(
            avango.gua.nodes.SSAAPassDescription())
        viewing_setup.register_pipeline_description(self.pipeline_description)

        # interactive shell
        self.interactive_shell = GuaVE()

    # blocking function: enters the main application loop of avango-guacamole
    def run(self, local_variables, global_variables):
        self.interactive_shell.start(local_variables, global_variables)
        self.viewer.run()
