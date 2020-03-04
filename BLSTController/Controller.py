"""
Contains the definitions for the classes that handle the serial communication
"""

from serial import Serial
from typing import Dict, Any, Set, Callable
from BLSTController.Action import Action
import abc


# NOTE: Creating Observer class here to avoid circular import between
# Controller.py and Observer.py
class Observer(metaclass=abc.ABCMeta):
    """
    Defines an observer class which will be updated on every state change
    that happens in the controller
    """

    def __init__(self) -> None:
        """
        """
        self._controller: Controller = None
        self._controller_state: Any = None

    @abc.abstractmethod
    def update(self, arg: Action) -> Any:
        """
        Implementation must be provided by the child class

        :arg: Controller will call update with an argument
        """
        pass


class Controller():
    """
    The Controller class implements the observer pattern to provide the
    consumer with an interface with which to interact with a serial connection
    which only recieves data.
    """

    def __init__(self, serial_config: Dict[str, Any]) -> None:
        """
        Construct a new Controller with a serial connection

        :serial_config:
            Configuration for serial connection
        """
        self.conn: Serial = Serial(
            port=serial_config['port'],
            baudrate=serial_config['baudrate'],
            timeout=serial_config['timeout']
        )
        self.observers: Set[Observer] = set()

    def attach(self, observer: Observer) -> None:
        """
        Add an observer to the list of observers

        :observer:
            Observer to add
        """
        observer._controller = self
        self.observers.add(observer)

    def __builder(self, update_function: Callable[[Action], Any]) -> Observer:
        """
        Helper function which creates an observer from a function of one
        argument. The argument in the passed function is expected to be an
        Action argument.

        :update_function:
            A function with one Action argument to be added to an observer
        :raises Execption:
            Raises an exception if the update function is malformed
        :returns:
            An observer instance with the update method set to the 
            update_function parameter
        """
        # Check to see if the passed function has the correct number of
        # arguments. If not raise an error.
        try:
            if update_function.__code__.co_argcount != 1:
                raise Exception("Argument func doesn't have one argument")
        except AttributeError:
            raise Exception("Argument func not a function")
        except Exception as e:
            raise e

        # Create a new function with self as the first argument
        def selfFunc(self, arg):
            self._controller_state = arg
            return update_function(arg)

        # Create a new observer type with the new update function
        o = type("o", (), {
            "__init__": Observer.__init__,
            "update": selfFunc
        })
        return o()

    def attach_function(self, func: Callable[[Action], Any]) -> None:
        """
        Helper function which accepts a function as a parameter and creates an
        Observer from that function replacing the Observer's update method with
        the passed function. The newly created Observer is then attached to this
        controller automatically.

        :func:
            Function used in the operation of an observer
        :raises Execption:
            Raises an exception if the update function is malformed
        :returns:
            None
        """
        o = self.__builder(func)
        self.attach(o)

    def start(self) -> None:
        """
        Starts listening for serial data and updating observers
        """
        with self.conn as serial:
            line = serial.readline()
            # Inform the observers that connection is open
            self.__notify(
                Action('OPEN', None)
            )
            while True:
                if not self.conn.isOpen():
                    return
                line = serial.readline().decode('utf-8')
                try:
                    action = Action.parse(line)
                except:
                    continue
                if action.directive == 'CLOSE':
                    self.__notify(action)
                    break
                self.__notify(action)

    def __notify(self, data: Action) -> None:
        """
        Go through all the observers and notify them that something has 
        happened using the passed Action instance.

        :data:
            Object containing the update
        """
        for observer in self.observers:
            observer.update(data)
