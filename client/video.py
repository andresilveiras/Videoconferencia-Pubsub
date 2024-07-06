import cv2
import zmq
import base64
import numpy as np

class VideoClient:
    def __init__(self, address):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(address)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
    
    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Encode frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            encoded_frame = base64.b64encode(buffer).decode()
            
            self.socket.send_string(encoded_frame)
            received_frame = self.socket.recv_string()
            decoded_frame = base64.b64decode(received_frame)
            np_frame = np.frombuffer(decoded_frame, dtype=np.uint8)
            frame = cv2.imdecode(np_frame, cv2.IMREAD_COLOR)
            
            cv2.imshow('Video', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        self.socket.close()
        self.context.term()
