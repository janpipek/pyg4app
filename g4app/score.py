from .macro import MacroBuilderWrapper

from functools import partial

class ScoreWrapper(MacroBuilderWrapper):
    def __init__(self, name, box_size, n_bins, file_name):
        self.name = name
        self.quantities = []
        self.box_size = box_size                      # (x, y, z) in mm
        self.n_bins = n_bins
        self.file_name = file_name
        self.translation = None                       # [x, y, z] in mm
        self.rotations = ()                           # (("X", 70), ("Z", 10)), in deg

    def add_quantity(self, quantity):
        self.quantities.append(quantity)

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
        commands.extend(self.quantities)
        commands.append("/score/close")
        return commands

    @property
    def after(self):
        commands = []
        for quantity in self.quantities:
            commands.append("/score/dumpQuantityToFile %s %s %s" % (self.name, quantity.qname, self.file_name))
        return commands


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

    def render(self):
        return "/score/quantity/%s %s %s" % (self.qtype, " ".join(self.args), self.qname)


class quantities(object):
    """Static class with defined scoring quantities."""
    energyDeposit = energy_deposit = partial(Quantity, "energyDeposit")
    cellCharge = cell_charge = partial(Quantity, "cellCharge")
    cellFlux = cell_flux = partial(Quantity, "cellFlux")
    doseDeposit = dose_deposit = partial(Quantity, "doseDeposit")




