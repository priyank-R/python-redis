import select
import socket
import logging
from server.processing import read_command, respond, respondError

logger = logging.getLogger()

BACKLOG = 128
RECV_BUFFER = 4096

def RunAsyncTcpServer(host = '0.0.0.0', port = 7379):
    """
    1. Create a raw socket to listen to IP Host and Port
    2. Register this listening socket FD with epoll and poll for events
    3. Once an event comes in, and if it is of the listening socket FD, treat it as a connection request
        3.1 Accept the connection on the FD
        3.2 Register the new client's FD as a part of the same epoll instance. 
    4. If the event is not matching the listening socket FD, it's a read data event coming from one of the clients.
        4.1 Read the incoming data, pass it to the read command, send a response. 
    """

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
        listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listening_socket.bind((host, int(port)))
        listening_socket.listen(BACKLOG)
        listening_socket.setblocking(False)
        

        epoll = select.epoll()
        epoll.register(listening_socket.fileno(), select.EPOLLIN)
        fd_to_socket: dict[int, socket.socket] = {}
        conn_clients = 0
        try:
            while True:
                events = epoll.poll(None, 10)
                for event in events:
                    fd, event_mask = event
                    if fd == listening_socket.fileno():
                        while True:
                            try: 
                                client,a = listening_socket.accept()
                                client.setblocking(False)
                                fd_to_socket[client.fileno()] = client
                                epoll.register(client.fileno(), select.EPOLLIN)
                                conn_clients+=1
                            except BlockingIOError as e:
                                logger.error('Encountered BlockingIOError')
                                break 

                        logger.info(f"Accepted connection from {a}, fd={fd}")
                        continue

                    if event_mask & select.EPOLLIN:
                        client = fd_to_socket[fd]
                        data = client.recv(RECV_BUFFER)
                        data, e = read_command(data)
                        if not data: 
                            respondError(e if e else "Some error occured", client)
                        else:
                            respond(data, client)

                    if event_mask & (select.EPOLLHUP | select.EPOLLERR):
                        # Socket disconnected - Perform cleanup.
                        epoll.unregister(fd)
                        fd_to_socket[fd].close()
                        del fd_to_socket[fd]
                        conn_clients-=1
                        continue
        finally:
            epoll.close()
            listening_socket.close()





            

    