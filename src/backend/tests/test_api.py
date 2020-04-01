import json

from unittest import TestCase
from unittest.mock import patch, ANY

from core.models.base import get_base_for_migrations
from core.models.database import get_engine

from app import app


class TestApi(TestCase):

    def setUp(self):
        # run migrations in the in-memory db
        get_base_for_migrations().metadata.create_all(bind=get_engine())

        self.fake_combination = [
            "O", "O", "O", "P",
            "R", "A", "E", "W",
            "E", "E", "T", "Z",
            "W", "S", "O", "H"
        ]

        self.fake_player_name = 'fake_player_name'

        self.generator_patcher = patch(
            'apps.boggle.board.CombinationGenerator.new')
        self.mocked_generator = self.generator_patcher.start()
        self.mocked_generator.return_value = self.fake_combination

        self.app = app.test_client()

    def tearDown(self):
        # run migrations in the in-memory db
        get_base_for_migrations().metadata.drop_all(bind=get_engine())

        self.generator_patcher.stop()

    def _request(self, url, method, data):
        response = getattr(self.app, method)(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )

        data = json.loads(response.get_data().decode())

        return response, data

    def _create_game(self, combination_id=None):
        data = {
            'player_name': self.fake_player_name
        }

        if combination_id:
            data['combination_id'] = combination_id

        response, data = self._request(
            '/api/v1/games',
            'post',
            data
        )

        return response, data

    def test_if_create_game_response_format_is_correct(self):
        response, actual_data = self._create_game()

        expected_data = {
            'uuid': ANY,
            'combination_id': '1',
            'letters': self.fake_combination,
            'player_name': self.fake_player_name,
            'created_at': ANY,
            'found_words': [],
            'final_score': 0
        }

        self.assertDictEqual(expected_data, actual_data)
        self.assertEqual(response.status_code, 201)

    def test_if_create_game_with_combination_id_works(self):
        _, first_game = self._create_game()

        response, second_game = self._create_game(
            combination_id=first_game['combination_id']
        )

        expected_data = {
            'uuid': ANY,
            'combination_id': first_game['combination_id'],
            'letters': first_game['letters'],
            'player_name': self.fake_player_name,
            'created_at': ANY,
            'found_words': [],
            'final_score': 0
        }

        self.assertDictEqual(expected_data, second_game)
        self.assertEqual(response.status_code, 201)

    def test_if_api_accepts_valid_words(self):
        _, game = self._create_game()

        valid_word = 'west'
        expected_score = 1

        response, actual_data = self._request(
            '/api/v1/games/{}'.format(game['uuid']),
            'post',
            {'word': valid_word}
        )

        expected_data = {
            'uuid': game['uuid'],
            'combination_id': game['combination_id'],
            'letters': game['letters'],
            'player_name': self.fake_player_name,
            'created_at': game['created_at'],
            'found_words': [
                {
                    'word': valid_word.upper(),
                    'score': expected_score,
                    'path': [12, 8, 13, 10]
                }
            ],
            'final_score': expected_score
        }

        self.assertDictEqual(expected_data, actual_data)
        self.assertEqual(response.status_code, 201)

    def test_if_api_rejects_invalid_sequence(self):
        _, game = self._create_game()

        invalid_sequence = 'zero'

        response, actual_data = self._request(
            '/api/v1/games/{}'.format(game['uuid']),
            'post',
            {'word': invalid_sequence}
        )

        expected_data = {
            'error_message': 'The word is not present on the board',
            'error_code': 'INCORRECT_SEQUENCE'
        }

        self.assertDictEqual(expected_data, actual_data)
        self.assertEqual(response.status_code, 400)

    def test_if_api_rejects_fake_word(self):
        _, game = self._create_game()

        fake_word = 'aoe'

        response, actual_data = self._request(
            '/api/v1/games/{}'.format(game['uuid']),
            'post',
            {'word': fake_word}
        )

        expected_data = {
            'error_message': 'The word does no exist',
            'error_code': 'WORD_DOES_NOT_EXIST'
        }

        self.assertDictEqual(expected_data, actual_data)
        self.assertEqual(response.status_code, 400)

    def test_if_api_rejects_duplicates(self):
        _, game = self._create_game()

        valid_word = 'west'

        self._request(
            '/api/v1/games/{}'.format(game['uuid']),
            'post',
            {'word': valid_word}
        )

        response, actual_data = self._request(
            '/api/v1/games/{}'.format(game['uuid']),
            'post',
            {'word': valid_word}
        )

        expected_data = {
            'error_message': 'The word has been added already',
            'error_code': 'WORD_HAS_BEEN_ADDED_ALREADY'
        }

        self.assertDictEqual(expected_data, actual_data)
        self.assertEqual(response.status_code, 400)

    def test_if_api_rejects_words_after_ttl(self):
        _, game = self._create_game()

        valid_word = 'west'

        # expires right away
        with patch('apps.boggle.resources.settings.GAME_TTL', new=0):
            response, actual_data = self._request(
                '/api/v1/games/{}'.format(game['uuid']),
                'post',
                {'word': valid_word}
            )

        expected_data = {
            'error_message': 'The game is finished',
            'error_code': 'GAME_IS_FINISHED'
        }

        self.assertDictEqual(expected_data, actual_data)
        self.assertEqual(response.status_code, 400)
