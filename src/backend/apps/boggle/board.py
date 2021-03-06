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
    DEFAULT_BOARD_SIZE = 4

    board_size = None
    cubes = None

    def __init__(self, cubes=None, board_size=None):
        self.cubes = cubes if cubes is not None else self.DEFAULT_CUBES
        self.board_size = board_size if board_size is not None else self.DEFAULT_BOARD_SIZE

        assert len(self.cubes) >= self.board_size ** 2

    def new(self):
        number_of_cubes = self.board_size ** 2

        letters = [
            random.choice(cube) for cube in random.sample(self.cubes, number_of_cubes)
        ]

        return letters


class WordRulesException(Exception):
    pass


class WordRulesLengthException(WordRulesException):
    pass


class WordRulesSequenceException(WordRulesException):
    pass


class WordLengthValidator:

    DEFAULT_MIN_LENGTH = 3
    DEFAULT_MAX_LENGTH = 16

    min_length = None
    max_length = None

    def __init__(self, min_length=None, max_length=None):
        self.min_length = min_length if min_length is not None else self.DEFAULT_MIN_LENGTH
        self.max_length = max_length if max_length is not None else self.DEFAULT_MAX_LENGTH

    def validate(self, word):
        word_length = len(word)

        if word_length < self.min_length or word_length > self.max_length:
            raise WordRulesLengthException(
                'Length must be between {} and {}'.format(self.min_length,
                                                          self.max_length)
            )


class WordSequenceValidator:

    DEFAULT_BOARD_SIZE = 4

    combination = None
    board_size = None

    def __init__(self, combination, board_size=None):
        self.combination = combination
        self.board_size = board_size if board_size is not None else self.DEFAULT_BOARD_SIZE

        assert len(self.combination) == self.board_size ** 2

    def validate(self, word):
        """
            Validates that the passed word is a valid sequence according to
            the game rules:

            can be constructed from the letters of sequentially adjacent cubes,
            where "adjacent" cubes are those horizontally, vertically, and
            diagonally neighboring. Words must be at least three letters long,
            may include singular and plural (or other derived forms)
            separately, but may not use the same letter cube more than once per
            word

            If the word is valid return first found valid path on the board
        """

        path = self._check_sequence(word)

        return path

    def _find_neighbors(self, pos):
        x, y = pos

        directions = [
            (-1, -1), (-1, 0), (-1, 1), (0, -1),
            (0, 1), (1, -1), (1, 0), (1, 1)
        ]

        neighbors = []
        for xd, yd in directions:
            neighbor_x = x + xd
            neighbor_y = y + yd

            if all([neighbor_x >= 0,
                    neighbor_x < self.board_size,
                    neighbor_y >= 0,
                    neighbor_y < self.board_size]):
                neighbors.append((neighbor_x, neighbor_y))

        return neighbors

    def _find_path(self, stack, pos, rest):
        x, y = pos
        letter = self.combination[y * self.board_size + x]

        # bad luck, let's go find another neighbor
        if letter != rest[0]:
            return False

        # this cube is already used
        if pos in stack:
            return False

        # ok, we're on the right path
        stack.append(pos)

        # this is the last letter - found!
        if len(rest) == 1:
            return True

        for neighbor in self._find_neighbors(pos):

            # already visited
            if neighbor in stack:
                continue

            found = self._find_path(stack, neighbor, rest[1:])

            if found:
                return True

        stack.pop()

        return False

    def _check_sequence(self, word):
        """
            Checks whether the word is on the board and returns first found
            valid path (indexes)
        """

        # first step is to find where the word begins. Since there might be
        # multiple options let's iterate over all possible start points
        # and check the sequence

        first_letter = word[0]
        start_points = [
            i for i, l in enumerate(self.combination) if l == first_letter
        ]

        for index in start_points:
            y = index // self.board_size
            x = index % self.board_size
            pos = (x, y)

            stack = []
            found = self._find_path(stack, pos, word)

            if found:
                # now let's go back to indexes
                return [y * self.board_size + x for (x, y) in stack]

        raise WordRulesSequenceException(
            'The word is not present on the board'
        )


class WordScoreCalculator:

    DEFAULT_SCORE_TABLE = {
        0: 0,
        1: 0,
        2: 0,
        3: 1,
        4: 1,
        5: 2,
        6: 3,
        7: 5,
        8: 11
    }

    score_table = None

    def __init__(self, score_table=None):
        self.score_table = score_table if score_table is not None else self.DEFAULT_SCORE_TABLE

    def calc(self, word):
        # if there is no key in the table just assume the word is longer than
        # the max defined in the table
        return self.score_table.get(len(word), max(self.score_table.values()))


class Dictionary:

    dictionary_path = None
    _words = None

    def __init__(self, dictionary_path):
        self.dictionary_path = dictionary_path

    def _load_dictionary(self):
        with open(self.dictionary_path, 'r') as file:
            return set(file.read().split())

    @property
    def words(self):
        if self._words is None:
            self._words = self._load_dictionary()

        return self._words

    def word_exists(self, word):
        return word in self.words


class WordDictionaryValidatorException(Exception):
    pass


class WordDictionaryValidator:

    dictionary = None

    def __init__(self, dictionary):
        self.dictionary = dictionary

    def validate(self, word):
        if not self.dictionary.word_exists(word):
            raise WordDictionaryValidatorException(
                'The word does no exist'
            )
