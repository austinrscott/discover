from RandomTextMap import RandomTextMap
from event import GameStartedEvent, TickEvent, MapGeneratedEvent


class GameModel:
    """
    A class that is subscribed to the event manager queue and which manages all game-related data. This class is the
    model for the program. It receives requests for changes in the model via "request" type events and when the view
    requires an update because of data changes, it posts an event for that.
    """

    STATE_LOADING = 'loading'
    STATE_RUNNING = 'running'

    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.register_listener(self)

        self.state = GameModel.STATE_LOADING

        self._map = RandomTextMap(70, 70, 0.01, 20, 0.35)
        self._map.print_map()
        event = MapGeneratedEvent(self._map.output_map())
        self.event_manager.post(event)
        # This is where all loading code would go

    def start(self):
        self.state = GameModel.STATE_RUNNING
        event = GameStartedEvent(self)
        self.event_manager.post(event)

    def notify(self, event):
        if isinstance(event, TickEvent):
            if self.state == GameModel.STATE_LOADING:
                self.start()
