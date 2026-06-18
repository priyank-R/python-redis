import logging
import socket 
import traceback
from server.processing import read_command, respond

logger = logging.getLogger()


def run_tcp_sync_server(host, port):
    logger.info(f"Starting a sync TCP server on {host}, {port}")

    conn_clients = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: 
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, int(port)))

        server_socket.listen()
        logger.info("TCP server started")

        while True:
            client, addr = server_socket.accept()
            try:
                with client: 
                    conn_clients+=1

                    logger.info(f"connected to client: {addr} connection clients {conn_clients}")
                    while True: 
                        data, e = read_command(client.recv(1024))
                        if not data:
                            break
                        
                        respond(data, client)
            except Exception as e:
                logger.error(traceback.format_exc())
                logger.error(f"Client disconnect {addr}")
            finally:
                conn_clients-=1



