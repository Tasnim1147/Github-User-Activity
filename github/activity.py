from typing import Union
import requests, json, time

from functools import lru_cache


@lru_cache
def get_acitivities(username: str) -> requests.Response:
    return requests.get(f"https://api.github.com/users/{username}/events")


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
        self.activities = json.loads(self.response.content)
        end_time = time.time()
        self.needed_time = end_time - start_time

    def is_valid_response(self) -> int: 
        return self.response.status_code == 200
    
    def get_response_status(self) -> int:
        return self.response.status_code

    def get_activities(self,
                       activity_types: list=[]
                       ) -> list[dict[str, Union[str, bool]]]:
        if self.response.status_code != 200: return list()
        filtered_activities = filter(lambda activity: activity in activity_types,
                                     self.activities)
        activities = list(map(lambda activity: {
            'type': activity['type'],
            'id': activity['id'],
            'created_at': activity['created_at'],
            'public': activity['public'],
            'repo_name': activity['repo']['name']
        }), filtered_activities)
        return activities

    def get_types_of_events(self): 
        if self.response.status_code != 200: return set()
        return set(map(lambda activity: activity['type'], self.activities))

    def get_needed_time(self) -> int: return self.needed_time
