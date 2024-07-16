"""
The quafel hardware base is for the runner to get the hardware information to connect to
"""

from abc import abstractmethod


class HardwareBase:
    """
    The base class for the hardware profile
    """

    @abstractmethod
    def get_host(self) -> str:
        """
        Get the host of the hardware
        """

    @abstractmethod
    def get_port(self) -> int:
        """
        Get the port of the hardware
        """

    @abstractmethod
    def get_username(self) -> str:
        """
        Get the username of the hardware
        """

    @abstractmethod
    def get_password(self) -> str:
        """
        Get the password of the hardware
        """

    @abstractmethod
    def needs_totp(self) -> bool:
        """
        Whether the hardware needs a TOTP
        """

    @abstractmethod
    def get_setup_script(self) -> str:
        """
        Get the setup script for the hardware
        """

    @abstractmethod
    def get_run_script(self) -> str:
        """
        Get the run script for the hardware
        """