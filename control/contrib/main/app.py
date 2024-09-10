
from control.core.app import Application, ApplicationManager

import sys

class MainApplication (Application):
    def prepare_application(self):
        manager = ApplicationManager()

        self.command_sets = []

        self.commands = {}

        for application in manager.applications:
            command_module = application.load_module("commands")
            if command_module is None: continue

            target = "commands"
            if not hasattr(command_module, target):
                print("Missing commands in module", application.path + ".commands")
                continue
            self.command_sets.append( (application.path, getattr(command_module, target) ) )

            for name, handler in getattr(command_module, target):
                if name in self.commands: assert False, "Conflict error"
                self.commands[name] = handler
        return 
    def init_application(self):
        return 
    def stop_application(self):
        return 
    
    def help(self, code = 0):
        print("Available subcommands :")
        print()

        for app, command_set in self.command_sets:
            print(f"[{app}]")
            for command, handler in command_set:
                print(f"\t{command}")
        sys.exit(code)
    def run (self, args):
        if len(args) == 0:
            self.help(0)
            return
        
        name, *args = args
        handler = self.commands.get(name, None)
        print(name, args, self.commands)
        if handler is None:
            print("Could not find subcommand")
            self.help(1)
            return 
        
        handler(args)