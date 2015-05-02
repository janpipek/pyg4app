import collections


class Configuration(collections.OrderedDict):
    def render(self):
        commands = []
        for key, value in self.items():
            if isinstance(value, int):
                commands.append("/app/setInt %s %d" % (key, value))
            elif isinstance(value, bool):
                if value:
                    commands.append("/app/setInt %s 1" % key)
                else:
                    commands.append("/app/setInt %s 0" % key)
            elif isinstance(value, float):
                commands.append("/app/setDouble %s %f" % (key, value))
            else:
                commands.append("/app/setString %s %s" % (key, str(value)))
        return commands