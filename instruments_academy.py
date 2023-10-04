class Eload:

    def __init__(self):
        self.voltage = 0
        self.current = 0
        self.power = self.voltage * self.current
        self._buffer = None

    def write(self, command):
        assert type(command) is str

        if command.startswith('CURR'):
            if command.endswith('?'):
                self._buffer = self.current
            else:
                command_string = command.split(' ')
                self.current = float(command_string[1])

        elif command == 'MEAS:CURR?':
            self._buffer = self.current

        elif command.startswith('VOLT'):
            if command.endswith('?'):
                self._buffer = self.voltage
            else:
                command_string = command.split(' ')
                self.voltage = float(command_string[1])

        elif command == 'MEAS:VOLT?':
            self._buffer = self.voltage

        elif command == 'MEAS:POW?':
           self._buffer = self.current * self.voltage

        else:
            raise ValueError('Not recognized command')

    def read(self):
        buffer = str(self._buffer)
        self._buffer = None

        return buffer

    def query(self, command):
        assert type(command) is str

        if command == 'CURR?':
            return str(self.current)

        elif command == 'MEAS:CURR?':
            return str(self.current)

        elif command == 'VOLT?':
            return str(self.voltage)

        elif command == 'MEAS:VOLT?':
            return str(self.voltage)

        elif command == 'MEAS:POW?':
            return str(self.current * self.voltage)

        else:
            raise ValueError('Not recognized command')


class PSU:

    def __init__(self):
        self.voltage = 0
        self._current = 1

    def get_voltage(self):
        return self.voltage

    def set_voltage(self, voltage):
        assert (type(voltage) is float) or (type(voltage) is int)
        self.voltage = voltage

    def get_current(self):
        return self._current

    def get_power(self):
        return self.voltage * self._current


class Equity:

    def __init__(self):
        self._temperature = 25

    def get_temperature(self):
        return self._temperature

    def set_temperature(self, temperature):
        assert (type(temperature) is float) or (type(temperature) is int)
        self._temperature = temperature