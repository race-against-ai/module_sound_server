import unittest
from unittest.mock import patch, MagicMock
from sound_server_backend.sound_server import SoundPlayer, RequestHandler, get_sound_folder_content


class TestSoundPlayer(unittest.TestCase):
    def setUp(self):
        self.sound_folder = './test_sound_files'
        self.meme_sound_folder = './test_meme_sound_files'

    def test_get_sound_folder_content(self):
        sound_dict = get_sound_folder_content(self.sound_folder)
        self.assertTrue(isinstance(sound_dict, dict))
        # Add more specific assertions based on your expectations

    @patch('pygame.mixer.Sound')
    @patch('pygame.time.delay')
    def test_play_sound(self, mock_delay, mock_sound):
        sound_player = SoundPlayer(self.sound_folder, self.meme_sound_folder)
        sound_player.play_sound('race-start.mp3')
        mock_sound.assert_called_once_with('./test_sound_files\\race-start.mp3')
        mock_sound.return_value.play.assert_called_once()
        mock_delay.assert_called_once()

    @patch('pygame.mixer.Sound')
    @patch('pygame.time.delay')
    @patch('random.choice')
    def test_play_random_meme(self, mock_choice, mock_delay, mock_sound):
        mock_choice.return_value = 'random_meme.mp3'
        sound_player = SoundPlayer(self.sound_folder, self.meme_sound_folder)
        sound_player.play_random_meme()
        mock_sound.assert_called_once_with('./test_meme_sound_files\\he_can_fock_of.mp3')
        mock_sound.return_value.play.assert_called_once()
        mock_delay.assert_called_once()


class TestRequestHandler(unittest.TestCase):
    @patch('pynng.Rep0')
    def test_process_request_random_meme(self, mock_sock):
        sound_player = MagicMock()
        handler = RequestHandler(sound_player, 'test_address')
        handler.process_request('random_meme', mock_sock)
        sound_player.play_random_meme.assert_called_once()
        mock_sock.send.assert_called_once_with('Played random meme'.encode('utf-8'))

    @patch('pynng.Rep0')
    def test_process_request_known_sound(self, mock_sock):
        sound_player = MagicMock()
        sound_player.sound_dict = {'race-start.mp3': './../sound_files/race-start.mp3'}
        handler = RequestHandler(sound_player, 'test_address')
        handler.process_request('race-start.mp3', mock_sock)
        sound_player.play_sound.assert_called_once_with('race-start.mp3')
        mock_sock.send.assert_called_once_with('Played sound'.encode('utf-8'))

    @patch('pynng.Rep0')
    def test_process_request_unknown_sound(self, mock_sock):
        sound_player = MagicMock()
        sound_player.sound_dict = {}
        handler = RequestHandler(sound_player, 'test_address')
        handler.process_request('unknown_sound.mp3', mock_sock)
        sound_player.play_sound.assert_not_called()
        mock_sock.send.assert_called_once_with('Sound not found'.encode('utf-8'))

if __name__ == '__main__':
    unittest.main()
