import threading

import zmq


def broker():
    context = zmq.Context()

    router = context.socket(zmq.ROUTER)
    router.bind('tcp://*:5555')

    # Criar sockets PUB para vídeo, áudio e texto
    pub = context.socket(zmq.PUB)
    pub.bind('tcp://*:5556')

    print('Broker está rodando...')

    try:
        while True:
            # O broker recebe mensagens dos clientes
            frame = router.recv_multipart()
            message = f'{frame[1].decode()}: {frame[2].decode()}'.encode()

            # O broker repassa as mensagens para todos os inscritos
            pub.send(message)
    except KeyboardInterrupt:
        print('Broker encerrado.')
    finally:
        pub.close()
        router.close()
        context.term()


if __name__ == '__main__':
    broker_thread = threading.Thread(target=broker)
    broker_thread.start()
    broker_thread.join()
