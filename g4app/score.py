from .macro import MacroBuilder


class ScoreWrapper(object):
    def __init__(self, name, box_size, n_bin, file_name):
        self.name = name
        self._quantities = {}
        self.box_size = box_size                      # (x, y, z) in mm
        self.n_bin = n_bin
        self.file_name = file_name
        self.translation = None     # [x, y, z] in mm
        self.rotations = ()                           # (("X", 70), ("Z", 10)), in deg

    def add_quantity(self, quantity, name):
        self._quantities[name] = quantity

    @property
    def before(self):
        commands = [
            "/score/create/boxMesh " + self.name,
            "/score/mesh/boxSize %f %f %f mm" % (self.box_size[0], self.box_size[1], self.box_size[2]),
            "/score/mesh/nBin %d %d %d" % (self.n_bin[0], self.n_bin[1], self.n_bin[2])
        ]
        commands.append("/score/mesh/translate/reset")
        if self.translation is not None:
            # print self.translation
            commands.append("/score/mesh/translate/xyz {} {} {} mm".format(self.translation[0], self.translation[1], self.translation[2]))
        commands.append("/score/mesh/rotate/reset")
        for rotation in self.rotations:
            if rotation[1]: # zero rotation not needed
                commands.append("/score/mesh/rotate/rotate%s %f deg" % (rotation[0].upper(), -rotation[1]))
        for name, quantity in self._quantities.items():
            commands.append("/score/quantity/%s %s" % (quantity, name))
        commands.append("/score/close")
        return MacroBuilder(commands)

    @property
    def after(self):
        commands = []
        for name, quantity in self._quantities.items():
            commands.append("/score/dumpQuantityToFile %s %s %s" % (self.name, name, self.file_name))
        return MacroBuilder(commands)