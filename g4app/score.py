from .macro import MacroBuilderWrapper


class ScoreWrapper(MacroBuilderWrapper):
    def __init__(self, name, box_size, n_bins, file_name):
        self.name = name
        self._quantities = []
        self.box_size = box_size                      # (x, y, z) in mm
        self.n_bins = n_bins
        self.file_name = file_name
        self.translation = None                       # [x, y, z] in mm
        self.rotations = ()                           # (("X", 70), ("Z", 10)), in deg

    def add_quantity(self, quantity):
        self._quantities.append(quantity)

    @property
    def before(self):
        commands = [
            "/score/create/boxMesh " + self.name,
            "/score/mesh/boxSize %f %f %f mm" % (self.box_size[0], self.box_size[1], self.box_size[2]),
            "/score/mesh/nBin %d %d %d" % (self.n_bins[0], self.n_bins[1], self.n_bins[2])
        ]
        commands.append("/score/mesh/translate/reset")
        if self.translation is not None:
            # print self.translation
            commands.append("/score/mesh/translate/xyz {} {} {} mm".format(self.translation[0], self.translation[1], self.translation[2]))
        commands.append("/score/mesh/rotate/reset")
        for rotation in self.rotations:
            if rotation[1]: # zero rotation not needed
                commands.append("/score/mesh/rotate/rotate%s %f deg" % (rotation[0].upper(), -rotation[1]))
        # for name, quantity in self._quantities.items():
        #    commands.append("/score/quantity/%s %s" % (quantity, name))
        commands.append("/score/close")
        return commands

    @property
    def after(self):
        commands = []
        # for name, quantity in self._quantities.items():
        #     commands.append("/score/dumpQuantityToFile %s %s %s" % (self.name, name, self.file_name))
        # return commands


class Quantity(object):
    '''Quantities defined by the scoring system.

    See https://geant4.web.cern.ch/geant4/UserDocumentation/UsersGuides/ForApplicationDeveloper/html/AllResources/Control/UIcommands/_score_quantity_.html

    A few of them are simple and can be specified just by name. Others are more complicated, 
    implemented as functions.
    '''
    def __init__(self, qtype, qname, *args):
        self.qtype = qtype
        self.qname = qname
        self.args = args

    def render(self, name):
        return "/score/quantity/"

    energy_deposit = "energyDeposit"
    cell_charge = "cellCharge"
    cell_flux = "cellFlux"
    dose_deposit = "doseDeposit"
    n_of_step = "nOfStep"
    n_of_secondary = "nOfSecondary"



