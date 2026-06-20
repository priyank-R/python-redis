from core.cmd import RedisCmd
import socket
import logging

logger = logging.getLogger()



def Encode(o: object, isSimple: bool) -> list[bytes]:
    if isinstance(o, str): 
        if isSimple: 
            return f"+{o}\r\n".encode()
        else:
            return f"${len(o)}\r\n{o}\r\n".encode()
        
    return bytearray()

PONG_RESPONSE = b"+PONG\r\n"
def evalPING(args: list[str], client: socket.socket):
    if len(args) >= 2:
        return Exception("ERR wrong number of arguments for 'ping' command")
    
    if len(args) == 0:
        b = PONG_RESPONSE
    else:
        b = Encode(args[0], False)
    try: 
        client.sendall(b)
    except Exception as e:
        logger.error(e)
        return e        


def evalAndRespond(cmd: RedisCmd, client: socket.socket) -> Exception | None:
    command = cmd.cmd
    args = cmd.args

    logger.info(f"evalAndRespond args {args}")

    if command.upper() == 'PING':
        return evalPING(args, client)
    
    evalPING([], client)