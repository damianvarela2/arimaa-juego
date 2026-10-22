from definiciones import *

#### Algunas funciones ya dadas

def son_posiciones_vecinas(pos1 : Posicion, pos2 : Posicion) -> bool: # pragma: no cover
    return (pos1.fila == pos2.fila and abs(pos1.columna - pos2.columna) == 1) \
        or (pos1.columna == pos2.columna and abs(pos1.fila - pos2.fila) == 1)

def direccion_desde_hasta(pos1 : Posicion, pos2 : Posicion) -> Direccion: # pragma: no cover
    assert son_posiciones_vecinas(pos1, pos2)
    if pos1.fila < pos2.fila:
       return NORTE
    elif pos1.fila > pos2.fila:
       return SUR
    elif pos1.columna < pos2.columna:
       return ESTE
    else:
       return OESTE

def pasar_turno(j : Juego) -> Juego: # pragma: no cover
    return Juego(j.tablero, oponente(j.turno), 0)

#### Ejercicio 1

def tablero_bien_formado(t : Tablero) -> bool:
    raise Exception("No implementado")

def posicion_en_tablero(pos : Posicion) -> bool:
    raise Exception("No implementado")

def movimiento_bien_formado(m : Movimiento) -> bool:
    raise Exception("No implementado")

def juego_bien_formado(j : Juego) -> bool:
    raise Exception("No implementado")

#### Ejercicio 2

def posicion_vecina_hacia(pos : Posicion, d : Direccion) -> Posicion:
    raise Exception("No implementado")

def casilla_en_posicion(t : Tablero, p : Posicion) -> Casilla:
    raise Exception("No implementado")

def hay_casilla_vacia(t : Tablero, pos : Posicion) -> bool:
    raise Exception("No implementado")

def hay_pieza_de_color(t : Tablero, pos : Posicion, col : Color) -> bool:
    raise Exception("No implementado")

#### Ejercicio 3

def hay_casilla_vacia_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """
    Indica si hay una casilla vacía en la dirección d desde la posición pos.

    PRE: tableroBienFormado (t) ∧ posicionEnTablero (pos)
    
    Args:
        pos (Posicion): La posición desde donde se busca.
        d (Direccion): La dirección en la que se busca.
        
    Returns:
        True si hay una casilla vacía en la dirección d desde la posición pos, False si no.
    """
    if posicion_en_tablero(posicion_vecina_hacia(pos, d)) and casilla_en_posicion(t, posicion_vecina_hacia(pos, d)) == VACIA:
        return True
    return False

def hay_pieza_amiga_vecina(t : Tablero, pos : Posicion) -> bool:
    """
    Indica si hay una pieza amiga vecina a la posición pos.

    PRE: tableroBienFormado (t) ∧ posicionEnTablero (pos)
        hayPieza (t, pos)

    Args:
        t (Tablero): El tablero en el que se busca.
        pos (Posicion): La posición desde donde se busca.
        
    Returns:
        True si hay una pieza amiga vecina a la posición pos, False si no.
    """
    for d in [NORTE, SUR, ESTE, OESTE]:
        if posicion_en_tablero(posicion_vecina_hacia(pos, d)) and hay_pieza_de_color(t, posicion_vecina_hacia(pos, d), casilla_en_posicion(t, pos).color):
            return True
    return False


def hay_pieza_enemiga_mas_debil_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """
    Indica si hay una pieza enemiga más débil en la dirección d desde la posición pos.

    PRE: tableroBienFormado (t) ∧ posicionEnTablero (pos)
        hayPieza (t, pos)

    Args:
        t (Tablero): El tablero en el que se busca.
        pos (Posicion): La posición desde donde se busca.
        d (Direccion): La dirección en la que se busca.
        
    Returns:
        True si hay una pieza enemiga más débil en la dirección d desde la posición pos, False si no.
    """
    if posicion_en_tablero(posicion_vecina_hacia(pos, d)) and casilla_en_posicion(t, posicion_vecina_hacia(pos, d)) != VACIA and hay_pieza_enemiga_debil(t, pos, d):
        return True
    return False

