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

#tablero_bien formado
def compruebo_anchos(t: Tablero) -> bool:
    """
    Indica si todas las filas del tablero tienen exactamente la longitud igual al ANCHO.
    
    PRE: True

    Args:
        t (Tablero): El tablero a evaluar.

    Returns:
        True si todas las filas de *t* tienen longitud ANCHO, False en caso contrario.
    """ 
    for fila in t:
        if len(fila) != ANCHO:
            return False
    return True

def columnas(t:Tablero, indice_columna: int) -> list:
    """
    Devuelve una lista con los elementos de una columna específica del tablero.

    PRE: 0 <= *indice_columna* < ANCHO

    Args:
        t (Tablero): El tablero del cual se extrae la columna.
        indice_columna (int): El índice de la columna a obtener.

    Returns:
        Una lista con los elementos pertenecientes a la columna *indice_columna* del tablero *t*.
    """
    columna: list = []
    for indice_fila in range(len(t)):
        columna.append(t[indice_fila][indice_columna])
    return columna

def compruebo_altos(t: Tablero) -> bool:
    """
    Indica si todas las columnas del tablero tienen exactamente la longitud igual al ALTO.

    PRE: True

    Args:
        t (Tablero): El tablero a evaluar.

    Returns:
        True si todas las columnas de *t* tienen la cantidad esperada de filas ALTO, False en caso contrario.
    """
    if not compruebo_anchos(t):
        return False
    for indice_columnas in range(ANCHO):
        if len(columnas(t,indice_columnas)) != ALTO:
            return False
    return True

def tablero_bien_formado(t : Tablero) -> bool:
    """
    Indica si el tablero cumple simultáneamente con las dimensiones válidas de ANCHO y ALTO.

    PRE: True

    Args:
        t (Tablero): El tablero a validar.

    Returns:
        True si el tablero *t* cumple con el ANCHO y ALTO requeridos, False en caso contrario.
    """   
    return (compruebo_altos(t) and compruebo_anchos(t))



#posicion_en_tablero
def posicion_en_tablero(pos : Posicion) -> bool:
    """
    Indica si una posición está dentro de los límites válidos del tablero (8x8).

    PRE: True

    Args:
        pos (Posicion): La posición a evaluar con atributos fila y columna.

    Returns:
        True si la Posición pertenece al tablero, False en caso contrario.
    """
    return (0 <= pos.fila < ALTO) and (0 <= pos.columna < ANCHO)


#movimiento_bien_formado

def accion_valida(acc:Accion) -> bool:
    """
    Indica si una acción dada pertenece al conjunto de acciones válidas del juego.

    PRE: True

    Args:
        acc (Accion): La acción a evaluar.

    Returns:
        True si acc es una acción válida, False en caso contrario.
    """
    acciones_validas = [MOVER_A_SECAS,ARRASTRAR,EMPUJAR]
    for accion in acciones_validas:
        if  acc == accion:
            return True
    return False


def origen_valido(pos_origen:Posicion):
    """
    Indica si la posicion de origen dada es valida.

    PRE: True

    Args:
        pos_origen (Posicion): origen a evaluar.

    Returns:
        True si pos_origen es una posicion válida, False en caso contrario.
    """
    return posicion_en_tablero(pos_origen)  


def pertenece(lista:list, elem) -> bool:
    """
    Indica si elem pertenece a la lista.
        
    PRE: True
    
    Args:
        lista (list): Lista a la que evaluar.
        elem: elemento que queremos ver si esta en la lista
    Returns:
        True si el elemento esta en la lista, False en caso contrario.
    """
    for elemento in lista:
        if elemento == elem:
            return True  
    return False

def direcciones_validas(pasos:list[Direccion]):
    """
    Indica si todas los direcciones pertenecen al conjunto de direcciones válidas del juego.
    
    PRE: True

    Args:
        pasos (list[Direccion]): Lista de direcciones a evaluar.
    
    Returns:
        True si todas las direcciones son válidas, False en caso contrario.
    """
    direcciones_validas = [NORTE,SUR,ESTE,OESTE]
    for paso in pasos:
        if not pertenece(direcciones_validas,paso):
            return False
    return True

def validar_catidad_pasos(pasos: list[Direccion], acc: Accion) -> bool:
    """
    Indica si la cantidad de direcciones de la secuencia coincide exactamente 
    con la requerida según el tipo de acción.

    PRE: True

    Args:
        pasos (list[Direccion]): Lista con las direcciones a realizar en el movimiento.
        acc (Accion): Tipo de acción que se desea ejecutar.

    Returns:
        True si la longitud de la lista de pasos es válida para la acción dada, 
        False en caso contrario.
    """   
    cant_pasos = len(pasos)
    pasos_MOVER_A_SECAS = 1
    pasos_ARRASTRAR_o_EMPUJAR = 2
    
    if acc == MOVER_A_SECAS and cant_pasos == pasos_MOVER_A_SECAS:
        return True
    elif (acc == ARRASTRAR or acc == EMPUJAR) and cant_pasos == pasos_ARRASTRAR_o_EMPUJAR:
        return True
    else: 
        return False


def movimiento_bien_formado(m : Movimiento) -> bool:
    """
    Indica si un movimiento cumple simultáneamente con la validez de su acción, 
    la posición de origen en el tablero, la secuencia de direcciones y la cantidad de pasos.

    PRE: True

    Args:
        m (Movimiento): El movimiento a evaluar.

    Returns:
        True si el movimiento es válido y está bien formado, False en caso contrario.
    """    
    
    if not accion_valida(m.accion):
        return False
    if not origen_valido(m.origen):
        return False
    if not validar_catidad_pasos(m.pasos, m.accion):
        return False
    if not direcciones_validas(m.pasos):
        return False
    
    return True    


#juego_bien_formado
def juego_bien_formado(j : Juego) -> bool:
    """
    Indica si un estado del juego está bien formado.

    PRE: True

    Args:
        j (Juego): El estado de juego a evaluar.

    Returns:
        True si el juego está bien formado, False en caso contrario.
    """    
    colores_validos = [DORADO,PLATEADO]
    if not tablero_bien_formado(j.tablero):
        return False
    if not (0 <= j.pasos_consumidos < MAX_PASOS):
        return False
    if j.turno not in colores_validos:
        return False
    
    return True

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
    raise Exception("No implementado")

def hay_pieza_amiga_vecina(t : Tablero, pos : Posicion) -> bool:
    raise Exception("No implementado")

def hay_pieza_enemiga_mas_debil_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    raise Exception("No implementado")

def hay_pieza_enemiga_mas_fuerte_vecina(t : Tablero, pos : Posicion) -> bool:
    raise Exception("No implementado")

def hay_pieza_congelada(t : Tablero, pos : Posicion) -> bool:
    raise Exception("No implementado")

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

