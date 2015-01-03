from .macro import Macro, MacroBuilder
from .configuration import Configuration
from .gui import Gui
from .runner import execute


class Application(MacroBuilder):
    '''A single execution of the application.'''
    def __init__(self, **kwargs):
        super(Application, self).__init__()
        self._plugins = []
        self._runs = []
        self.random = kwargs.get("random", True)
        self.log_events = kwargs.get("log_events", 1000)
        self.interactive = kwargs.get("interactive", False)
        self.configuration = kwargs.get("configuration", Configuration())
        self._kwargs = kwargs
        self.events = 0

    def add_plugin(self, path):
        self._plugins.append(path)

    def add_run(self, run):
        self._runs.append(run)

    def on_rendering(self):
        pass

    def pre_initialize(self):
        '''Override this.'''
        return []

    def post_initialize(self):
        '''Override this.'''
        return []

    def render(self):
        # Prepare app for rendering
        self.on_rendering()

        commands = []
        for plugin in self._plugins:
            if not plugin.endswith(".so"):
                # TODO: Works only on linux
                plugin = "lib" + plugin + ".so"
            commands.append("/app/plugin/load " + plugin)

        if self.random:
            commands.append("/app/generateRandomSeed")        

        commands += self.pre_initialize()
        commands.append("/run/initialize")
        commands += self.post_initialize()

        if self.configuration:
            commands.append(self.configuration)

        if self.log_events:
            commands.append("/app/addAction NumberingEventAction")
            commands.append("/app/setInt app.logEvents %d" % self.log_events)
        commands.append("/app/addAction MemoryRunAction")

        if self.interactive:
            run = self._runs[0]
            commands.append(run.render_before())            
            commands.append("/app/prepareInteractive")
            commands.append(Gui())
            commands.append("/app/interactive")
        else:
            for run in self._runs:
                commands.append(run)

        # commands.append("/run/beamOn %d" % self.events)        
        return commands

    def execute(self, events=None, interactive=None, **kwargs):
        '''Execute the application.'''
        if events is not None:
            self.events = events
        if interactive is not None:
            self.interactive = interactive
        macro = Macro()
        macro.add(self)
        execute(macro, **kwargs)

    def write(self, path):
        '''Just write the macro commands to a file.

        :param path: path of the output macro file

        Running g4 application with the macro file has same result as self.run().'''
        macro = Macro()
        macro.add(self)
        macro.write(path)