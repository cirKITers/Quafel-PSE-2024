"""
This module provides a function to disassemble a connection string into its components.
"""

import re

def disassemble_connection_string(connection_string):
    """
    Disassemble a connection string into its components
    """
    # Define the regex pattern for the connection string
    pattern = r'^(?P<type>\w+)://(?P<host>[^:]+):(?P<port>\d+)$'
    match = re.match(pattern, connection_string)

    if not match:
        raise ValueError("Invalid connection string format")

    # Extract type, host, and port
    type_ = match.group('type')
    host = match.group('host')
    port = int(match.group('port'))

    # Validate port
    if not (1 <= port <= 65535):
        raise ValueError("Port number must be between 1 and 65535")

    return type_, host, port
