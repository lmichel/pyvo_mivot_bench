import os

__all__ = ["get_raw_data_folder", "get_annotated_data_folder", "get_sanbox_folder"]

def get_raw_data_folder(file):
    return os.path.realpath(
        os.path.join(os.path.dirname(__file__), "..", "data", "raw", file)
        )
    
def get_annotated_data_folder(file):
    return os.path.realpath(
        os.path.join(os.path.dirname(__file__), "..", "data", "annotated", file)
        )
    
def get_sanbox_folder(file):
    return os.path.realpath(
        os.path.join(os.path.dirname(__file__), "..", "data", "annotated", file)
        )