"""
This module is responsible to handle runs and manage the input and output of the API.
"""
from quafelweb.api_node.i_node_run import INodeRun


# Maybe more methods?


def run(username:str, host:str, port:str, password:str, totp: str,
        min_qubits: int, max_qubits: int, qubits_increment: int, qubits_type: str, 
        min_depth: int, max_depth: int, depth_increment: int, depth_type: str, 
        min_shots: int, max_shots: int, shots_increment: int, shots_type: str,
        quantum_framework: list[str], evaluations: int):
    # was ist i node?
    """
    try to run the i_node
    """
    # Connect to the node with ip, port and totp
    # Check if the node is set up
    # Setup if not set up
    # Run the node with the config ???


def get_output(username:str, host:str, port:str, password:str, totp: str):
    """
    Get the output of the node-run.
    """


def update(username:str, host:str, port:str, password:str, totp: str):
    """
    Look if the output is finished and write it to the database. 
    This can be must be done by a separate thread.
    """
