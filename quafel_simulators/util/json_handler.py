"""
Util to read json files
"""

import json
from pathlib import Path


def _assure_json(file_path: str) -> bool:
    """
    Check if a file exists
    :return: True if the file was created, False otherwise
    """
    path = Path(file_path)

    if (not path.exists()) or (not path.is_file()):
        path.touch()
        return True

    return False


def write_json_file(file_path: str, data):
    """
    Write a json file
    """
    with open(file_path, mode="w", encoding="utf-8") as file:
        json.dump(data, file)


def read_json_file(file_path: str):
    """
    Read a json file
    """
    with open(file_path, mode="r", encoding="utf-8") as file:
        return json.load(file)


def read_dict(file_path: str) -> dict:
    """
    Read a dictionary from the file_path
    If there is no dict, create it.
    """
    if _assure_json(file_path):
        write_json_file(file_path, {})
        return {}

    read = read_json_file(file_path)

    if isinstance(read, dict):
        return read

    write_json_file(file_path, {})
    return {}


def read_list(file_path: str) -> list:
    """
    Read a list from the file_path
    If there is no list, create it
    """
    if _assure_json(file_path):
        write_json_file(file_path, [])
        return []

    read = read_json_file(file_path)

    if isinstance(read, list):
        return read

    write_json_file(file_path, [])
    return []
