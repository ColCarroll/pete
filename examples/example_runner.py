from examples import StringBroadcaster, TimeChecker
from runner import Runner


def time_to_string_runner():
    """Get a runner that will print the time to string on the time every 10 seconds."""
    return Runner(
        tasks=(TimeChecker(),),
        broadcasters=(StringBroadcaster(),),
        timeout=10
    )


if __name__ == '__main__':
    time_to_string_runner().main()
