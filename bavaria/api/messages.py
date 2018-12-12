from dataclasses import dataclass, field
from datetime import datetime
from typing import List

def to_dataclass(data):
    for name, cls in _source_to_class.items():
        if data['content'] == None:
            return None

        if name in data['source']:
            if name in ['websocket', 'newsticker']:
                return cls(**data['content'])

            return cls(**data['content']['properties'])

    return None


@dataclass
class NewsItem:
    updated: datetime
    images: field(repr=False)
    title: str
    tracks: field(default_factory=list)
    content: str

    def __post_init__(self):
        self.updated = datetime.fromisoformat(self.updated)


@dataclass
class NewsTicker:
    incident_program: bool
    messages: List[NewsItem] = field(default_factory=list)

    def __post_init__(self):
        messages = []
        for message in self.messages:
            messages.append(NewsItem(**message))

        self.messages = messages


@dataclass
class Station:
    name: str
    uic: int


@dataclass
class Websocket:
    status: str


_source_to_class = {
    "station ": Station,
    "websocket": Websocket,
    "newsticker": NewsTicker
}
