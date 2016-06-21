import unittest

from broadcaster import Broadcaster


class TestBroadcaster(unittest.TestCase):
    def test_must_define_send(self):

        #  Can define an empty class, but not instantiate
        class EmptyBroadcaster(Broadcaster):
            pass
        with self.assertRaises(TypeError):
            EmptyBroadcaster()

        # Once we define a send method, things go fine
        EmptyBroadcaster.send = lambda x: None
