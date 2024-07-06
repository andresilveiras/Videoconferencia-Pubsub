import zmq

def main():
    context = zmq.Context()
    
    # Criar sockets PUB para vídeo, áudio e texto
    video_socket = context.socket(zmq.PUB)
    audio_socket = context.socket(zmq.PUB)
    text_socket = context.socket(zmq.PUB)
    
    video_socket.bind("tcp://*:5555")
    audio_socket.bind("tcp://*:5556")
    text_socket.bind("tcp://*:5557")
    
    print("Broker está rodando...")
    
    try:
        while True:
            # O broker não faz nada além de rodar os sockets PUB
            pass
    except KeyboardInterrupt:
        print("Broker encerrado.")
    finally:
        video_socket.close()
        audio_socket.close()
        text_socket.close()
        context.term()

if __name__ == "__main__":
    main()
