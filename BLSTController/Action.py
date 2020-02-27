from typing import Any, List


class Action():
    """
    Action is going to be the type that is passed to all the observable classes
    during the notify phase of execution. Every action has a directive which
    defines what that action is doing. The values of each directive is defined
    below.

    FOOT - Standard foot entry that comes back from the arduino and will init
    the self.value property to a dictionary of pedal values.

    DEBUG - Used by the arduino to send messages to the host machine and will
    init the self.value property to a string with the information sent by the
    arduino.

    OPEN - Used to tell the observers that the serial connection to the Arduino
    is open and listening for packets.

    CLOSE - Used by the arduino to close the connection to the host machine.
    With this directive the self.value property will be None.
    """
    directives = ['FOOT', 'DEBUG', 'CLOSE', 'OPEN']

    def __init__(self, directive: str, value: Any) -> None:
        self.value: Any = value
        if directive not in self.directives:
            raise KeyError(f'{directive} is not a valid directive')
        self.directive: str = directive

    @staticmethod
    def parse(line: str):
        """
        This function will parse out a line from the arduino and return an
        appropriate Action instance to encapsulte the object. The definitions
        for what a line from the arduino could look like are as follows:

        FOOT
        ------
        123 -124 142 67 45 -98\n
        The first three numbers are the left pedals pitch, yaw, and roll (in
        that order). The latter three numbers are the pitch, yaw, and roll (in
        that order) for the right pedal.

        DEBUG
        ------
        DEBUG|Message to send as debug message\n
        A debug message must have the word DEBUG at the start and seperate the
        message with a pipe (|). Everything after the pipe (|) and before the
        newline (\n) will be sent as a debug string.

        CLOSE
        ------
        CLOSE|\n
        A close message is just sent as the word CLOSE at the start of the
        packet and punctuated with a pipe (|) and newline (\n).

        :line: 
            A string containing information from the Arduino
        :raises RuntimeError: 
            Raises a runtime error every time there is an unknown packet
        """
        # Arduino sends 'keep alive' packets to keep the serial connection open
        # the keep alive packet is just an empty byte
        if line == '':
            return Action('DEBUG', 'Arduino sent keep alive packet')
        # Handles special packets
        if '|' in line:
            split_line: List[str] = line.split('|')
            directive: str = split_line[0]
            value = None
            if directive == 'DEBUG':
                value = split_line[1]
            return Action(directive, value)
        # Handles foot action
        try:
            [l_pitch, l_yaw, l_roll,
                r_pitch, r_yaw, r_roll] = list(map(int, line.split(' ')))
        except ValueError as ex:
            raise RuntimeError(f'FOOT packet unrecognized: {line}') from ex
        return Action('FOOT', {
            'left': {
                'pitch': l_pitch,
                'yaw': l_yaw,
                'roll': l_roll
            },
            'right': {
                'pitch': r_pitch,
                'yaw': r_yaw,
                'roll': r_roll
            }
        })
