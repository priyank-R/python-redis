import sys
from config.logging import setup_logger
from server.async_tcp import RunAsyncTcpServer
# from server.sync_tcp import run_tcp_sync_server
import logging

logger = logging.getLogger("app_logger")


def setup_flags():
    if len(sys.argv) < 3: 
        logger.error("Error - Please provide host and port")
        raise Exception('Please provide host and port')

    host = sys.argv[1]
    port = sys.argv[2]

    return host, port

def main():
    setup_logger()
    host, port = setup_flags()
    
    # run_tcp_sync_server(host, port)
    RunAsyncTcpServer(host, port)
    print('running !')


if __name__ == "__main__":
    main()