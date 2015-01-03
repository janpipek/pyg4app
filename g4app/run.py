from .macro import CompositeMacroBuilder


class G4Run(CompositeMacroBuilder):
    def __init__(self, events):
        super(G4Run, self).__init__()
        self.events = events

    def render_self(self):
        return ["/run/beamOn %d" % self.events]