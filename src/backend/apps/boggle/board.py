import random


class CombinationGenerator:
    """
        The letters in Boggle are not simply chosen at random. Instead, the
        letter cubes are designed in such a way that common letters come up
        more often and it is easier to get a good mix of vowels and consonants.
        Below are the cubes from the original Boggle.
    """
    DEFAULT_CUBES = [
        "AAEEGN", "ABBJOO", "ACHOPS", "AFFKPS",
        "AOOTTW", "CIMOTU", "DEILRX", "DELRVY",
        "DISTTY", "EEGHNW", "EEINSU", "EHRTVW",
        "EIOSST", "ELRTTY", "HIMNQU", "HLNNRZ",
    ]
    DEFAULT_SIZE = 4

    size = None
    cubes = None

    def __init__(self, cubes=None, size=None):
        self.cubes = cubes if cubes is not None else self.DEFAULT_CUBES
        self.size = size if size is not None else self.DEFAULT_SIZE

    def new(self):
        number_of_cubes = self.size * self.size

        letters = [
            random.choice(cube) for cube in random.sample(self.cubes, number_of_cubes)
        ]

        return letters
