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



#Defino copiar_tablero(t), usenla para que no se les modifique el parametro de entrada
def copiar_tablero(t:Tablero)->Tablero:
    res:Tablero=[]
    for fila in t:
        fila_copia:list[Casilla]=[]
        for casilla in fila:
            fila_copia.append(casilla)
        res.append(fila_copia)
    return res

    
#### Ejercicio 1

#tablero_bien formado
#AUXILIAR
def compruebo_anchos(t: Tablero) -> bool:
    """
    Indica si todas las filas del tablero tienen exactamente la longitud igual al ANCHO.
    
    PRE: True

    Args:
        t (Tablero): El tablero a evaluar.

    Returns:
        True si todas las filas de *t* tienen longitud ANCHO, False en caso contrario.
    """ 
    res:bool=True
    for fila in t:
        if len(fila) != ANCHO:
            res=False
    return res
#AUXILIAR
def columnas(t:Tablero, indice_columna: int) -> list[Casilla]:
    """
    Devuelve una lista con los elementos de una columna específica del tablero.

    PRE: 0 <= *indice_columna* < ANCHO

    Args:
        t (Tablero): El tablero del cual se extrae la columna.
        indice_columna (int): El índice de la columna a obtener.

    Returns:
        Una lista con los elementos pertenecientes a la columna *indice_columna* del tablero *t*.
    """
    columna: list[Casilla] = []
    for indice_fila in range(len(t)):
        columna.append(t[indice_fila][indice_columna])
    return columna
#AUXILIAR
def compruebo_altos(t: Tablero) -> bool:
    """
    Indica si todas las columnas del tablero tienen exactamente la longitud igual al ALTO.

    PRE: True

    Args:
        t (Tablero): El tablero a evaluar.

    Returns:
        True si todas las columnas de *t* tienen la cantidad esperada de filas ALTO, False en caso contrario.
    """
    res:bool=True
    if not compruebo_anchos(t):
        res=False
    else:
        for indice_columnas in range(ANCHO):
            if len(columnas(t,indice_columnas)) != ALTO:
                res=False
    return res

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
#aux
def accion_valida(acc:Accion) -> bool:
    """
    Indica si una acción dada pertenece al conjunto de acciones válidas del juego.

    PRE: True

    Args:
        acc (Accion): La acción a evaluar.

    Returns:
        True si acc es una acción válida, False en caso contrario.
    """
    res:bool=False
    acciones_validas:list[Accion] = [MOVER_A_SECAS,ARRASTRAR,EMPUJAR]
    for accion in acciones_validas:
        if  acc == accion:
            res=True
    return res

#aux
def origen_valido(pos_origen:Posicion)->bool:
    """
    Indica si la posicion de origen dada es valida.

    PRE: True

    Args:
        pos_origen (Posicion): origen a evaluar.

    Returns:
        True si pos_origen es una posicion válida, False en caso contrario.
    """
    return posicion_en_tablero(pos_origen)  
#aux
def direcciones_validas(pasos:list[Direccion])->bool:
    """
    Indica si todas los direcciones pertenecen al conjunto de direcciones válidas del juego.
    
    PRE: True

    Args:
        pasos (list[Direccion]): Lista de direcciones a evaluar.
    
    Returns:
        True si todas las direcciones son válidas, False en caso contrario.
    """
    res:bool=True
    direcciones_validas:list[Direccion] = [NORTE,SUR,ESTE,OESTE]
    for paso in pasos:
        if paso not in direcciones_validas:
            res=False
    return res
#aux
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
    cant_pasos:int = len(pasos)
    pasos_MOVER_A_SECAS:int = 1
    pasos_ARRASTRAR_o_EMPUJAR:int = 2
    return ((acc == MOVER_A_SECAS and cant_pasos == pasos_MOVER_A_SECAS) or ((acc == ARRASTRAR or acc == EMPUJAR) and cant_pasos == pasos_ARRASTRAR_o_EMPUJAR))

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

    return (accion_valida(m.accion) and origen_valido(m.origen) and validar_catidad_pasos(m.pasos, m.accion) and direcciones_validas(m.pasos))


