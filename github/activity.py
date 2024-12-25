import requests, json, time

from functools import lru_cache


@lru_cache
def get_acitivities(username: str) -> requests.Response:
    return requests.get(f"https://api.github.com/user/{username}/events")


class Activity(object):
    
    def __init__(self,
                 username: str
                 ) -> None:
        self.username = username
        self.events = None
        self.needed_time = 0
        self._process_events()

    def _process_events(self): pass

    def is_valid_response(self): pass

    def get_activities(self,
                       activity_types: list=[]
                       ) -> list[dict[str, str]]:
        pass

    def get_types_of_events(self): pass

    def get_needed_time(self) -> int: pass
