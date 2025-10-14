from collections import deque
from collections import deque

def find_path(origen, destino, nodos, bloqueados=None):
    if origen == destino:
        return [origen]
    visitados = set()
    cola = deque([[origen]])
    while cola:
        camino = cola.popleft()
        nodo_id = camino[-1]
        if nodo_id == destino:
            return camino
        visitados.add(nodo_id)
        for vecino_id in nodos[nodo_id].adyacentes:
            if  vecino_id not in visitados:
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino_id)
                cola.append(nuevo_camino)
    return None



def find_safe_path(origen, destino, grafo, minas, autos):
    """
    Versión extendida: evita tanto minas como autos.
    """
    
    bloqueados = set(minas) | set(autos)
    return find_path(origen, destino, grafo, bloqueados)


