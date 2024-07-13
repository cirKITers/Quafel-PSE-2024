"""
Here is the submission class that is used to submit a simulation request to the hardware.
"""


from paramiko.client import SSHClient
from quafel_simulators.base.simulation_request import QuafelSimulationRequest


class HardwareConnection:
    """
    The hardware connection class to connect to the hardware
    Helper class for the submitter
    """

    simulation_request: QuafelSimulationRequest = None
    ssh_client: SSHClient = None

    def __init__(self, simulation_request: QuafelSimulationRequest):
        """
        Initialize the hardware connection
        """
        self.simulation_request = simulation_request

    def connect(self) -> bool:
        """
        Connect to the hardware
        """
        if ((self.simulation_request is None) or
                (self.ssh_client is not None) or
                (self.simulation_request.get_hardware() is None)):
            return False

        host = self.simulation_request.get_hardware().get_host()
        port = self.simulation_request.get_hardware().get_port()
        username = self.simulation_request.get_hardware().get_username()
        password = self.simulation_request.get_hardware().get_password()
        needs_totp = self.simulation_request.get_hardware().needs_totp()
        self.ssh_client = SSHClient()

        if needs_totp:
            # TODO: totp = self.simulation_request.get_totp()
            print("TOTP is needed but not implemented yet")
            return False
        else:
            try:
                self.ssh_client.connect(
                    hostname=host,
                    port=port,
                    username=username,
                    password=password,
                )
            except Exception as e:  # TODO: specify the exception
                print("Error connecting to the hardware: ", e)
                return False

        return True

    def _set_setup_script(self) -> bool:
        """
        Set the setup flag
        """
        if ((self.ssh_client is None) or
                (self.simulation_request is None) or
                (self.simulation_request.get_hardware() is None)):
            return False

        self.ssh_client.exec_command("touch setup_script")

        # Write the setup script to the file
        setup_script = self.simulation_request.get_hardware().get_setup_script()
        self.ssh_client.exec_command(f"echo 'setup_flag' > {setup_script}") # TODO check

        return True

    def _setup_script_is_set(self) -> bool:
        """
        Get the setup flag
        """
        if self.ssh_client is None:
            return False

        _, stdout, _ = self.ssh_client.exec_command("ls setup_script")
        return "setup_flag" in stdout.read().decode("utf-8")

    def initiate(self) -> bool:
        """
        Initiate the hardware profile
        (setup if needed)
        """
        if ((self.simulation_request is None) or
                (self.ssh_client is None) or
                (self.simulation_request.get_hardware() is None)):
            return False

        if not self._setup_script_is_set():
            self._set_setup_script()
            _, stdout, stderr = self.ssh_client.exec_command("bash setup_script")
            if stderr.read().decode("utf-8") != "":
                return False
            if "Error" in stdout.read().decode("utf-8"):
                return False

        return True

    def run(self) -> bool:
        """
        Run the simulation request
        """
        if ((self.simulation_request is None) or
                (self.simulation_request.get_hardware() is None) or
                (self.simulation_request.get_simulator() is None)):
            return False

        # TODO: Create run script

        # TODO: Run the simulation request

        return False  # TODO: return the result of the simulation

    def disconnect(self) -> bool:
        """
        Disconnect from the hardware
        """

        if self.ssh_client is None:
            return False

        self.ssh_client.close()
        self.ssh_client = None

        return False


class Submitter:
    """
    The submitter class to submit a simulation request
    """

    def submit(self, simulation_request) -> bool:
        """
        Submit a simulation request
        """
        hardware_connection = HardwareConnection(simulation_request)

        if not hardware_connection.connect():
            return False

        if not hardware_connection.initiate():
            return False

        if not hardware_connection.run():
            return False

        if not hardware_connection.disconnect():
            return False

        # TODO handle output?

        return True


# The submitter singleton
submitter = Submitter()
