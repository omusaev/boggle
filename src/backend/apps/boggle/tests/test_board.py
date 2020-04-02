from unittest import TestCase
from unittest.mock import Mock, patch

from apps.boggle.board import (
    CombinationGenerator, WordSequenceValidator, WordLengthValidator,
    WordRulesLengthException, WordRulesSequenceException,
    WordScoreCalculator, Dictionary, WordDictionaryValidatorException,
    WordDictionaryValidator
)


class TestCombinationGenerator(TestCase):

    def test_if_fails_with_invalid_parameters(self):
        size = 4

        # 2 cubes instead of 16
        cubes = ['abcdef', 'abcdef']

        with self.assertRaises(AssertionError):
            CombinationGenerator(cubes=cubes, board_size=size)

    def test_if_generates_the_right_number_of_letters(self):
        size = 4

        letters = CombinationGenerator(board_size=size).new()

        assert len(letters) == size ** 2

    def test_if_really_random(self):
        generator = CombinationGenerator()

        # good enough if two consecutive calls give us different results
        assert generator.new() != generator.new()


class TestWordLengthValidator(TestCase):

    def setUp(self):
        self.validator = WordLengthValidator()

    def test_if_check_length_checks_min_length(self):
        word = 'a' * (self.validator.min_length - 1)

        with self.assertRaises(WordRulesLengthException):
            self.validator.validate(word)

    def test_if_check_length_checks_max_length(self):
        word = 'a' * (self.validator.max_length + 1)

        with self.assertRaises(WordRulesLengthException):
            self.validator.validate(word)


class TestWordSequenceValidator(TestCase):

    def setUp(self):
        combination = [
            "O", "O", "O", "P",
            "R", "A", "E", "W",
            "E", "D", "T", "Z",
            "W", "S", "O", "H"
        ]
        self.validator = WordSequenceValidator(combination=combination)

    def test_if_fails_with_invalid_parameters(self):
        size = 4
        combination = 'abcd'

        with self.assertRaises(AssertionError):
            WordSequenceValidator(combination=combination, board_size=size)

    def test_if_validate_calls_check_sequence(self):
        word = Mock()

        with patch.object(self.validator, '_check_sequence') as mocked:
            self.validator.validate(word)

        mocked.assert_called_with(word)

    def test_if_find_neighbors_returns_all_neighbors(self):
        """
            Here is the board with x, y instead of the values:

            (0, 0), (1, 0), (2, 0), (3, 0),
            (0, 1), (1, 1), (2, 1), (3, 1),
            (0, 2), (1, 2), (2, 2), (3, 2),
            (0, 3), (1, 3), (2, 3), (3, 3)

            for position (1, 1) we expect to get all the neighbors
            since they all are valid
        """

        pos = (1, 1)
        expected_neighbors = [
            (0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)
        ]

        actual_neighbors = self.validator._find_neighbors(pos)

        self.assertListEqual(expected_neighbors, actual_neighbors)

    def test_if_find_neighbors_drops_invalid_neighbors(self):
        """
            Here is the board with x, y instead of the values:

            (0, 0), (1, 0), (2, 0), (3, 0),
            (0, 1), (1, 1), (2, 1), (3, 1),
            (0, 2), (1, 2), (2, 2), (3, 2),
            (0, 3), (1, 3), (2, 3), (3, 3)

            for position (0, 0) we expect to get only 3 neighbors
            since it's in the corner
        """

        pos = (0, 0)
        expected_neighbors = [
            (0, 1), (1, 0), (1, 1)
        ]

        actual_neighbors = self.validator._find_neighbors(pos)

        self.assertListEqual(expected_neighbors, actual_neighbors)

    def test_if_find_path_returns_false_if_the_letter_is_wrong(self):
        pos = (0, 0)  # upper left corner, letter O
        rest = ['A']

        expected_result = False
        actual_result = self.validator._find_path(stack=[], pos=pos, rest=rest)

        self.assertEqual(expected_result, actual_result)

    def test_if_find_path_returns_true_if_found_a_path(self):
        pos = (0, 0)  # upper left corner, letter O
        rest = ['O']

        expected_result = True
        actual_result = self.validator._find_path(stack=[], pos=pos, rest=rest)

        self.assertEqual(expected_result, actual_result)

    def test_if_find_path_adds_pos_to_stack(self):
        pos = (0, 0)  # upper left corner, letter O
        rest = ['O']
        stack = []

        self.validator._find_path(stack=stack, pos=pos, rest=rest)

        self.assertListEqual(stack, [pos])

    def test_if_find_path_returns_false_if_pos_already_visited(self):
        pos = (0, 0)
        rest = ['O']
        stack = [pos]

        expected_result = False
        actual_result = self.validator._find_path(stack=stack, pos=pos, rest=rest)

        self.assertEqual(expected_result, actual_result)

    def test_if_find_path_finds_a_path(self):
        """
            Let's check 'west':

            "_", "_", "_", "_",
            "_", "_", "_", "_",
            "E", "_", "T", "_",
            "W", "S", "_", "_"
        """
        pos = (0, 3)  # left lower corner
        rest = ['W', 'E', 'S', 'T']
        stack = []

        expected_result = True
        actual_result = self.validator._find_path(stack=stack, pos=pos,
                                                  rest=rest)

        self.assertEqual(expected_result, actual_result)

    def test_if_find_path_build_the_right_path(self):
        """
            Let's check 'west':

            "_", "_", "_", "_",
            "_", "_", "_", "_",
            "E", "_", "T", "_",
            "W", "S", "_", "_"
        """
        pos = (0, 3)  # left lower corner
        rest = ['W', 'E', 'S', 'T']
        stack = []

        expected_stack = [(0, 3), (0, 2), (1, 3), (2, 2)]
        self.validator._find_path(stack=stack, pos=pos, rest=rest)

        self.assertListEqual(expected_stack, stack)

    def test_if_check_sequence_exist_as_soon_as_finds_a_path(self):
        """
            Let's check a fake word 'OA'.
            There are 3 starting points but the method is expected to exist
            as soon as it finds the word
            "O", "O", "O", "_",
            "_", "A", "_", "_",
            "_", "_", "_", "_",
            "_", "_", "_", "_"
        """

        word = 'OA'

        with patch.object(self.validator, '_find_path') as mocked:
            self.validator._check_sequence(word)

        mocked.assert_called_once()

    def test_if_check_sequence_return_flat_indexes_if_finds_a_path(self):
        """
            [(0, 3), (0, 2), (1, 3), (2, 2)]
            index = y * board_size + x
            [12, 8, 13, 10]
        """
        word = 'WEST'

        def _fake_find_path(stack, pos, rest):
            stack.extend([(0, 3), (0, 2), (1, 3), (2, 2)])
            return True

        expected_result = [12, 8, 13, 10]

        with patch.object(self.validator, '_find_path') as mocked:
            mocked.side_effect = _fake_find_path
            actual_result = self.validator._check_sequence(word)

        self.assertListEqual(expected_result, actual_result)

    def test_if_check_sequence_iterates_over_all_start_points(self):
        """
            Let's check a fake word 'OA'.
            There are 4 starting points. The method is expected to check
            all of them
            "O", "O", "O", "_",
            "_", "A", "_", "_",
            "_", "_", "_", "_",
            "_", "_", "O", "_"
        """

        word = 'OA'

        with patch.object(self.validator, '_find_path', return_value=False) as mocked:
            try:
                self.validator._check_sequence(word)
            except:
                pass

        self.assertEqual(mocked.call_count, 4)

    def test_if_check_sequence_raises_exception_if_not_found(self):
        word = 'OA'

        with patch.object(self.validator, '_find_path', return_value=False) as mocked:
            with self.assertRaises(WordRulesSequenceException):
                self.validator._check_sequence(word)


