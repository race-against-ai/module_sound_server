import os
import pygame
from pathlib import Path
import pynng


class SoundPlayer:
    def __init__(self, sound_folder):
        self.sound_folder = sound_folder
        self.sound_dict = self.get_sound_folder_content()
        pygame.init()
        pygame.mixer.init()

    def get_sound_folder_content(self):
        sound_dict = {}
        for file in os.listdir(self.sound_folder):
            sound_dict[file] = os.path.join(self.sound_folder, file)
        print(sound_dict)
        return sound_dict

    def play_sound(self, sound_file):
        sound = pygame.mixer.Sound(self.sound_dict.get(sound_file))
        if sound:
            sound.play()
            pygame.time.delay(int(sound.get_length() * 100))
        else:
            print("Sound not found: ", sound_file)


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
                msg = data.decode('utf-8')
                self.process_request(msg, sock)

    def process_request(self, msg, sock):
        if msg in self.sound_player.sound_dict:
            print("Playing sound: ", msg)
            self.sound_player.play_sound(msg)
            sock.send("Played sound".encode('utf-8'))
        else:
            print("Sound not found: ", msg)
            sock.send("Sound not found".encode('utf-8'))


def main():
    parent_path = Path(__file__).parent.parent.absolute()
    sound_folder = parent_path / 'sound_files'
    request_address = "ipc:///tmp/RAAI/sound_request.ipc"

    player = SoundPlayer(sound_folder)
    request_handler = RequestHandler(player, request_address)

    request_handler.run()


if __name__ == "__main__":
    main()
