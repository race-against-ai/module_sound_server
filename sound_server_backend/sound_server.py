import os
from pygame import *
from pathlib import Path
import pynng
from random import choice


def get_sound_folder_content(folder):
    sound_dict = {}
    for file in os.listdir(folder):
        if file.endswith(".mp3"):
            sound_dict[file] = os.path.join(folder, file)
    print(sound_dict)
    return sound_dict


class SoundPlayer:
    def __init__(self, sound_folder, meme_sound_folder, use_dummy_audio=False):
        self.sound_folder = sound_folder
        self.meme_sound_folder = meme_sound_folder
        self.sound_dict = get_sound_folder_content(self.sound_folder)
        self.meme_sound_dict = get_sound_folder_content(self.meme_sound_folder)

        if use_dummy_audio:
            os.environ['SDL_AUDIODRIVER'] = 'dummy'

        init()
        mixer.init()

        if use_dummy_audio:
            del os.environ['SDL_AUDIODRIVER']

    def play_sound(self, sound_file):
        sound = mixer.Sound(self.sound_dict.get(sound_file))
        if sound:
            sound.play()
            time.delay(int(sound.get_length() * 1000))
        else:
            print("Sound not found: ", sound_file)

    def play_random_meme(self):
        random_sound = choice(list(self.meme_sound_dict.keys()))
        sound = mixer.Sound(self.meme_sound_dict.get(random_sound))
        if sound:
            sound.play()
            time.delay(int(sound.get_length() * 1000))
        else:
            print("Sound not found: ", random_sound)


class RequestHandler:
    def __init__(self, sound_player, request_address):
        self.sound_player = sound_player
        self.request_address = request_address

    def run(self):
        with pynng.Rep0() as sock:
            sock.listen(self.request_address)
            while True:
                print("Waiting for request...")
                data = sock.recv()
                msg = data.decode("utf-8")
                self.process_request(msg, sock)

    def process_request(self, msg, sock):
        if msg == "random_meme":
            print("Playing random meme")
            self.sound_player.play_random_meme()
            print("Sending response")
            sock.send("Played random meme".encode("utf-8"))
        else:
            if msg in self.sound_player.sound_dict:
                print("Playing sound: ", msg)
                self.sound_player.play_sound(msg)
                sock.send("Played sound".encode("utf-8"))
            else:
                print("Sound not found: ", msg)
                sock.send("Sound not found".encode("utf-8"))


def main():
    parent_path = Path(__file__).parent.parent.absolute()
    sound_folder = parent_path / "sound_files"
    meme_sound_folder = parent_path / "meme_sound_files"
    request_address = "ipc:///tmp/RAAI/sound_request.ipc"

    player = SoundPlayer(sound_folder, meme_sound_folder)
    request_handler = RequestHandler(player, request_address)

    request_handler.run()
