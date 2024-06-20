"""
This module is responsible to handle runs and manage the input and output of the API.
"""
from quafelweb.api_node.i_node_run import INodeRun


# Maybe more methods?


def run(config , node_run: INodeRun, totp: str):
    """
    try to run the i_node
    """
    # Connect to the node with ip, port and totp
    # Check if the node is set up
    # Setup if not set up
    # Run the node with the config ???


def get_output(node_run: INodeRun):
    """
    Get the output of the node-run.
    """


def update():
    """
    Look if the output is finished and write it to the database. 
    This can be must be done by a separate thread.
    """
