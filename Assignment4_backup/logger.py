from datetime import datetime
import json

class Logger:
    def __init__(self, path="events.json"):
        self.path = path
        self.logs = []
        pass

    def log(self, event_type, data):
        self.logs.append([rf'[LOG] {event_type} -> {data}'])
        print(rf'[LOG] {event_type} -> {data}')
        pass

    def save(self, path=None):
        with open(self.path if path is None else path, 'w') as json_file:
            json.dump(self.logs, json_file, indent=4)
        pass