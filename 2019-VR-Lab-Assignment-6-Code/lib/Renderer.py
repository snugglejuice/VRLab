#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.gua
import avango.vive

# import python libraries
import sys

# renders the given scenegraph
class Renderer:

    def __init__(self, scenegraph, viewing_setup):
        # window
        if sys.platform.startswith('win'):
            self.window = avango.vive.nodes.ViveWindow()
            self.window.Size.value = self.window.Resolution.value
            self.window.EnableVsync.value = False
            self.window.EnableFullscreen.value = False

        viewing_setup.register_window(self.window)

        # viewer
        self.viewer = avango.gua.nodes.Viewer()
        self.viewer.SceneGraphs.value = [scenegraph]
        self.viewer.Windows.value = [self.window]
        self.viewer.DesiredFPS.value = 2000.0

        # render pipeline description
        self.pipeline_description = avango.gua.nodes.PipelineDescription(Passes=[
        ])
        self.pipeline_description.EnableABuffer.value = False
        self.pipeline_description.Passes.value.append(
            avango.gua.nodes.LineStripPassDescription())
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
        if not sys.platform.startswith('win'):
            from lib.GuaVE import GuaVE
            self.interactive_shell = GuaVE()

    # blocking function: enters the main application loop of avango-guacamole
    def run(self, local_variables, global_variables):
        if not sys.platform.startswith('win'):
            self.interactive_shell.start(local_variables, global_variables)
        self.viewer.run()
