import glob
import sys
import serial
from BLSTController import Observer
from typing import List

# https://tinyurl.com/w7pkw8z - Taken from SO


def serial_ports() -> List[str]:
    """ Lists serial port names
    :raises EnvironmentError:
            On unsupported or unknown platforms
    :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def __add_self_arg(func):
    """
    Takes any function with one argument and returns that function with self as
    the first argument. This is a helper method for build the build utility.

    :func:
        A function with one argument of type Action
    :raises:
        Exception when the func parameter is not correctly formed
    :returns:
        A function with two arguments self and Action
    """
    try:
        if func.__code__.co_argcount != 1:
            raise Exception("Argument func doesn't have one argument")
    except AttributeError:
        raise Exception("Argument func not a function")
    except Exception as e:
        raise e

    def selfFunc(self, arg):
        self._controller_state = arg
        return func(arg)
    return selfFunc


def builder(update_function):
    """
    Creates an observer from a function of one argument. The argument in the
    passed function is expected to be an Action argument.

    :update_function:
        A function with one Action argument to be added to an observer
    :raises Execption:
        Raises an exception if the update function is malformed
    :returns:
        An observer instance with the update method set to the update_function
        parameter
    """
    update_with_self = __add_self_arg(update_function)
    o = type("o", (), {
        "__init__": Observer.__init__,
        "update": update_with_self
    })
    return o()
