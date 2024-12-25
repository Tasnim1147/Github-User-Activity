from typing import Union
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
        self.activities = None
        self.response = None
        self._process_events()

    def _process_events(self): 
        start_time = time.time()
        self.response = get_acitivities(self.username)
        self.activities = json.loads(self.response)
        end_time = time.time()
        self.needed_time = end_time - start_time

    def is_valid_response(self): 
        return self.response.status_code

    def get_activities(self,
                       activity_types: list=[]
                       ) -> list[dict[str, Union[str, bool]]]:
        filtered_activities = filter(lambda activity: activity in activity_types,
                                     self.activities)
        activities = list(map(lambda activity: {
            'type': activity['type'],
            'id': activity['id'],
            'created_at': activity['created_at'],
            'public': activity['public'],
            'repo_name': activity['repo']['name']
        }))
        return activities

    def get_types_of_events(self): 
        return set(map(lambda activity: activity['type'], self.activities))

    def get_needed_time(self) -> int: return self.needed_time
