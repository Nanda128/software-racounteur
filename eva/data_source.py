"""Reading EVA data from storage. Knows the file format and nothing else."""
import json


def load_raw_records(path):
    """Reads the EVA data file.

    Args:
        path (str): Path to the JSON file.

    Returns:
        list[dict]: Raw, unvalidated EVA entries exactly as stored.
    """
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)
    return None
