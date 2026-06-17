class RedisCmd:

    def __init__(self, cmd: str, args: list[str]):
        self.cmd = cmd
        self.args = args
