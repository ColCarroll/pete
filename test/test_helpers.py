import os
from tempfile import mktemp
import unittest

from helpers import touch


class TestHelpers(unittest.TestCase):
    def test_touch(self):
        # docs advise not to use this, but I'm fine with test failing due to race condition
        file_to_touch = mktemp()
        self.assertFalse(os.path.exists(file_to_touch))
        touch(file_to_touch)
        self.assertTrue(os.path.exists(file_to_touch))
