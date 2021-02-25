import os


class ManagementDirectory:
    def __init__(self, bar: str):
        self._path = os.getcwd()
        self._parent_folder = "screenshots"
        self._bar = bar

    def create_the_folder_if_it_does_not_exist(self, name_folder: str) -> str:
        path = f"{self._path}{self._bar}{self._parent_folder}{self._bar}{name_folder}{self._bar}"
        if not os.path.exists(path):
            os.makedirs(path)

        return path
