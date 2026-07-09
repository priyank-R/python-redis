from datetime import datetime
class NewObj():
    value: object
    expiryMs: int = -1
    def __init__(self, value: object, expiryMs: int):
        self.value = value
        if expiryMs > 0:
            self.expiryMs = (datetime.now().timestamp() * 1000) + expiryMs

store: dict[str, NewObj] = {}

def Put(key: str, obj: NewObj)->None:
    store[key] = obj

def Get(key)->NewObj | None:
    return store.get(key, None)


