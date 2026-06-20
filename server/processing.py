import logging
import socket 
from core.resp import readArrayString
from core.eval import evalAndRespond, evalPING
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
    try:
        tcp_conn.sendall(f"-{e}\r\n".encode('utf-8'))
    except Exception as e:
        logger.error(f"Error running sendall: {str(e)}")