from .macro import MacroBuilder


class Gui(MacroBuilder):
    '''A simple visualization menu.'''
    @property
    def commands(self):
        return [
            '/gui/addMenu vis Visualization',
            '/gui/addButton vis "Initialize" "/vis/open OGLSQt"',
            '/gui/addButton vis "Draw Volume" "/vis/drawVolume"',
            '/gui/addButton vis "Draw Axes" "/vis/scene/add/axes 0 0 0 1 m"'
        ]