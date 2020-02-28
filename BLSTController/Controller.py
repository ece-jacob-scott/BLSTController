"""
Contains the definitions for the classes that handle the serial communication
"""

from serial import Serial
from typing import Dict, Any, Set
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

    def start(self) -> None:
        """
        Starts listening for serial data and updating observers
        """
        with self.conn as serial:
            line = serial.readline()
            # Inform the observers that connection is open
            self._notify(
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
                    self._notify(action)
                    break
                self._notify(action)

    def _notify(self, data: Any) -> None:
        """
        Go through all the observers and notify them that something has 
        happened

        :data:
            Object containing the update
        """
        for observer in self.observers:
            observer.update(data)
