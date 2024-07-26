"""
This file contains the definition of a hardware connection that is controlled by a script.
"""

from hardware_controller.models import HardwareProfile
from quafel_simulators.base.hardware import QuafelHardwareBase


class HardwareWithScript(QuafelHardwareBase):
    """
    This class is used to define a hardware connection that is controlled by a script.
    """

    def __init__(self, hardware_profile: HardwareProfile, username, password, totp):
        """ """

        self.hardware_profile = hardware_profile

        # The scripts are defined under:
        # ./scripts/<script_type>/run.bash
        # ./scripts/<script_type>/setup.bash

        # Check if files exist:
        path_run = f"./scripts/{hardware_profile.protocol}/run.bash"
        path_setup = f"./scripts/{hardware_profile.protocol}/setup.bash"

        with open(path_run, "r") as f:
            self.run_script = f.read()
        with open(path_setup, "r") as f:
            self.setup_script = f.read()

        self.username = username
        self.password = password
        self.otp = totp

    def get_id(self) -> str:
        return self.hardware_profile.uuid

    def get_host(self) -> str:
        return self.hardware_profile.ip_addr

    def get_port(self) -> int:
        return self.hardware_profile.port_addr

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
