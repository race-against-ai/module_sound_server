import unittest
import os
from unittest.mock import patch
from io import StringIO
from ..sound_server_backend.sound_server import SoundPlayer, RequestHandler, get_sound_folder_content


class TestSoundPlayer(unittest.TestCase):
    def setUp(self):
        # Set up paths and create a SoundPlayer instance for testing
        sound_folder = 'test_sound_files'
        meme_sound_folder = 'test_meme_sound_files'
        self.player = SoundPlayer(sound_folder, meme_sound_folder)

    def test_get_sound_folder_content(self):
        # Mock the os.listdir method to simulate folder content
        with patch('sound_server.os.listdir') as mock_listdir:
            mock_listdir.return_value = ['sound1.mp3', 'sound2.mp3', 'not_a_sound.txt']

            result = get_sound_folder_content('test_folder')

            expected_result = {'sound1.mp3': 'test_folder/sound1.mp3', 'sound2.mp3': 'test_folder/sound2.mp3'}
            self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()

