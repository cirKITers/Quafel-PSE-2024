"""
Here is the submission class that is used to submit a simulation request to the hardware.
"""
import logging
from time import sleep

from paramiko import AutoAddPolicy
from paramiko.client import SSHClient

from quafel_simulators.base.simulation_request import QuafelSimulationRequest
from quafel_simulators.util.script_builder import build_quafel_script_submit, build_quafel_script_setup


class HardwareConnection:
    """
    The hardware connection class to connect to the hardware
    Helper class for the submitter
    """

    simulation_request: QuafelSimulationRequest | None = None
    ssh_client: SSHClient | None = None

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
        self.ssh_client.set_log_channel("connection.connect")

        if needs_totp:
            # TODO: totp = self.simulation_request.get_totp()
            print("TOTP is needed but not implemented yet")
            return False
        else:
            try:
                self.ssh_client.set_missing_host_key_policy(AutoAddPolicy())  # TODO: check
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

    def run(self, command: str, log_channel: str = "connection.all") -> bool:
        """
        Run a command on the hardware
        """
        if self.ssh_client is None:
            return False

        self.ssh_client.set_log_channel(log_channel)
        channel = self.ssh_client.get_transport().open_session()

        channel.exec_command(command)

        while channel.active:
            sleep(0.01)
            if channel.recv_ready():
                logging.getLogger(log_channel).debug(msg=channel.recv(100000000).decode("utf-8"))
            if channel.recv_stderr_ready():
                logging.getLogger(log_channel).debug(msg=channel.recv_stderr(100000000).decode("utf-8"))
            if channel.exit_status_ready():
                break

        return channel.exit_status == 0

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
        setup_script = build_quafel_script_setup(self.simulation_request)
        self.ssh_client.exec_command(f"cat << EOT > setup_script\n{setup_script}\nEOT\n")

        return True

    def _setup_script_is_set(self) -> bool:
        """
        Get the setup flag
        """
        if self.ssh_client is None:
            return False

        self.ssh_client.set_log_channel("connection.setup_script")
        _, stdout, _ = self.ssh_client.exec_command("ls")
        return "setup_script" in stdout.read().decode("utf-8")

    def initiate(self, force: bool = False) -> bool:
        """
        Initiate the hardware profile
        (setup if needed)
        """
        if ((self.simulation_request is None) or
                (self.ssh_client is None) or
                (self.simulation_request.get_hardware() is None)):
            return False

        self.ssh_client.set_log_channel("connection.initiate")
        if (not self._setup_script_is_set()) or force:
            self._set_setup_script()
            return self.run(
                command="bash setup_script\n",
                log_channel="connection.setup_script",
            )

        return True

    def submit(self) -> bool:
        """
        Run the simulation request
        """
        if ((self.simulation_request is None) or
                (self.simulation_request.get_hardware() is None) or
                (self.simulation_request.get_simulator() is None)):
            return False

        self.ssh_client.set_log_channel("connection.run")
        return self.run(build_quafel_script_submit(self.simulation_request), "connection.run")  # TODO: check

    def disconnect(self) -> bool:
        """
        Disconnect from the hardware
        """

        if self.ssh_client is None:
            return False

        self.ssh_client.set_log_channel("connection.disconnect")
        self.ssh_client.close()
        self.ssh_client = None

        return True


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

        if not hardware_connection.submit():
            return False

        if not hardware_connection.disconnect():
            return False

        # TODO handle output?

        return True


# The submitter singleton
submitter = Submitter()
