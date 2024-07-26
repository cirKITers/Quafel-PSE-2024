"""
In this module the output connection is defined
The output connection is set in the submitter to copy the output to 
and get the output from
"""

from quafel_simulators.base.hardware import QuafelHardwareBase
from quafel_simulators.util.json_handler import read_dict, write_json_file


class QuafelOutputHardware(QuafelHardwareBase):
    """
    The output hardware to get the output from
    """
    def __init__(self):
        self.configuration_file_path: str = "output.json"  # path to the configuration file

        self._output_location: str = ""  # location where all outputs are stored (not the id of the output)
        self._host: str = ""  # host of the output server
        self._port: int = 22  # port of the output server
        self._username: str = ""  # username to connect to the output server
        self._password: str = ""  # password to connect to the output server

    def get_id(self) -> str:
        return "output"

    def get_host(self) -> str:
        return self._host

    def get_port(self) -> int:
        return self._port

    def get_username(self) -> str:
        return self._username

    def get_password(self) -> str:
        return self._password

    def get_totp(self) -> str | None:
        return None  # No TOTP needed

    def get_setup_script(self) -> str:
        return ""

    def get_run_script(self) -> str:
        # Override this function to use a custom script to pull the output
        # Look at the default script to see how to define parameters
        return ""  # The default script is build in the script_builder

    def get_output_location(self) -> str:
        """
        Get the output location
        """
        return self._output_location

    def update(self) -> bool:
        """
        Update the output location from the configuration file
        :return: True if the update was successful, False if the configuration file is not valid
        """
        read = read_dict(self.configuration_file_path)

        if len(read) == 0:
            write_json_file(self.configuration_file_path, {
                "output_location": "",
                "host": "",
                "port": 22,
                "username": "",
                "password": "",
            })

        if (("output_location" not in read) or
                ("host" not in read) or
                ("port" not in read) or
                ("username" not in read) or
                ("password" not in read)):
            return False

        self._output_location = read["output_location"]
        self._host = read["host"]
        self._port = read["port"]
        self._username = read["username"]
        self._password = read["password"]

        return True
