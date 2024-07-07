import argparse
import threading
import time

import zmq

parser = argparse.ArgumentParser(description='Cliente para videoconferencia')
parser.add_argument('--id', type=int, help='ID do cliente')


def publish(context: zmq.Context, client_id: int):
    dealer = context.socket(zmq.DEALER)
    dealer.connect('tcp://localhost:5555')

    while True:
        dealer.send_multipart([client_id, b'audio message'])
        dealer.send_multipart([client_id, b'video message'])
        dealer.send_multipart([client_id, b'text message'])
        time.sleep(1)


def subscribe(context: zmq.Context):
    sub = context.socket(zmq.SUB)
    sub.connect('tcp://localhost:5556')

    # Inscrito em todos os canais
    sub.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
        message = sub.recv_string()
        print(message)


if __name__ == '__main__':
    args = parser.parse_args()
    client_id = f'client{args.id}'.encode()
    context = zmq.Context()

    # Threads
    pub_thread = threading.Thread(target=publish, args=(context, client_id))
    sub_thread = threading.Thread(target=subscribe, args=(context,))

    pub_thread.start()
    sub_thread.start()

    pub_thread.join()
    sub_thread.join()

    context.term()
