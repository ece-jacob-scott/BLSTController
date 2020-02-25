import unittest
from BLSTController.Action import Action
from typing import List

class ActionTests(unittest.TestCase):
    def test_debug_w_msg(self):
        line = 'DEBUG|This is a message'
        a = Action.parse(line)
        self.assertEqual(a.directive, 'DEBUG', 'Directive was set')
        self.assertEqual(a.value, line.split('|')[1], 
            'Debug message is correct')

    def test_debug_wo_msg(self):
        line = 'DEBUG|'
        a = Action.parse(line)
        self.assertEqual(a.directive, 'DEBUG', 'Directive was set')
        self.assertEqual(a.value, '', 'Debug message is correct')
    
    def test_w_nodir(self):
        line = '|This is a message'
        with self.assertRaises(KeyError):
            a = Action.parse(line)

    def test_foot_w_vals(self):
        line = '123 43 -123 -34 -250 -12'
        should_be = {
            'left': {
                'pitch': 123,
                'yaw': 43,
                'roll': -123
            },
            'right': {
                'pitch': -34,
                'yaw': -250,
                'roll': -12
            }
        }
        a = Action.parse(line)
        self.assertDictEqual(a.value, should_be, 'Parsed correct values')

    def test_foot_w_morevals(self):
        line = '12 12 12 12 12 12 12'
        with self.assertRaises(RuntimeError):
            a = Action.parse(line)

    def test_foot_w_lessvals(self):
        line = '12 12 12 12 12'
        with self.assertRaises(RuntimeError):
            a = Action.parse(line)

    def test_foot_w_nonints(self):
        line = '12 12 12 12 not12 12'
        with self.assertRaises(RuntimeError):
            a = Action.parse(line)

    def test_close_wo_msg(self):
        line = 'CLOSE|'
        a = Action.parse(line)
        self.assertEqual(a.directive, 'CLOSE', 'Sets directive correctly')
        self.assertEqual(a.value, None, 'Discards message correctly')
    
    def test_close_w_msg(self):
        line = 'CLOSE|Hey there is a message in here'
        a = Action.parse(line)
        self.assertEqual(a.directive, 'CLOSE', 'Sets directive correctly')
        self.assertEqual(a.value, None, 'Discards message correctly')


if __name__ == '__main__':
    unittest.main()