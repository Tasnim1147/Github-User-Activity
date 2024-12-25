import cmd, enum
from github.activity import Activity

class State(enum.Enum):

    EVENT = "event"
    USERNAME = "username"

    def __str__(self):
        return self.value


class Github_Activity(cmd.Cmd):

    def __init__(self):
        self.prompt = "github-activity "
        self.state = State.USERNAME
        self.activity = Activity()


    def run_cli(self) -> None: self.cmdloop()

    def precmd(self, 
               line: str
               ) -> str:
        line = self.state + line
        return super().precmd(line)

    def do_username(self, 
                    arg: str
                    ) -> None: pass

    def do_event(self, 
                 arg: str
                 ) -> None: pass