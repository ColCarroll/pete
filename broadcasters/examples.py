from . import Broadcaster


class StringBroadcaster(Broadcaster):
    def send(self, messages):
        print(self._format(messages))

    def _format(self, messages):
        return '\n\n'.join(messages)
