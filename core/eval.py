import socket
import logging
from datetime import datetime 


from core.errors import ERRORS
from core.cmd import RedisCmd
from core.store import NewObj, Put, Get, Delete, Expire

logger = logging.getLogger()


RESPNIL = "$-1\r\n".encode()

def Encode(o: object, isSimple: bool) -> list[bytes]:
    if isinstance(o, str): 
        if isSimple: 
            return f"+{o}\r\n".encode()
        else:
            return f"${len(o)}\r\n{o}\r\n".encode()
    if isinstance(o, int):
        return f":{o}\r\n".encode()
        
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

def evalGET(args: list[str], client: socket.socket):
    if len(args) < 1:
        return Exception(ERRORS.GET_WRONG_ARGS)
    
    obj = Get(args[0])
    if obj is None: 
        client.sendall(RESPNIL)
        return None
    
    if obj.expiryMs != -1 and obj.expiryMs < datetime.now().timestamp() * 1000:
        client.sendall(RESPNIL)
        return None
    
    client.sendall(Encode(obj.value, False))
    return None
    

def evalSET(args: list[str], client: socket.socket):
    if len(args) < 2:
        return Exception(ERRORS.SET_WRONG_ARGS)
    
    key, value = args[0], args[1]
    exDurationMs = -1

    if len(args) > 2:
        i = 2
        while True:
            match args[i]:
                case "EX" | "ex":
                    i+=1
                    if i == len(args):
                        return Exception(ERRORS.SYNTAX_ERROR)
                    try:
                        exDurationSec = int(args[i])
                    except ValueError:
                        return Exception(ERRORS.VALUE_ERROR_INTEGER) 
                    
                    exDurationMs = exDurationSec * 1000
                case _:
                    return Exception(ERRORS.SYNTAX_ERROR)
                
            break
    Put(key, NewObj(value, exDurationMs))
    client.sendall("+OK\r\n".encode())
    return None 

def evalTTL(args: list[str], client: socket.socket):
    if len(args) != 1:
        return Exception(ERRORS.TTL_WRONG_ARGS)

    obj = Get(args[0])
    if obj is None:
        client.sendall(RESPNIL)
        return None
    
    if obj.expiryMs == -1:
        client.sendall(":-1\r\n".encode())
        return None
    
    durationMs = obj.expiryMs - (datetime.now().timestamp() * 1000)
    if durationMs < 0:
        client.sendall(":-2\r\n".encode())
        return None
    
    client.sendall(Encode(int(durationMs // 1000), False))
    return None

def evalDEL(args: list[str], client: socket.socket):
    if len(args) == 0:
        return Exception(ERRORS.DEL_WRONG_ARGS)
    deleted_keys = 0
    for arg in args:
        if Delete(arg):
            deleted_keys+=1
    
    client.sendall(Encode(deleted_keys, False))
    return None

def evalEXPIRE(args: list[str], client: socket.socket): 
    if len(args) < 2: 
        return Exception(ERRORS.EXPIRE_WRONG_ARGS)
    
    try:
        key = args[0]
        expiryMs = int(args[1]) * 1000
    except:
        return Exception(ERRORS.SYNTAX_ERROR)
    
    expired = Expire(key, expiryMs)
    client.sendall(Encode(expired, False))
    return None 
    
def evalAndRespond(cmd: RedisCmd, client: socket.socket) -> Exception | None:
    command = cmd.cmd
    args = cmd.args

    logger.info(f"evalAndRespond args {args}")

    if command.upper() == 'PING':
        return evalPING(args, client)
    if command.upper() == 'GET':
        return evalGET(args,client)
    if command.upper() == 'SET':
        return evalSET(args,client)
    if command.upper() == 'TTL':
        return evalTTL(args,client)
    if command.upper() == 'DEL':
        return evalDEL(args,client)
    if command.upper() == 'EXPIRE':
        return evalEXPIRE(args,client)
    
    
    evalPING([], client)