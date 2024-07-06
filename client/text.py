import zmq

class TextClient:
    def __init__(self, address):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(address)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
    
    def run(self):
        while True:
            message = input("Digite sua mensagem: ")
            self.socket.send_string(message)
            received_message = self.socket.recv_string()
            print("Mensagem recebida:", received_message)
        
        self.socket.close()
        self.context.term()
