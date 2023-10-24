import tkinter as tk
import pynng

SOUND_REQUEST_ADDRESS = "ipc:///tmp/RAAI/sound_request.ipc"


def send_sound_request():
    with pynng.Req0() as sock:
        sock.dial(SOUND_REQUEST_ADDRESS)
        sound_file = 'random_meme'
        sock.send(sound_file.encode('utf-8'))

        try:
            msg = sock.recv_msg()
            decoded_data: str = msg.bytes.decode()
            print(decoded_data)

        except pynng.Timeout:
            print("Sound request timed out")


def main():
    root = tk.Tk()
    root.title("Sound Request App")

    button = tk.Button(root, text="Sound", command=send_sound_request)
    button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
