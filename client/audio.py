import pyaudio
import zmq

class AudioClient:
    def __init__(self, address):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(address)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
    
    def run(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        
        while True:
            data = stream.read(1024)
            self.socket.send(data)
            received_data = self.socket.recv()
            stream.write(received_data)
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        self.socket.close()
        self.context.term()
