import cmd, enum
from github.activity import Activity

class State(enum.Enum):

    EVENT = "event "
    USERNAME = "username "

    def __str__(self):
        return self.value

def display_activities(activities: list[dict[str, str]]) -> None:

    headers = list(activities[0].keys())
    rows = [list(activity.values()) for activity in activities]
    max_column_widths = [max([len(str(row[idx])) for row in rows] + [len(headers[idx])]) for idx in range(len(headers))]
    table_width = sum(max_column_widths) + 4 * len(headers)
    
    def display_border(edge='+') -> None: print(f"{edge}{'-'*table_width}{edge}")

    def display_row(row) -> None: 
        nonlocal max_column_widths
        for idx, cell in enumerate(row):
            print(f"| {' ' * (max_column_widths[idx] - len(str(cell)))} {cell}", end=" ")
        print(" |")
        

    display_border()
    def display_headers() -> None: 
        nonlocal headers
        display_row(headers)
        display_border()
        
    def display_rows(row: list[any]) -> None: 
        nonlocal rows
        n = len(rows)
        for idx, row in enumerate(rows):
            display_row(row)  
            if idx != n - 1: display_border(edge='-')

    display_headers()
    display_rows(rows)
    if rows: display_border()
    

class Github_Activity(cmd.Cmd):

    def __init__(self):
        self.prompt = "github-activity "
        self.state = State.USERNAME
        self.activity = []
        self.event_types = []
        super().__init__(completekey=None, 
                         stdin=None, 
                         stdout=None)

    def run_cli(self): self.cmdloop()

    def precmd(self, 
               line: str
               ) -> str:
        if (line != "help" and line != "exit"):
            line = str(self.state) + line
        return super().precmd(line)

    def do_username(self, 
                    arg: str
                    ) -> None: 
        if arg:
            self.activity = Activity(arg)
            if (self.activity.is_valid_response()):
                self.event_types = self.activity.get_types_of_events()
                if (len(self.event_types) == 0):
                    print("No activities found")
                    return
                print(f"Got event list in {self.activity.get_needed_time()} seconds\n")
                self.prompt_event_types()
                self.change_state()
            else:
                print(f"Provided username ({arg}) is invalid or the server is down")

    def do_event(self, 
                 arg: str
                 ) -> None: 
        if arg:
            try:
                choice = int(arg)
                if (1 <= choice <= len(self.event_types)):
                    display_activities(self.activity.get_activities([self.event_types[choice - 1]]))
                elif (choice == len(self.event_types) + 1):
                    display_activities(self.activity.get_activities(self.event_types))
                else:
                    raise IndexError
            except ValueError:
                print(f"Please provide a valid input: {arg}")
                self.prompt_event_types()
            except IndexError:
                print(f"Provided choice is out of range: {arg}")
        else:
            self.change_state()


    def prompt_event_types(self) -> None:
        print("Please select an option:")
        for i, choice in enumerate(self.event_types, start=1):
            print(f"{i}. {choice}")
        print(f"{len(self.event_types) + 1}. All")

    def do_help(self, arg):
        if self.state == State.USERNAME:
            print("<username>")
        elif self.state == State.EVENT:
            print("<choice>")
        else:
            raise NotImplementedError
        print("exit")

    def do_exit(self, 
                _) -> bool:
        return True
        
    def change_state(self) -> None:
        if self.state == State.USERNAME:
            self.state = State.EVENT
            self.prompt = "choice: "
        elif self.state == State.EVENT:
            self.state = State.USERNAME
            self.prompt = "github-activity "

if __name__ == "__main__":
    github_activity = Github_Activity()
    github_activity.run_cli()

