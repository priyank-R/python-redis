from enum import Enum
class ERRORS():
    GET_WRONG_ARGS="(error) ERR wrong number of arguments for 'get' command"
    SET_WRONG_ARGS="(error) ERR wrong number of arguments for 'set' command"
    TTL_WRONG_ARGS="(error) ERR wrong number of arguments for 'ttl' command"
    SYNTAX_ERROR="(error) ERR syntax error"
    VALUE_ERROR_INTEGER="(error) ERR value is not integer or is out of range"