#juego_bien_formado
def juego_bien_formado(j : Juego) -> bool:
    """
    Indica si un estado del juego está bien formado.

    PRE: True

    Args:
        j (Juego): El juego a evaluar.

    Returns:
        True si el juego está bien formado, False en caso contrario.
    """    
    return (tablero_bien_formado(j.tablero) and (0 <= j.pasos_consumidos < MAX_PASOS))#lo de colores no esta en la especificacion a proposito?

#### Ejercicio 2

def posicion_vecina_hacia(pos : Posicion, d : Direccion) -> Posicion:
    """
    Dada una dirección *d*, devuelve una posición *Posicion* vecina en esa dirección
    PRE : True
    Args:
        pos (Posicion): Una tupla de enteros que indica coordenadas en el tablero
        d (Direccion): NORTE, SUR, ESTE, OESTE
    Returns:
        Posicion (Posicion): Una tupla de enteros al NORTE, SUR, ESTE, OESTE de pos dependiendo d
    """
    res: Posicion
    if d == NORTE:
        res = Posicion(pos.fila + 1, pos.columna)
    elif d == SUR:
        res = Posicion(pos.fila - 1, pos.columna)
    elif d == ESTE:
        res = Posicion(pos.fila, pos.columna + 1)
    else:
        res = Posicion(pos.fila, pos.columna - 1)
    return res

def casilla_en_posicion(t : Tablero, pos : Posicion) -> Casilla:
    """
    Dado un tablero *t* y una posición *pos*, devuelve la Casilla (VACIA O FIGURA) ubicada en esa posicion *p* de tablero *t*
    PRE: tablero_bien_formado(t) == True and posicion_en_tablero(pos) == True
    Args:
        t (Tablero): Una secuencia de secuencias de Casillas (VACIA O FIGURA)
        pos (Posicion): Una tupla de enteros que indica coordenadas en el tablero
    Returns:
        Casilla (VACIA O FIGURA): Devuelve la casilla (VACIA O FIGURA) correspondiente a esa posicion *pos* en el tablero *t*
    """
    res:Casilla = t[pos.fila][pos.columna]
    return res

def hay_casilla_vacia(t : Tablero, pos : Posicion) -> bool:
    """
    Dado un tablero *t* y una posición *pos*, devuelve la True si el valor de la Casilla (VACIA O FIGURA) en esa posicion *pos* es VACIA
    PRE: tablero_bien_formado(t) == True and posicion_en_tablero(pos) == True
    Args:
        t (Tablero): Una secuencia de secuencias de Casillas (VACIA O FIGURA)
        pos (Posicion): Una tupla de enteros que indica coordenadas en el tablero
    Returns:
        True si Casilla (VACIA O FIGURA) es VACIA
    """
    casilla : Casilla = casilla_en_posicion(t, pos)
    return casilla == VACIA

def hay_pieza_de_color(t : Tablero, pos : Posicion, col : Color) -> bool:
    """
    Dado un tablero *t* y una posición *pos*, y un color *col*, devuelve True si el color de la FIGURA en la CASILLA correspondiente a POSICION es igual a col. 
    PRE: tablero_bien_formado(t) == True and posicion_en_tablero(pos) == True
    Args:
        t (Tablero): Una secuencia de secuencias de Casillas (VACIA O FIGURA)
        pos (Posicion): Una tupla de enteros que indica coordenadas en el tablero
        col (Color): La posicion 1 en la tupla FIGURA. str que representa el color de las piezas (Plateado o Dorado)
    Returns:
        True si el color (Color) de la Pieza (Figura, Color) en la posicion *pos* de tablero *t* es igual a al color ingresado *col*
    """
    casilla : Casilla = casilla_en_posicion(t, pos)
    return (not hay_casilla_vacia(t, pos) and casilla.color == col)

#### Ejercicio 3

