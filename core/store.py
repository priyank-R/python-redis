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

def Delete(key)->bool:
    if store.get(key):
        del store[key]
        return True
    return False

def Expire(key, expiryMs)->int:
    value = Get(key)
    if value and value.expiryMs > datetime.now().timestamp() * 1000:
        # update the expiry 
        value.expiryMs = datetime.now().timestamp() * 1000 + expiryMs
        return 1
    return 0
    


