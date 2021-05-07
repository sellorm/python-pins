"""
Main board parent class for generic methods
"""

import os
import pickle
import tempfile


class Board:
    """
    main board class
    """

    def __init__(self, board_type):
        self.board_type = board_type
        self.temp_dir = None # contains the current temp dir if one exists

    def pin_meta(self):
        """
        Read metadata from pin
        """


    def info(self):
        """
        display the status of the board
        """
        print("Board info:")
        print("* Type: {}".format(self.board_type))
        # Print other info about the board
        # Maybe even a list of pins on it?

    def _to_json(self, data):
        pass

    def _to_arrow(self, data):
        pass

    def _to_csv(self, data):
        pass

    def _to_pickle(self, data):
        if not os.path.exists(self.temp_dir):
            raise Exception("Temporary directory does not exist.")
        data_file = os.path.join(self.temp_dir, "data.pkl")
        with open(data_file, 'wb') as data_file_conn:
            pickle.dump(data, data_file_conn)


    def _write_meta(self, **kwargs):
        pass

    def create_temp_pin(self, short_name, data_format, data):
        """
        Create a temproray local pin

        The temporary local pin should be used for preparing a pin for the target board.
        All pins start out as temporary local pins and are then packaged and transferred
        to the target storage backend. For example, in order to store a pin in a folder
        we would first create a temporary local pin and then copy it to the desired
        location.

        Note that optional meta data should also be passed in here in the future.

        :param: short_name A short friendly name for the pin
        :param: data_format Target storage format. One of csv, json, arrow or pickle
        :param: data the object to pickle
        :return: a string containing the path to the pin
        """
        
        self.temp_dir = tempfile.TemporaryDirectory()
        valid_formats = ["csv", "json", "arrow", "pickle"]
        if data_format not in valid_formats:
            raise Exception("Invalid data format")

        if data_format == "pickle":
            self._to_pickle(self, data)

        return self.temp_dir
 