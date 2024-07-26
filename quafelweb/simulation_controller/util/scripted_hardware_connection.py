"""
This file contains the definition of a hardware connection that is controlled by a script.
"""

from quafel_simulators.base.hardware import QuafelHardwareBase
from simulation_controller.util.connection_string_helper import disassemble_connection_string


class HardwareWithScript(QuafelHardwareBase):
    """
    This class is used to define a hardware connection that is controlled by a script.
    """

    def __init__(self, connection_string, username, password, totp, id):
        script_type, host, port = disassemble_connection_string(connection_string)

        # The scripts are defined under: 
        # ./scripts/<script_type>/run.bash
        # ./scripts/<script_type>/setup.bash

        # Check if files exist:
        path_run = f"./scripts/{script_type}/run.bash"
        path_setup = f"./scripts/{script_type}/setup.bash"

        with open(path_run, "r") as f:
            self.run_script = f.read()
        with open(path_setup, "r") as f:
            self.setup_script = f.read()

        self.id = id
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.otp = totp

    def get_id(self) -> str:
        return self.id

    def get_host(self) -> str:
        return self.host

    def get_port(self) -> int:
        return self.port

    def get_username(self) -> str:
        return self.username

    def get_password(self) -> str:
        return self.password

    def get_totp(self) -> str | None:
        return self.otp

    def get_setup_script(self) -> str:
        return self.setup_script

    def get_run_script(self) -> str:
        return self.run_script
