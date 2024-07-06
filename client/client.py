from video import VideoClient
from audio import AudioClient
from text import TextClient
import threading

def main():
    video_client = VideoClient("tcp://localhost:5555")
    audio_client = AudioClient("tcp://localhost:5556")
    text_client = TextClient("tcp://localhost:5557")
    
    video_thread = threading.Thread(target=video_client.run)
    audio_thread = threading.Thread(target=audio_client.run)
    text_thread = threading.Thread(target=text_client.run)
    
    video_thread.start()
    audio_thread.start()
    text_thread.start()
    
    video_thread.join()
    audio_thread.join()
    text_thread.join()

if __name__ == "__main__":
    main()
