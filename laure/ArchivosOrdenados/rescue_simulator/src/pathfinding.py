from collections import deque

def find_path(origen, destino, nodos):
    """
    nodos: dict[str, Nodo]
    """
    if origen == destino:
        return [origen]

    visitados = set()
    cola = deque([[origen]])

    while cola:
        camino = cola.popleft()
        nodo_id = camino[-1]
        nodo_actual = nodos[nodo_id]

        if nodo_actual.ocupado:
            continue

        if nodo_id == destino:
            return camino

        visitados.add(nodo_id)

        for vecino_id in nodo_actual.adyacentes:
            vecino = nodos[vecino_id]
            if not vecino.ocupado and vecino_id not in visitados:
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
