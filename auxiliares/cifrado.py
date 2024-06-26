import hashlib

def encriptar(dato):
    dato = dato.encode(encoding='utf-8')
    h = hashlib.shake_256(dato)
    return h.hexdigest(20)