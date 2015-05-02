from .macro import WrappedMacroBuilder


class G4Run(WrappedMacroBuilder):
    def __init__(self, events):
        super(G4Run, self).__init__()
        self.events = events
        self.add_command("/run/beamOn %d" % self.events)

    def add_scorer(self, scorer):
    	# TODO: type checking?
    	self.wrap(scorer)