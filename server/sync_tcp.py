import logging
import socket 
import traceback
from core.resp import readArrayString
from core.eval import evalAndRespond
from core.cmd import RedisCmd

logger = logging.getLogger()

def read_command(data: bytes):
    v,e = readArrayString(data)
    if v and not e:
        return RedisCmd(v[0], v[1:]), None
    if e:
        return None, e
    
    return None, Exception('Valid command not found')

    
def respond(cmd: RedisCmd, tcp_conn: socket):
    err = evalAndRespond(cmd, tcp_conn)
    if err: 
        respondError(err, tcp_conn)

def respondError(error: Exception | str, tcp_conn: socket.socket):
    e = str(error) if isinstance(error, str) else error
    tcp_conn.sendall(f"-{e}\r\n".encode('utf-8'))




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



