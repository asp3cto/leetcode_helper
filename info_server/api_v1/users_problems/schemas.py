from enum import Enum

class ProblemStatus(str, Enum):
    """Class for description of problem's status for user
    """
    solved = "Solved"
    planned = "Planned"