class TestWordScoreCalculator(TestCase):

    def test_if_calc_return_max_score_if_word_is_too_long(self):
        word = 'a' * 42
        calculator = WordScoreCalculator()

        expected_result = max(calculator.score_table.values())

        actual_result = calculator.calc(word)

        self.assertEqual(expected_result, actual_result)


class TestDictionary(TestCase):

    def setUp(self):
        self.dictionary = Dictionary('fake_path')

    def test_if_load_dictionary_called_only_once(self):
        with patch.object(self.dictionary, '_load_dictionary') as mocked:
            self.dictionary.words
            self.dictionary.words

        mocked.assert_called_once()

    def test_if_word_exists_returns_true_if_word_exists(self):
        fake_word = 'fake'

        expected_result = True

        with patch.object(self.dictionary, '_load_dictionary', return_value=[fake_word]) as mocked:
            actual_result = self.dictionary.word_exists(fake_word)

        self.assertEqual(expected_result, actual_result)

    def test_if_word_exists_returns_false_if_word_does_not_exist(self):
        fake_word = 'fake'

        expected_result = False

        with patch.object(self.dictionary, '_load_dictionary', return_value=[]) as mocked:
            actual_result = self.dictionary.word_exists(fake_word)

        self.assertEqual(expected_result, actual_result)


class TestWordDictionaryValidator(TestCase):

    def test_if_validate_raises_exception_if_word_does_not_exist(self):
        fake_dictionary = Mock()
        fake_dictionary.word_exists = Mock(return_value=False)

        validator = WordDictionaryValidator(dictionary=fake_dictionary)

        with self.assertRaises(WordDictionaryValidatorException):
            validator.validate('fake')
