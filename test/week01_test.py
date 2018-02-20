# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# DO NOT EDIT THIS FILE!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import unittest
from unittest import TestCase
from unittest.mock import patch

from test.utils import sleep, MockRPi, clock_pin, patcher

patcher.start()


class TestLED(TestCase):
    PIN = 23

    def setUp(self):
        from datacom.week01 import LED
        MockRPi.GPIO.reset_mock()
        self.uut = LED(self.PIN)

    def test_init(self):
        assert self.uut.pin == self.PIN, "Pin property not set correctly"
        MockRPi.GPIO.setup.assert_called_once_with(self.PIN, MockRPi.GPIO.OUT)

    def test_on(self):
        MockRPi.GPIO.reset_mock()
        self.uut.on()
        MockRPi.GPIO.output.assert_called_once_with(self.PIN, True)

    def test_off(self):
        MockRPi.GPIO.reset_mock()
        self.uut.off()
        MockRPi.GPIO.output.assert_called_once_with(self.PIN, False)

    def test_toggle(self):
        MockRPi.GPIO.reset_mock()
        MockRPi.GPIO.input.side_effect = None
        MockRPi.GPIO.input.return_value = MockRPi.GPIO.LOW
        self.uut.toggle()
        MockRPi.GPIO.input.assert_called_once_with(self.PIN)
        MockRPi.GPIO.output.assert_called_once_with(self.PIN, True)

        MockRPi.GPIO.reset_mock()

        MockRPi.GPIO.input.return_value = MockRPi.GPIO.HIGH
        self.uut.toggle()
        MockRPi.GPIO.input.assert_called_once_with(self.PIN)
        MockRPi.GPIO.output.assert_called_once_with(self.PIN, False)


class TestButton(TestCase):
    PIN = 23

    def setUp(self):
        from datacom.week01 import Button
        MockRPi.GPIO.reset_mock()
        self.uut = Button(self.PIN)

    def test_init(self):
        assert self.uut.pin == self.PIN, "Pin property not set correctly"
        MockRPi.GPIO.setup.assert_called_once_with(self.PIN, MockRPi.GPIO.IN, pull_up_down=MockRPi.GPIO.PUD_UP)

    def test_pressed(self):
        MockRPi.GPIO.reset_mock()
        MockRPi.GPIO.input.return_value = MockRPi.GPIO.LOW
        assert self.uut.pressed is True, "Button state invalid when pressed"
        MockRPi.GPIO.input.return_value = MockRPi.GPIO.HIGH
        assert self.uut.pressed is False, "Button state invalid when NOT pressed"

    @patch('time.sleep', sleep)
    def test_wait_for_press(self):
        MockRPi.GPIO.reset_mock()
        MockRPi.GPIO.input.side_effect = clock_pin
        self.uut.wait_for_press()


class TestMain(TestCase):
    def test_gpio_mode(self):
        from datacom.week01 import main
        MockRPi.GPIO.reset_mock()
        MockRPi.GPIO.input.side_effect = clock_pin
        main()
        MockRPi.GPIO.setmode.assert_called_once_with(MockRPi.GPIO.BCM)


def teardownModule():
    patcher.stop()


if __name__ == '__main__':
    unittest.main()
