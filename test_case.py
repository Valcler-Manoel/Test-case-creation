from instruments_academy import PSU, Equity, Eload
from time import sleep

class Test:

    def __init__(self):
        self._fm_state = 'START'
        self._fm_sleep_time = 0.1
        self._temperature_step = 0

    def _fm(self):
        if self._fm_state == 'START':

            print('Actual state -------- START --------')

            # Modules importation
            self.eload = Eload()
            self.equity = Equity()
            self.psu = PSU()

            # Functions
            self._config_eload()
            self._config_equity()
            self._config_psu()

            #Setting A's temperatures (A1,A2 A3)
            self._temperature = [-10, 25, 85]
            if any(temp not in range(-20, 101) for temp in self._temperature):
                raise ValueError('Temperature range error')

            #Setting stabilization time
            self._temperature_stabilization_time = 40
            if self._temperature_stabilization_time not in range(0, 61):
                raise ValueError('Temperature stabilization error')

            # Setting stabilization temperature
            self._stabilization_temperature_time = 2400
            if not 0 <= self._stabilization_temperature_time <= 3600:
                raise ValueError('Stabilization time error')

            self._current = 0.0
            assert type(self._current) is float
            if not 0.0 <= self._current <= 10.0:
                raise ValueError('Current range error')

            self._initial_current = 3.0
            if not 0 <= self._initial_current <= 5:
                raise ValueError('Initial electric current range error')
            self._current = 1.25
            self._initial_voltage = 12
            self._voltage = 120
            self._setpoint_power = 24
            self._final_current = 9.0
            if not 1 <= self._initial_current <= 10:
                raise ValueError('Final electric current range error')


            self._actual_temperature = self._temperature[self._temperature_step]

            self.eload.write(f'VOLT {self._initial_voltage}')

            self._fm_state = 'CONFIG_EQUITY'

        elif self._fm_state == 'CONFIG_EQUITY':
            """
               Configures the equity with the current temperature and waits for it to stabilize
               before proceeding to the next step 'CONFIG_EQUITY'.
               
               Returns:
                   None
               """

            print(f'Actual state -------- CONFIG_EQUITY --------')
            self._actual_current = self._initial_current

            self.equity.set_temperature(self._actual_temperature)

            while self._actual_temperature != self.equity.get_temperature():
                sleep(1)

            print(f'⚠️Actual temperature: {self.equity.get_temperature()}°C')

            self._fm_state = 'CONFIG_PSU'


        elif self._fm_state == 'CONFIG_PSU':
            """
                Configure the power supply unit (PSU) with the desired voltage and wait 1 second
                 before proceeding to the next step 'CONFIG_ELOAD'.
                 
                Returns:
                    None
            """
            print(f'Actual state -------- CONFIG_PSU --------')
            self.psu.set_voltage(self._voltage)
            sleep(1)
            self._fm_state = 'CONFIG_ELOAD'

        elif self._fm_state == 'CONFIG_ELOAD':
            """
               Configure the electronic load (ELOAD) with the desired current and wait 1 second
                before proceeding to the next step 'SHOW_OUTPUT'.

                Returns:
                    None
            """
            print(f'Actual state -------- CONFIG_ELOAD --------')
            self.eload.write(f'CURR {self._actual_current}')
            sleep(1)
            self._fm_state = 'SHOW_OUTPUT'

        elif self._fm_state == 'SHOW_OUTPUT':
            """
                This function prints the current readings of the electronic load, including CURRENT (A),
                VOLTAGE (V) and power (W),as well as the power supply readings, including current and voltage.
                It then waits 1 second before proceeding to the next step in the program flow, 
                on whether the output power has reached the set reference value.

                Returns:
                    None
            """
            print(f'Actual state -------- SHOW_OUTPUT --------')
            self._output_power = float(self.eload.query("MEAS:POW?"))

            print(f'Eload current: {self.eload.query("MEAS:CURR?")}A')
            print(f'Eload voltage: {self.eload.query("MEAS:VOLT?")}V')
            print(f'Eload power: {self._output_power}W')

            print(f'PSU current: {self.psu.get_current()}A')
            print(f'PSU voltage: {self.psu.get_voltage()}V')

            sleep(1)

            if self._output_power >= self._setpoint_power:
                self._fm_state = 'VERIFY_TEMPERATURE_STEP'
            else:
                self._actual_current += self._current
                self._fm_state = 'CONFIG_ELOAD'

        elif self._fm_state == 'VERIFY_TEMPERATURE_STEP':
            """
                This function is responsible for checking all temperature steps in the 'self._temperature' list.
                 If there are remaining steps,it updates the current temperature to the next step and sets the
                state of the program flow to 'CONFIG_EQUITY'. Otherwise, it sets the status to 'END'.

                Returns:
                    None
            """
            print(f'Actual state -------- VERIFY_TEMPERATURE_STEP --------')
            self._temperature_step += 1
            if self._temperature_step < len(self._temperature):
                self._actual_temperature = self._temperature[self._temperature_step]
                self._fm_state = 'CONFIG_EQUITY'
            else:
                self._fm_state = 'END'

        elif self._fm_state == 'END':
            """
                The following instructions are set in this function:
                    - Sets the PSU voltage to 0.0.
                    - Sets the current and voltage to 0.
                    - Sets the "_stop_flag" attribute to True, indicating the end of the test.

                Returns:
                    None
            """
            print(f'Actual state -------- END --------')
            self.psu.set_voltage(0.0)
            self.eload.write('CURR 0')
            self.eload.write('VOLT 0')

            self._stop_flag = True
            print('Test is done')

        else:
            raise Exception('Invalid FM state')

    """
        These methods represent a test automation system for controlling temperature, voltage and load.
         It generates reports and runs the main automation loop until the test is complete.

        Attributes:
            _stop_flag (bool): A flag indicating whether the test automation should stop.
            _fm_sleep_time (int): Sleep time between automation state transitions.

        Methods:
            _config_eload():
                Sets the current to 0 A.
            _config_equity():
                Sets the temperature to 25.0°C.
            _config_psu():
               Sets the PSU voltage to 0.0 V.
            _main():
               Controls the test process until the stop signal is set.

        """
    def _config_eload(self):
        self.eload.write('CURR 0')

    def _config_equity(self):
        self.equity.set_temperature(25.0)

    def _config_psu(self):
        self.psu.set_voltage(0.0)

    def _main(self):
        self._stop_flag = False
        while self._stop_flag is False:
            self._fm()
            sleep(self._fm_sleep_time)

if __name__ == '__main__':
    test = Test()
    test._main()
