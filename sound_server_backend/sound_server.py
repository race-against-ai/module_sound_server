import os
import pygame
from pathlib import Path
import pynng
from random import choice
from time import sleep

REQUEST_ADDRESS = "ipc:///tmp/RAAI/sound_request.ipc"
STATUS_ADDRESS = "ipc:///tmp/RAAI/sound_server_status.ipc"


def get_sound_folder_content(folder):
    sound_dict = {}
    for file in os.listdir(folder):
        if file.endswith('.mp3'):
            sound_dict[file] = os.path.join(folder, file)
    print(sound_dict)
    return sound_dict


class SoundPlayer:
    def __init__(self, sound_folder, meme_sound_folder):
        self.sound_folder = sound_folder
        self.meme_sound_folder = meme_sound_folder
        self.sound_dict = get_sound_folder_content(self.sound_folder)
        self.meme_sound_dict = get_sound_folder_content(self.meme_sound_folder)
        pygame.init()
        pygame.mixer.init()

    def play_sound(self, sound_file):
        sound = pygame.mixer.Sound(self.sound_dict.get(sound_file))
        if sound:
            sound.play()
            pygame.time.delay(int(sound.get_length() * 1000))
        else:
            print("Sound not found: ", sound_file)

    def play_random_meme(self):
        random_sound = choice(list(self.meme_sound_dict.keys()))
        sound = pygame.mixer.Sound(self.meme_sound_dict.get(random_sound))
        if sound:
            sound.play()
            pygame.time.delay(int(sound.get_length() * 1000))
        else:
            print("Sound not found: ", random_sound)


class RequestHandler:
    def __init__(self, sound_player, request_address, status_socket):
        self.sound_player = sound_player
        self.request_address = request_address
        self.status_socket = status_socket

    def run(self):
        with pynng.Rep0() as sock:
            sock.listen(self.request_address)
            while True:
                print("Waiting for request...")
                data = sock.recv()
                msg = data.decode('utf-8')
                self.process_request(msg, sock)

    def process_request(self, msg, sock):
        if msg == "random_meme":
            sock.send("Playing random meme".encode('utf-8'))
            self.send_status("running")
            self.sound_player.play_random_meme()
            sock.send("Played random meme".encode('utf-8'))
            self.send_status("idle")
        else:
            if msg in self.sound_player.sound_dict:
                print("Playing sound: ", msg)
                self.sound_player.play_sound(msg)
                sock.send("Played sound".encode('utf-8'))
            else:
                print("Sound not found: ", msg)
                sock.send("Sound not found".encode('utf-8'))

    def send_status(self, status):
        self.status_socket.send(status.encode('utf-8'))


def main():
    parent_path = Path(__file__).parent.parent.absolute()
    sound_folder = parent_path / 'sound_files'
    meme_sound_folder = parent_path / 'meme_sound_files'

    status_socket = pynng.Pub0()
    status_socket.listen(STATUS_ADDRESS)
    sleep(2)

    player = SoundPlayer(sound_folder, meme_sound_folder)
    request_handler = RequestHandler(player, REQUEST_ADDRESS, status_socket)

    request_handler.run()
