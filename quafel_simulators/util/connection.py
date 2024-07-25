"""
SSH connections
- Connection to a simulation server
- Connection to an output server
"""

import logging
import socket
import subprocess
from pathlib import Path
from time import sleep

import paramiko
from paramiko import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import SSHException

from quafel_simulators.base.hardware import QuafelHardwareBase
from quafel_simulators.base.simulation_request import QuafelSimulationRequest
from quafel_simulators.output import QuafelOutputHardware
from quafel_simulators.util.script_builder import build_quafel_script_setup, build_quafel_script_submit, \
    build_quafel_script_pull_output


class Connection:
    """
    Connection to a hardware_base
    Uses SSH
    """
    def __init__(self, hardware_base: QuafelHardwareBase):
        """
        Initialize the connection
        """
        self._hardware_base: QuafelHardwareBase | None = hardware_base
        self._ssh_client: SSHClient | None = None

    def _top_handler(self, title, instructions, prompt_list):
        """
        Top handler for the connection
        """
        response = []

        for prompt in prompt_list:
            if str(prompt[0]).lower().find("name") != -1:
                response.append(self._hardware_base.get_username())
            if str(prompt[0]).lower().find("word") != -1:
                response.append(self._hardware_base.get_password())
            if str(prompt[0]).lower().find("otp") != -1:
                response.append(self._hardware_base.get_totp())

        return tuple(response)

    def connect(self) -> bool:
        """
        Connect to the hardware
        """
        if (self._hardware_base is None) or (self._ssh_client is not None):
            return False

        self._ssh_client = SSHClient()
        self._ssh_client.set_log_channel("connection.connect")

        host = self._hardware_base.get_host()
        port = self._hardware_base.get_port()
        username = self._hardware_base.get_username()
        password = self._hardware_base.get_password()
        totp = self._hardware_base.get_totp()

        if totp is not None:
            try:
                self._ssh_client.set_missing_host_key_policy(AutoAddPolicy())
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((host, port))

                transport = paramiko.Transport(sock)
                transport.start_client(timeout=10)
                transport.auth_interactive(username, self._top_handler)

            except SSHException as ssh_exception:
                print("Error connecting to the hardware: ", ssh_exception)
                return False
        else:
            try:
                self._ssh_client.set_missing_host_key_policy(AutoAddPolicy())
                self._ssh_client.connect(
                    hostname=host,
                    port=port,
                    username=username,
                    password=password,
                )

            except SSHException as ssh_exception:
                print("Error connecting to the hardware: ", ssh_exception)
                return False

        return True

    def run(self, command: str, log_channel: str = "connection.all") -> bool:
        """
        Run a command on the hardware
        """
        if self._ssh_client is None:
            return False

        self._ssh_client.set_log_channel(log_channel)
        channel = self._ssh_client.get_transport().open_session()

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

    def disconnect(self) -> bool:
        """
        Disconnect from the hardware
        """

        if self._ssh_client is None:
            return False

        self._ssh_client.set_log_channel("connection.disconnect")
        self._ssh_client.close()
        self._ssh_client = None

        return True

class SubmitConnection(Connection):
    """
    The hardware connection class to connect to the hardware
    Helper class for the submitter
    """

    _simulation_request: QuafelSimulationRequest | None = None
    _output_hardware: QuafelOutputHardware | None = None

    def __init__(self, request_base: QuafelSimulationRequest, output_hardware: QuafelOutputHardware):
        """
        Initialize the connection
        """
        super().__init__(request_base.get_hardware())
        self._simulation_request = request_base
        self._output_hardware = output_hardware

    def _set_setup_script(self) -> bool:
        """
        Set the setup flag
        :return: True if the set of the setup script was successful
        """
        if ((self._ssh_client is None) or
                (self._hardware_base is None) or
                (self._simulation_request is None)):
            return False

        self._ssh_client.exec_command("touch setup_script")

        # Write the setup script to the file
        setup_script = build_quafel_script_setup(self._simulation_request)
        self._ssh_client.exec_command(f"cat << EOT > setup_script\n{setup_script}\nEOT\n")

        return True

    def _setup_script_is_set(self) -> bool:
        """
        Get the setup flag
        """
        if self._ssh_client is None:
            return False

        self._ssh_client.set_log_channel("connection.setup_script")
        _, stdout, _ = self._ssh_client.exec_command("ls")
        return "setup_script" in stdout.read().decode("utf-8")

    def submit(self) -> bool:
        """
        Run the simulation request
        :return: True if the submission was successful
        """
        if ((self._simulation_request is None) or
                (self._hardware_base is None) or
                (self._simulation_request.get_simulator() is None) or
                (self._output_hardware is None)):
            return False

        if not self._output_hardware.update():
            raise RuntimeError("The output hardware is not configured")

        self._ssh_client.set_log_channel("connection.run")
        return self.run(build_quafel_script_submit(self._simulation_request, self._output_hardware), "connection.run")

    def initiate(self, force: bool = False) -> bool:
        """
        Initiate the hardware profile
        (setup if needed)
        """
        if ((self._simulation_request is None) or
                (self._ssh_client is None) or
                (self._hardware_base is None)):
            return False

        self._ssh_client.set_log_channel("connection.initiate")
        if (not self._setup_script_is_set()) or force:
            self._set_setup_script()
            return self.run(
                command="bash setup_script\n",
                log_channel="connection.setup_script",
            )

        return True


class OutputConnection:
    """
    The output connection class to connect to the output server
    Helper class for the submitter
    """

    _output_hardware: QuafelOutputHardware | None = None
    _submit_id: str | None = None

    def __init__(self, output_hardware: QuafelOutputHardware, submit_id: str):
        """
        Initialize the connection
        """
        super().__init__()
        self._output_hardware = output_hardware
        self._submit_id = submit_id

    def _move_remote_output(self) -> bool:
        """
        Get the output from the remote output_location
        Move it to the relative path "outputs/<submit_id>"
        """

        build_pull_script = build_quafel_script_pull_output(self._output_hardware, self._submit_id)
        completed_process = subprocess.run(["bash", "-c", build_pull_script], check=False)

        print(completed_process.stdout)

        if completed_process.returncode != 0:
            return False

        return True

    def _get_local_output(self) -> str | None:
        """
        Get the output from the local output_location
        Remove the output_location after getting the output
        The output should be in the relative path "outputs/<submit_id>"
        """

        # inside this path should be another directory with an unknown name
        output_path = "outputs/" + self._submit_id + "/"

        # get the name of the directory
        # there should be only one subdirectory
        completed_process = subprocess.run(["bash", "-c", f"ls {output_path}"], capture_output=True, check=False)
        subdir = completed_process.stdout.decode("utf-8").strip()

        if completed_process.returncode != 0 or subdir == "":
            return None

        # Check if the file exists
        output_file = f"{output_path}{subdir}/evaluations_combined.csv"
        if not Path(output_file).exists():
            return None

        output = None

        # Read the file
        with open(output_file, mode="r", encoding="utf-8") as file:
            output = file.read()
            file.flush()
            file.close()

        # Delete the output_location
        completed_process = subprocess.run(["bash", "-c", f"rm -rf {output_path}"], check=False)
        if completed_process.returncode != 0:
            return None

        return output

    def get_output(self) -> str | None:
        """
        Get the output from the specific output_location/output
        """
        if self._output_hardware is None:
            return None

        if self._submit_id is None or self._submit_id == "":
            return None

        if self._output_hardware.get_host() != "":
            if not self._move_remote_output():
                return None

        return self._get_local_output()