def hay_casilla_vacia_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """
    Indica si hay una casilla vacía en la dirección d desde la posición pos.

    PRE: tableroBienFormado (t) ∧ posicionEnTablero (pos)
    
    Args:
        t (Tablero): Una secuencia de secuencias de Casillas (VACIA O FIGURA)
        pos (Posicion): La posición desde donde se busca.
        d (Direccion): La dirección en la que se busca.
        
    Returns:
        True si hay una casilla vacía en la dirección d desde la posición pos, False si no.
    """
    return (posicion_en_tablero(posicion_vecina_hacia(pos, d)) and casilla_en_posicion(t, posicion_vecina_hacia(pos, d)) == VACIA)

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
    res:bool=False
    for d in [NORTE, SUR, ESTE, OESTE]:
        if posicion_en_tablero(posicion_vecina_hacia(pos, d)) and hay_pieza_de_color(t, posicion_vecina_hacia(pos, d), casilla_en_posicion(t, pos).color):
            res=True
    return res


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
    return (posicion_en_tablero(posicion_vecina_hacia(pos, d)) and casilla_en_posicion(t, posicion_vecina_hacia(pos, d)) != VACIA and hay_pieza_enemiga_debil(t, pos, d))

def hay_pieza_enemiga_debil(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """
    Indica si la pieza vecina es una enemiga más débil en la dirección d desde la posición pos.

    PRE: tableroBienFormado (t) ∧ posicionEnTablero (pos)
        hayPieza (t, pos)
        direccionValida (d, pos)
        hayPiezaEnDireccionD (t, pos, d)

    Args:
        t (Tablero): El tablero en el que se busca.
        pos (Posicion): La posición desde donde se busca.
        d (Direccion): La dirección en la que se busca.
    Returns:
        True si la pieza vecina es una enemiga más débil en la dirección d desde la posición pos, False si no.
    """

    return fuerza(casilla_en_posicion(t, posicion_vecina_hacia(pos, d)).figura) < fuerza(casilla_en_posicion(t, pos).figura) and casilla_en_posicion(t, posicion_vecina_hacia(pos, d)).color == oponente(casilla_en_posicion(t, pos).color)


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
    res:bool=False
    for d in [NORTE, SUR, ESTE, OESTE]:
        if posicion_en_tablero(posicion_vecina_hacia(pos, d)) and casilla_en_posicion(t, posicion_vecina_hacia(pos, d)) != VACIA and hay_pieza_enemiga_fuerte_hacia(t, pos, d):
            res=True
    return res

def hay_pieza_enemiga_fuerte_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """
    Indica si la pieza vecina es una enemiga más fuerte en la dirección d desde la posición pos.

    PRE: tableroBienFormado (t) ∧ posicionEnTablero (pos)
        hayPieza (t, pos)
        direccionValida (d, pos)
        hayPiezaEnDireccionD (t, pos, d)

    Args:
        t (Tablero): El tablero en el que se busca.
        pos (Posicion): La posición desde donde se busca.
        d (Direccion): La dirección en la que se busca.
        
    Returns:
        True si la pieza vecina es una enemiga más fuerte en la dirección d desde la posición pos, False si no.
    """
    return (fuerza(casilla_en_posicion(t, posicion_vecina_hacia(pos, d)).figura) > fuerza(casilla_en_posicion(t, pos).figura) and casilla_en_posicion(t, posicion_vecina_hacia(pos, d)).color == oponente(casilla_en_posicion(t, pos).color))
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
    return not hay_casilla_vacia(t,pos) and hay_pieza_enemiga_mas_fuerte_vecina(t, pos) and not hay_pieza_amiga_vecina(t, pos)

#### Ejercicio 4
def direccionDeMovimientoHabilitada(t : Tablero , pos : Posicion , d : Direccion )->bool:#es uno de los predicados
    """
    Indica si la direccion para el movimiento habilitada
    PRE: True
    Args:
    t (Tablero): El tablero actual
    pos (Posicion): Posicion de la que parto
    d (Direccion): Direccion a la que me desplazo
    Returns:
    True si el movimiento esta habilitado, False sino
    """
    res:bool=False
    casilla:Casilla =casilla_en_posicion(t,pos)
    if (casilla != VACIA):
        f:Figura=casilla.figura
        col:Color=casilla.color
        es_dorado_invalido:bool = (f==CONEJO and col==DORADO and d==SUR)
        es_plateado_invalido:bool = (f==CONEJO and col==PLATEADO and d==NORTE)            
        res=not (es_dorado_invalido or es_plateado_invalido)
    return res


def puedeMoverASecas(t:Tablero,pos:Posicion,d:Direccion)->bool:#es uno de los predicados
    """
    Indica si en la direccion para el movimiento es posible mover a secas
    PRE: True
    Args:
    t (Tablero): El tablero actual
    pos (Posicion): Posicion de la que parto
    d (Direccion): Direccion a la que me desplazo
    Returns:
    True si es posible el movimiento a secas, False sino
    """
    return (hay_casilla_vacia_hacia(t,pos,d))

def puedeArrastrar(t:Tablero,pos:Posicion,d:Direccion,d_arrastre:Direccion)->bool:#es uno de los predicados
    """
    Indica si en la direccion para el movimiento es posible arrastrar
    PRE: True
    Args:
    t (Tablero): El tablero actual
    pos (Posicion): Posicion de la que parto
    d (Direccion): Direccion a la que me desplazo
    d_arrastre (Direccion): Direccion a la que arrastro
    Returns:
    True si es posible arrastrar, False sino
    """
    return (hay_casilla_vacia_hacia(t,pos,d) and hay_pieza_enemiga_mas_debil_hacia(t,pos,opuesta(d_arrastre)))


def puedeEmpujar(t:Tablero,pos:Posicion,d:Direccion,d_empuje:Direccion)->bool:#es uno de los predicados
    """
    Indica si en la direccion para el movimiento es posible empujar
    PRE: True
    Args:
    t (Tablero): El tablero actual
    pos (Posicion): Posicion de la que parto
    d (Direccion): Direccion a la que me desplazo
    d_empuje (Direccion): Direccion a la que empujo
    Returns:
    True si es posible empujar, False sino
    """
    pos_enemiga:Posicion=posicion_vecina_hacia(pos,d)
    return(hay_pieza_enemiga_mas_debil_hacia(t,pos,d) and hay_casilla_vacia_hacia(t,pos_enemiga,d_empuje))



def puedeRealizarAccion(t : Tablero , m : Movimiento )->bool:#es uno de los predicados
    """
    Indica si es posible realizar un determinado movimiento en un tablero
    PRE: True
    Args:
    t (Tablero): El tablero actual
    m (Movimiento): el movimiento a realizar
    Returns:
    True si es posible realizar movimiento, False sino
    """
    return (m.accion==MOVER_A_SECAS and puedeMoverASecas(t, m.origen , m.pasos[0])) or (m.accion==ARRASTRAR and puedeArrastrar(t, m.origen , m.pasos[0] , m.pasos[1])) or (m.accion==EMPUJAR and puedeEmpujar(t, m.origen , m.pasos[0] , m.pasos[1]))


def puede_realizar_movimiento(j : Juego, m : Movimiento) -> bool:#es consigna
    """
    Indica si el movimiento se puede realizar o no
    PRE: juegoBienFormado (j ) ∧ movimientoBienFormado (m)
    Args:
    j (Juego): estado actual del juego
    m (Movimiento): el movimiento a realizar
    Returns:
    True si es el movimiento es posible, False sino
    """
    return(hay_pieza_de_color(j.tablero,m.origen,j.turno) and (not (hay_pieza_congelada(j.tablero,m.origen))) and (direccionDeMovimientoHabilitada(j.tablero,m.origen,m.pasos[0])) and  (j.pasos_consumidos + len(m.pasos)<=MAX_PASOS) and (puedeRealizarAccion(j.tablero,m)))
#para este punto supuse el correcto funcionamiento de hay_pieza_de_color,hay_pieza_congelada,casilla_en_posicion,posicion_vecina_hacia,hay_pieza_enemiga_mas_debil_hacia,hay_casilla_vacia_hacia

#### Ejercicio 5

def sacar_pieza_tablero(t: Tablero, postrampa: Posicion) -> Tablero: #Es funcion auxiliar
    """
        Dado un tablero *t* y una posición trampa *postrampa*, devuelve el tablero resultante de sacar la pieza en postrampa, esa casilla queda vacia
        PRE: tablero_bien_formado(t) == True and posicion_en_tablero(postrampa) == True
        Args:
            t (Tablero): Una secuencia de secuencias de Casillas (VACIA O FIGURA)
            postrampa (Posicion): Una tupla de enteros que indica coordenadas en el tablero y postrampa pertenece a POSICIONES_TRAMPA
        Returns:
            Si hay_pieza_amiga_vecina(t, postrampa), devuelve un tablero igual a *t*.
            Si no, devuelve un tablero con la casilla de *postrampa* VACIA.
    """
    res : Tablero = []
    for i in range(len(t)):
        fila: list[Casilla] = []
        for j in range(len(t[i])):
            if i == postrampa.fila and j == postrampa.columna:
                fila.append(VACIA)
            else:
                fila.append(t[i][j])
        res.append(fila)
    return res

def tablero_despues_de_activar_trampa(t: Tablero, postrampa: Posicion) -> Tablero: #Es funcion auxiliar
    """
        Dado un tablero *t* y una posición trampa *postrampa*, devuelve un Tablero (list[list[Casilla]]) con Casilla = VACIA si la posición de la casilla = posicion trampa 
        PRE: tablero_bien_formado(t) == True and posicion_en_tablero(postrampa) == True
        Args:
            t (Tablero): Una secuencia de secuencias de Casillas (VACIA O FIGURA)
            postrampa (Posicion): Una tupla de enteros que indica coordenadas en el tablero y postrampa pertenece a POSICIONES_TRAMPA
        Returns:
            Si existen figuras en postrampa y estas no tienen piezas amigas vecinas, entonces devuelve un tablero con las casillas que corresponden a postrampa VACIAS. 
            Si no, devuelve el mismo tablero.
    """
    res:Tablero=t
    if not hay_casilla_vacia(t, postrampa) and not hay_pieza_amiga_vecina(t,postrampa):
        res = sacar_pieza_tablero(t,postrampa)
    return res

def tablero_despues_de_activar_todas_las_trampas(t: Tablero) -> Tablero: #Es funcion auxiliar
    """
    Dado un tablero *t*, devuelve el tablero resultante de activar, una tras otra, todas las trampas de POSICIONES_TRAMPA, en ese orden. Cada trampa se activa sobre el resultado de la anterior.
    PRE: tablero_bien_formado(t) == True
    Args:
        t (Tablero): Una secuencia de secuencias de Casillas (VACIA o Pieza)
     Returns:
        Un tablero con las trampas ya activadas. 
    """
    res : Tablero = t
    for postrampa in POSICIONES_TRAMPA:
       res = tablero_despues_de_activar_trampa(res,postrampa)
    return res


def activar_trampas(t : Tablero) -> Tablero:
    """
        Dado un tablero *t*, devuelve el tablero resultante de activar todas las trampas y el tablero es válido.
        PRE: True
        Args:
            t (Tablero): Una secuencia de secuencias de Casillas (VACIA o Pieza)
        Returns:
        Un tablero bien formado, igual a *t* salvo en las trampas de POSICIONES_TRAMPA donde no había pieza amiga vecina, que quedan VACIAS.
    """

    res:Tablero = tablero_despues_de_activar_todas_las_trampas(copiar_tablero(t))
    return res

#### Ejercicio 6

# problema realizar_movimiento ( in j : Juego , in m : Movimiento ) : Juego {
# r e q u i e r e { juegoBienFormado (j ) ∧ movimientoBienFormado (m) }
# r e q u i e r e { puedeRealizarMovimiento (j , m) }
# asegura { juegoBienFormado (res) }
# asegura { juegoPostMovimiento (j , res, m) }
# }
# entonces j y m estan bien formados, y el movimiento es posible en el juego dado

# aux juegoPostMovimiento (j0 , j1 : Juego , m : Movimiento ) :=
# tableroPostMovimiento (j0 . tablero , j1 . tablero , m) ∧ j uegoConTurnoPosiblementeAvanzado (j0 , j1 , m)
#hay que implementar esto

# aux tableroPostMovimiento (t0 , t1 : Tablero , m : Movimiento ) :=
# (m. acci ó n = Mover_a_secas →
# tableroPostMoverASecas (t0 , t1 , m. origen , m. pasos [0]))
# ∧ (m. acci ó n = Arrastrar →
# tableroPostArrastrar (t0 , t1 , m. origen , m. pasos [0] , m. pasos [1]))
# ∧ (m. acci ó n = Empujar →
# tableroPostEmpujar (t0 , t1 , m. origen , m. pasos [0] , m. pasos [1]))

def tableroPostMovimiento(t:Tablero,m:Movimiento)->Tablero:
    """
    Dado un tablero *t*, devuelve el tablero resultante del movimiento
    PRE: True
    Args:
        t (Tablero): Una secuencia de secuencias de Casillas (VACIA o Pieza)
        m (Movimiento): El movimiento que sera efectuado en el tablero
     Returns:
        Un tablero habiendo hecho el movimiento m. 
    """
    res:Tablero=[]
    if(m.accion==MOVER_A_SECAS):
        res=tableroPostMoverASecas(t,m)
    elif(m.accion==EMPUJAR):
        res=tableroPostEmpujar(t,m)
    else:
        res=tableroPostArrastrar(t,m)
    return res

def tableroTrasladandoPieza(t:Tablero,p_inicial:Posicion,p_objetivo:Posicion)->Tablero:
    """
    Dado un tablero *t*, y 2 posiciones *p_inicial* y *p_objetivo* devuelve un tablero habiendo trasladado el contenido de p_inicial hacia p_objetivo
    PRE: True
    Args:
        t (Tablero): Una secuencia de secuencias de Casillas (VACIA o Pieza)
        p_inicial (Posicion): Posicion a desplazar
        p_objetivo (Posicion): Objetivo del movimiento
     Returns:
        Un tablero habiendo hecho el traslado de piezas. 
    """
    res: Tablero = copiar_tablero(t)
    res[p_objetivo.fila][p_objetivo.columna] = t[p_inicial.fila][p_inicial.columna]
    res[p_inicial.fila][p_inicial.columna] = VACIA
    return res



def tableroPostMoverASecas(t:Tablero,m:Movimiento)->Tablero:
    """
    Dado un tablero *t*, y movimiento *m* devuelve un tablro habiendo realizado la accion MOVER_A_SECAS dado por movimiento
    PRE: True
    Args:
        t (Tablero): Una secuencia de secuencias de Casillas (VACIA o Pieza)
        m (Movimiento): El movimiento que sera efectuado en el tablero
     Returns:
        Un tablero habiendo hecho el movimiento m con la accion MOVER_A_SECAS. 
    """
    res:Tablero=[]
    pos:Posicion=m.origen
    pos_destino:Posicion=posicion_vecina_hacia(pos,m.pasos[0])
    res=tableroTrasladandoPieza(t,pos,pos_destino)
    res=activar_trampas(res)
    return res


def tableroPostEmpujar(t:Tablero,m:Movimiento)->Tablero:
    """
    Dado un tablero *t*, y movimiento *m* devuelve un tablro habiendo realizado la accion EMPUJAR dado por movimiento
    PRE: True
    Args:
        t (Tablero): Una secuencia de secuencias de Casillas (VACIA o Pieza)
        m (Movimiento): El movimiento que sera efectuado en el tablero
     Returns:
        Un tablero habiendo hecho el movimiento m con la accion EMPUJAR. 
    """
    res:Tablero=copiar_tablero(t)
    pos_enemiga:Posicion = posicion_vecina_hacia(m.origen, m.pasos[0])
    pos_objetivo:Posicion = posicion_vecina_hacia(pos_enemiga, m.pasos[1])
    res=tableroTrasladandoPieza(res, pos_enemiga,pos_objetivo)
    res=tableroTrasladandoPieza(res, m.origen,pos_enemiga)
    res = activar_trampas(res)
    return res


def tableroPostArrastrar(t:Tablero,m:Movimiento)->Tablero:
    """
    Dado un tablero *t*, y movimiento *m* devuelve un tablro habiendo realizado la accion ARRASTRAR dado por movimiento
    PRE: True
    Args:
        t (Tablero): Una secuencia de secuencias de Casillas (VACIA o Pieza)
        m (Movimiento): El movimiento que sera efectuado en el tablero
     Returns:
        Un tablero habiendo hecho el movimiento m con la accion ARRASTRAR. 
    """
    res:Tablero=copiar_tablero(t)
    pos_enemiga:Posicion=posicion_vecina_hacia(m.origen,opuesta(m.pasos[1]))
    pos_objetivo:Posicion=posicion_vecina_hacia(m.origen,m.pasos[0])
    res=tableroTrasladandoPieza(res, m.origen,pos_objetivo)
    res=tableroTrasladandoPieza(res,pos_enemiga ,m.origen)
    res = activar_trampas(res)
    return res

def hayQueCambiarDeTurno(j:Juego,m:Movimiento)->bool:
    """
    Dado un juego *j*, y movimiento *m* devuelve un resultado booleano según si hay que cambiar de turno o no
    PRE: True
    Args:
        j (Juego): estado actual del juego
        m (Movimiento): El movimiento que sera efectuado en el turno
     Returns:
        True si hay que cambiar de turno, False sino. 
    """
    return((j.pasos_consumidos + len(m.pasos))==MAX_PASOS)
#definir los 3 tableros posmovimientos, hay que tener cuidado de no modificar t ni m
# ahora bien, res debe ser un juegobienformado, y j

#Estoy asumiendo el correcto funcionamiento de:
#juego_bien_formado. posicion_vecina_hacia,tableroTrasladandoPieza(t)->t,esTableroDespuesDeActivarTodasLasTrampas
def realizar_movimiento(j : Juego, m : Movimiento) -> Juego:
    """
    Dado un juego *j*, y movimiento *m* devuelve un juego habiendo modificado el tablero segun movimiento, y cambiado de TURNO de ser necesario
    PRE: juegoBienFormado (j ) ∧ movimientoBienFormado (m) ∧ puedeRealizarMovimiento (j , m)
    Args:
        j (Juego): estado actual del juego
        m (Movimiento): El movimiento que sera efectuado en el turno
     Returns:
        Devuelve un Juego habiendo modificado el tablero segun indica movimiento y cambiando de turno. 
    """
    t:Tablero=copiar_tablero(j.tablero)
    t=tableroPostMovimiento(t,m)
    cambio_de_turno:Color=j.turno
    pasos_proximo:int=j.pasos_consumidos + len(m.pasos)
    if(hayQueCambiarDeTurno(j,m)):
        cambio_de_turno=oponente(j.turno)
        pasos_proximo=0
    return (Juego(t,cambio_de_turno,pasos_proximo))#asi vi que se definia un nuevo juego, nose si esta habilitado
    


        



#### Ejercicio 7
#AUXILIAR
def es_inicio_de_turno(j: Juego, col: Color) -> bool:
    """
    Indica si es el inicio del turno para el jugador del color especificado 

    PRE: True

    Args:
        j (Juego): juego a evaluar.
        col (Color): El color del jugador.

    Returns:
        True si es el turno de col y j.pasos_consumidos == 0, False en caso contrario.
    """
    return j.turno == col and j.pasos_consumidos == 0 
#AUXILIAR
def hay_figura_de_color(t: Tablero, pos: Posicion, f: Figura, col: Color) -> bool:
    """Indica si en la casilla especificada del tablero existe una pieza con esa figura y color.

    PRE: True

    Args:
        t (Tablero): Matriz de casillas.
        pos (Posicion): (fila, columna) a consultar.
        f (Figura): Tipo de figura a buscar.
        col (Color): Color del jugador.

    Returns:
        True si la casilla contiene la pieza dada, False en caso contrario.
    """
    res: bool = False
    c: Casilla = t[pos.fila][pos.columna]
    if c != VACIA:
        res = c.figura == f and c.color == col
    return res
#AUXILIAR
def hay_conejo_en_tablero(j: Juego, col: Color) -> bool:
    """Verifica si el jugador col conserva al menos un conejo sobre el tablero.

    PRE: True
    Args:
        j (Juego): juego a evaluar.
        col (Color): Color del jugador consultado.

    Returns:
        True si existe al menos una casilla ocupada por un CONEJO del color col, False si no hay conejo de color col.
    """
    res: bool = False
    for fila in range(ALTO):
        for columna in range(ANCHO):
            pos = Posicion(fila, columna)
            if hay_figura_de_color(j.tablero, pos, CONEJO, col):
                res = True
    return res
  

#AUXILIAR
def hay_conejo_en_fila_inicial_oponente(j: Juego, col: Color) -> bool:
    """Verifica si un conejo del jugador col ha alcanzado la fila inicial de su oponente.

    PRE: True

    Args:
        j (Juego): juego a evaluar.
        col (Color): Color del jugador evaluado.

    Returns:
        True si hay un conejo propio en la fila inicial rival.
    """
    res: bool = False
    col_oponente: Color = oponente(col)
    fila_oponente: int = 0 if col_oponente == DORADO else 7
    for columna in range(ANCHO):
        pos = Posicion(fila_oponente,columna)
        if hay_figura_de_color(j.tablero, pos, CONEJO, col):
            res = True
    return res


#AUXILIAR
def reune_condiciones_de_ganar (j : Juego , col : Color ) -> bool:
    """Evalúa si el jugador col cumple alguna de las dos condiciones para ganar.

    PRE: True

    Args:
        j (Juego): juego a evaluar.
        col (Color): Color del jugador evaluado.

    Returns:
        True si tiene un conejo en la meta rival o si el rival perdió sus conejos.
    """
    return hay_conejo_en_fila_inicial_oponente(j,col) or not hay_conejo_en_tablero(j,oponente(col))


#aux
def reune_condiciones_de_ganar_exclusivas(j : Juego , col : Color) -> bool:
    """Evalúa si col cumple las condiciones de ganar y su oponente no.

    PRE: True

    Args:
        j (Juego): juego a evaluar.
        col (Color): Color del jugador evaluado.

    Returns:
        True si solo col cumple condiciones de ganar.
    """
    return reune_condiciones_de_ganar(j,col) and not reune_condiciones_de_ganar(j,oponente(col))



#aux
def es_jugador_ganador (j : Juego , col : Color ) -> bool:
    """Indica si el jugador de color col es el ganador del juego.

    PRE: True

    Args:
        j (Juego): juego a evaluar.
        col (Color): El color del jugador a evaluar.

    Returns:
        True si col cumple con las condiciones para ganar el juego,False en caso contrario.
    """
    return (es_inicio_de_turno(j,oponente(col)) and reune_condiciones_de_ganar(j,col)) or (es_inicio_de_turno(j,col) and reune_condiciones_de_ganar_exclusivas(j,col))

#EJERCICIO 7
def hay_ganador_determinado(j : Juego) -> bool:
    """Indica si existe al menos un jugador cumple para ser el ganador del juego.

    PRE: True

    Args:
        j (Juego): juego a evaluar.

    Returns:
        True si alguno de los dos jugadores cumple para ganar la partida, False en caso contrario.
    """
    return es_jugador_ganador(j,DORADO) or es_jugador_ganador(j,PLATEADO)


def ganador_del_juego(j : Juego) -> Color:
    """Devuelve el color del jugador que gano la partida.

    PRE: TRUE

    Args:
        j (Juego): juego a evaluar.

    Returns:
        DORADO si el ganador es el jugador Dorado, PLATEADO en caso contrario.
    """
    res: Color = PLATEADO
    if es_jugador_ganador(j,DORADO):
        res = DORADO    
    return res    

