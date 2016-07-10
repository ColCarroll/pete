from pete.broadcaster import Broadcaster


class StringBroadcaster(Broadcaster):
    """Prints messages to standard out"""
    def send(self, messages):
        print(self._format(messages))

    def _format(self, messages):
        return '\n\n'.join(messages)
