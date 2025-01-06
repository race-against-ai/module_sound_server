# Sound Player with Remote Request Handling

This Python project provides a simple system to play sounds and random meme sounds on request, using the `pygame` library for audio playback and `pynng` for inter-process communication (IPC).  

## Features
- Play specific sounds from a folder.
- Play random meme sounds from a separate folder.
- Handle sound playback requests via IPC (`pynng`).

## Requirements
- Python 3.8 or higher
- Libraries: `pygame`, `pynng`
- Audio files in `.mp3` format organized in two folders:  
  - `sound_files`: For regular sounds  
  - `meme_sound_files`: For meme sounds  

## Installation
1. Clone the repository.  
2. Install dependencies:  
   ```bash
   pip install pygame pynng
   ```
3. Place your `.mp3` files in the `sound_files` and `meme_sound_files` folders.  

## Usage
Run the script using:  
```bash
python main.py
```

### IPC Communication
- **Request Address:** `ipc:///tmp/RAAI/sound_request.ipc`
- **Supported Requests:**  
  - `random_meme`: Plays a random meme sound.  
  - `<sound_filename>`: Plays the specific sound (e.g., `sound1.mp3`).  

## Example Request via IPC
You can send requests using any `pynng` client. Example request to play a random meme:  
```python
import pynng

with pynng.Req0() as client:
    client.dial("ipc:///tmp/RAAI/sound_request.ipc")
    client.send(b"random_meme")
    print(client.recv().decode())
```
