import unittest
from find_combinations import Flight


class TestFlight(unittest.TestCase):
    def setUp(self):
        self.f1 = Flight('BRQ', 'PRG', '2016-10-11T10:10:00', '2016-10-11T11:10:00', 'OK234')
        self.f2 = Flight('PRG', 'VIE', '2016-10-11T12:10:00', '2016-10-11T13:40:00', 'LH239')
        self.f3 = Flight('BRQ', 'PRG', '2016-10-18T10:10:00', '2016-10-11T19:10:00', 'OK236')
        self.f4 = Flight('PRG', 'VIE', '2016-10-11T15:10:01', '2016-10-11T16:40:00', 'LH239')

    def test_connects(self):
        self.assertTrue(self.f1.connects(self.f2), 'Connecting flight')
        self.assertFalse(self.f1.connects(self.f3), 'Not connecting flight, bad city')
        self.assertFalse(self.f1.connects(self.f4), 'Not connecting flight, too late')

    def test_is_same(self):
        self.assertTrue(self.f1.is_same(self.f3))
        self.assertTrue(self.f2.is_same(self.f4))
        self.assertFalse(self.f1.is_same(self.f2))

if __name__ == '__main__':
    unittest.main()