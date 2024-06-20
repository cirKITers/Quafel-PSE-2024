"""
This module is responsible to handle runs and manage the input and output of the API.
"""
from source.api_node.i_node_run import INodeRun


# Maybe more methods?


def run(username:str, host:str, port:str, password:str, totp: str, slurm: str,
        min_qubits: int, max_qubits: int, qubits_increment: int, qubits_type: str, 
        min_depth: int, max_depth: int, depth_increment: int, depth_type: str, 
        min_shots: int, max_shots: int, shots_increment: int, shots_type: str,
        quantum_framework: list[str], evaluations: int):
    connection = connect(username, host, port, password, totp, slurm)
    """ 
    if correct QUAFEL version is not set up, set it up
    Run QUAFEL with given parameters through SLURM
    """

def connect(username:str, host:str, port:str, password:str, totp: str, slurm: str):
    """
    Connect to the node through ssh with username, host, port, password, totp and slurm.
    """


def get_output(username:str, host:str, port:str, password:str, totp: str, slurm: str):
    """
    Get the output of the node-run.
    """


def update(username:str, host:str, port:str, password:str, totp: str, slurm: str):
    """
    Look if the output is finished and write it to the database. 
    This can be must be done by a separate thread.
    """
