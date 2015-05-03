from .macro import MacroBuilder


class Gui(MacroBuilder):
    '''A simple visualization menu.'''
    @property
    def commands(self):
        return [
            '/gui/addMenu vis Visualization',
            '/gui/addButton vis "Initialize" "/vis/open OGLSQt"',
            '/gui/addButton vis "Draw Volume" "/vis/drawVolume"',
            '/gui/addButton vis "Draw Trajectories" "/vis/scene/add/trajectories"',
            '/gui/addButton vis "Draw Axes" "/vis/scene/add/axes 0 0 0 1 m"',

            '/gui/addMenu run Run',
            '/gui/addButton run "BeamOn 1" "/run/beamOn 1"',
            '/gui/addButton run "BeamOn 10" "/run/beamOn 10"',
            '/gui/addButton run "BeamOn 100" "/run/beamOn 100"',
            '/gui/addButton run "BeamOn 1000" "/run/beamOn 1000"',
        ]