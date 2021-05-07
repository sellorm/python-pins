"""
Allows you to create pins in a specified folder
"""

from .board_parent import Board


class BoardFolder(Board):
    """
    class to encapsulate the folder based board
    """

    def __init__(self, folder):
        self.board_type = "Local folder"
        self.folder = folder
        Board.__init__(self, self.board_type)

    def pin_read(self):
        """
        Reads a pin from the board
        """


    def pin_write(self):
        """
        writes a pin to the board
        """


    def list_pins(self):
        """
        lists available pins on the board
        """
