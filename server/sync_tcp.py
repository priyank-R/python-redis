import logging
import socket 

logger = logging.getLogger()

def read_command(data: bytes):
    if "COMMAND" in data.decode('utf-8'):
    # Respond with an empty RESP Array ('*0\r\n') telling the CLI there are 0 commands available.
    # This satisfies the CLI's parsing checks without crashing it.
        return "*0\r\n"
    
    return data.decode('utf-8')



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
                        data = read_command(client.recv(1024))
                        if not data:
                            break

                        logger.debug(f"received:  {data}")
                        client.sendall(data.encode('utf-8'))
            except Exception as e:
                logger.error(e)
                logger.error(f"Client disconnect {addr}")
            finally:
                conn_clients-=1