def hay_pieza_enemiga_debil(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """
    Indica si hay una pieza enemiga más débil en la dirección d desde la posición pos.

    PRE: tableroBienFormado (t) ∧ posicionEnTablero (pos)
        hayPieza (t, pos)
        direccionValida (d, pos)
        hayPiezaEnDireccionD (t, pos, d)

    Args:
        t (Tablero): El tablero en el que se busca.
        pos (Posicion): La posición desde donde se busca.
        d (Direccion): La dirección en la que se busca.
        
    Returns:
        True si hay una pieza enemiga más débil en la dirección d desde la posición pos, False si no.
    """
    if casilla_en_posicion(t, posicion_vecina_hacia(pos, d)).fuerza < casilla_en_posicion(t, pos).fuerza and casilla_en_posicion(t, posicion_vecina_hacia(pos, d)).color == oponente(casilla_en_posicion(t, pos).color):
        return True
    return False

def hay_pieza_enemiga_mas_fuerte_vecina(t : Tablero, pos : Posicion) -> bool:
    """
    Indica si hay una pieza enemiga más fuerte vecina a la posición pos.

    PRE: tableroBienFormado (t) ∧ posicionEnTablero (pos)
        hayPieza (t, pos)

    Args:
        t (Tablero): El tablero en el que se busca.
        pos (Posicion): La posición desde donde se busca.

        
    Returns:
        True si hay una pieza enemiga más fuerte vecina a la posición pos, False si no.
    """
    for d in [NORTE, SUR, ESTE, OESTE]:
        if posicion_en_tablero(posicion_vecina_hacia(pos, d)) and casilla_en_posicion(t, posicion_vecina_hacia(pos, d)) != VACIA and hay_pieza_enemiga_fuerte_hacia(t, pos, d):
            return True
    return False

def hay_pieza_enemiga_fuerte_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """
    Indica si hay una pieza enemiga más fuerte en la dirección d desde la posición pos.

    PRE: tableroBienFormado (t) ∧ posicionEnTablero (pos)
        hayPieza (t, pos)
        direccionValida (d, pos)
        hayPiezaEnDireccionD (t, pos, d)

    Args:
        t (Tablero): El tablero en el que se busca.
        pos (Posicion): La posición desde donde se busca.
        d (Direccion): La dirección en la que se busca.
        
    Returns:
        True si hay una pieza enemiga más fuerte en la dirección d desde la posición pos, False si no.
    """
    if casilla_en_posicion(t, posicion_vecina_hacia(pos, d)).fuerza > casilla_en_posicion(t, pos).fuerza and casilla_en_posicion(t, posicion_vecina_hacia(pos, d)).color == oponente(casilla_en_posicion(t, pos).color):
        return True
    return False

def hay_pieza_congelada(t : Tablero, pos : Posicion) -> bool:
    """
    Indica si hay una pieza congelada en la posición pos.

    PRE: tableroBienFormado (t) ∧ posicionEnTablero (pos)

    Args:
        t (Tablero): El tablero en el que se busca.
        pos (Posicion): La posición desde donde se busca.

    Returns:
        True si hay una pieza congelada en la posición pos, False si no.
    """
    if hay_pieza_de_color(t, pos, casilla_en_posicion(t, pos).color) and hay_pieza_enemiga_mas_fuerte_vecina(t, pos) and not hay_pieza_amiga_vecina(t, pos):
        return True
    return False

#### Ejercicio 4

def puede_realizar_movimiento(j : Juego, m : Movimiento) -> bool:
    raise Exception("No implementado")

#### Ejercicio 5

def activar_trampas(t : Tablero) -> Tablero:
    raise Exception("No implementado")

#### Ejercicio 6

def realizar_movimiento(j : Juego, m : Movimiento) -> Juego:
    raise Exception("No implementado")

#### Ejercicio 7

def hay_ganador_determinado(j : Juego) -> bool:
    raise Exception("No implementado")

def ganador_del_juego(j : Juego) -> Color:
    raise Exception("No implementado")

