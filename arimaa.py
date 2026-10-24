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
    """
    Dada una dirección *d*, devuelve una posición *Posicion* vecina en esa dirección
    PRE : True
    Args:
        pos (Posicion): Una tupla de enteros que indica coordenadas en el tablero
        d (Direccion): NORTE, SUR, ESTE, OESTE
    Returns:
        Posicion (Posicion): Una tupla de enteros al NORTE, SUR, ESTE, OESTE de pos dependiendo d
    """

    if d == NORTE:
        res = Posicion(pos.fila + 1, pos.columna)
    if d == SUR:
        res = Posicion(pos.fila -1, pos.columna)
    if d == ESTE:
        res = Posicion(pos.fila, pos.columna + 1)
    if d == OESTE:
        res = Posicion(pos.fila, pos.columna - 1)
    return res

def casilla_en_posicion(t : Tablero, p : Posicion) -> Casilla:
    """
    Dado un tablero *t* y una posición *p*, devuelve la Casilla (VACIA O FIGURA) ubicada en esa posicion *p* de tablero *t*
    PRE: tablero_bien_formado(t) == True and posicion_en_tablero(p) == True
    Args:
        t (Tablero): Una secuencia de secuencias de Casillas (VACIA O FIGURA)
        p (Posicion): Una tupla de enteros que indica coordenadas en el tablero
    Returns:
        Casilla (VACIA O FIGURA): Devuelve la casilla (VACIA O FIGURA) correspondiente a esa posicion *p* en el tablero *t*
    """
    res = t[p.fila][p.columna]
    return res

def hay_casilla_vacia(t : Tablero, pos : Posicion) -> bool:
    """
    Dado un tablero *t* y una posición *p*, devuelve la True si el valor de la Casilla (VACIA O FIGURA) en esa posicion *p* es VACIA
    PRE: tablero_bien_formado(t) == True and posicion_en_tablero(p) == True
    Args:
        t (Tablero): Una secuencia de secuencias de Casillas (VACIA O FIGURA)
        p (Posicion): Una tupla de enteros que indica coordenadas en el tablero
    Returns:
        True si Casilla (VACIA O FIGURA) es VACIA
    """
    res : bool = False
    casilla : Casilla = casilla_en_posicion(t, pos)
    if casilla == VACIA:
        res = True
    return res

def hay_pieza_de_color(t : Tablero, pos : Posicion, col : Color) -> bool:
    """
    Dado un tablero *t* y una posición *p*, y un color *col*, devuelve True si el color de la FIGURA en la CASILLA correspondiente a POSICION es igual a col. 
    PRE: tablero_bien_formado(t) == True and posicion_en_tablero(p) == True
    Args:
        t (Tablero): Una secuencia de secuencias de Casillas (VACIA O FIGURA)
        p (Posicion): Una tupla de enteros que indica coordenadas en el tablero
        col (Color): La posicion 1 en la tupla FIGURA. str que representa el color de las piezas (Plateado o Dorado)
    Returns:
        True si el color (Color) de la Pieza (Figura, Color) en la posicion *p* de tablero *t* es igual a al color ingresado *col*
    """
    res : bool = False
    casilla : Casilla = casilla_en_posicion(t, pos)
    if not hay_casilla_vacia(t, pos) and casilla.color == col:
        res = True
    return res

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
    if fuerza(casilla_en_posicion(t, posicion_vecina_hacia(pos, d))[0]) < fuerza(casilla_en_posicion(t, pos)[0]) and casilla_en_posicion(t, posicion_vecina_hacia(pos, d)).color == oponente(casilla_en_posicion(t, pos).color):
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
    if fuerza(casilla_en_posicion(t, posicion_vecina_hacia(pos, d))[0]) > fuerza(casilla_en_posicion(t, pos)[0]) and casilla_en_posicion(t, posicion_vecina_hacia(pos, d)).color == oponente(casilla_en_posicion(t, pos).color):        
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
#j es de in, y m tambien, se supone que el juego y el movimiento estan bien formados, se asegura que se puede realizar el movimiento, es decir,
# #haypieza de color (j.tablero,m.origen,j.turno), nohaypiezacongelada(j.tablero,m.origen),direcci ó nDeMovimientoHabilitada (j . tablero , m. origen , m. pasos [0])
# ∧ j . pasosConsumidos + |m. pasos | ≤ Max_pasos
# ∧ puedeRealizarAcci ó n (j . tablero , m)
#Movimiento = Acción × Posición × seq ⟨ Dirección ⟩
#Acción = Mover_a_secas | Arrastrar | Empujar
#Posición = Z × Z
# Dirección = Norte | Sur | Este | Oeste

#juego=Juego = Tablero × Color × Z
#Tablero = seq ⟨ seq ⟨ Casilla ⟩ ⟩
#Casilla = Vacía | Pieza
#Pieza = Figura × Color
#Figura = Elefante | Camello | Caballo | Perro | Gato | Conejo
#Color = Dorado | Plateado
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
    res:bool=False
    if (m.accion==MOVER_A_SECAS and puedeMoverASecas(t, m.origen , m.pasos[0])):
        res=True
    elif(m.accion==ARRASTRAR and puedeArrastrar(t, m.origen , m.pasos[0] , m.pasos[1])):
        res=True
    elif(m.accion==EMPUJAR and puedeEmpujar(t, m.origen , m.pasos[0] , m.pasos[1])):
        res=True
    return res


def puede_realizar_movimiento(j : Juego, m : Movimiento) -> bool:#es consigna
    """
    Indica si el movimiento se puede realizar o no
    PRE: juegoBienFormado (j ) ∧ movimientoBienFormado (m)
    Args:
    j (Juego): estado actual del juego
    m (Movimiento): Direccion a la que me desplazo
    Returns:
    True si es el movimiento es posiblo, False sino
    """
    res:bool=False
    if(hay_pieza_de_color(j.tablero,m.origen,j.turno) and (not (hay_pieza_congelada(j.tablero,m.origen))) and (direccionDeMovimientoHabilitada(j.tablero,m.origen,m.pasos[0])) and  (j.pasos_consumidos + len(m.pasos)<=MAX_PASOS) and (puedeRealizarAccion(j.tablero,m))):
        res=True
    return(res)
#para este punto supuse el correcto funcionamiento de hay_pieza_de_color,hay_pieza_congelada,casilla_en_posicion,posicion_vecina_hacia,hay_pieza_enemiga_mas_debil_hacia,hay_casilla_vacia_hacia

#### Ejercicio 5

def sacar_pieza_tablero(t: Tablero, postrampa: Posicion) -> Tablero: #Es funcion auxiliar
    """
        Dado un tablero *t* y una posición trampa *postrampa*, devuelve el tablero resultante de activar esa trampa: la casilla queda VACIA si no hay una pieza amiga vecina; si la hay, el tablero queda igual.
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
        fila = []
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
            Si existen figuras en postrampa, entonces devuelve un tablero con las casillas que corresponden a postrampa VACIAS. 
            Si no, devuelve el mismo tablero.
    """
    if hay_casilla_vacia(t, postrampa) or hay_pieza_amiga_vecina(t,postrampa):
        res = t
    else:
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

    res = tablero_despues_de_activar_todas_las_trampas(t)
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
    res:Tablero=[]
    if(m.accion==MOVER_A_SECAS):
        res=tableroPostMoverASecas(t,m)
    elif(m.accion==EMPUJAR):
        res=tableroPostEmpujar(t,m)
    elif(m.accion==ARRASTRAR):
        res=tableroPostArrastrar(t,m)
    return res

def tableroPostMoverASecas(t:Tablero,m:Movimiento)->Tablero:
    res:Tablero=[]
    pos:Posicion=m.origen
    pos_destino:Posicion=posicion_vecina_hacia(pos,m.pasos[0])
    res=tableroTrasladandoPieza(t,pos,pos_destino)
    res=activar_trampas(res)
    return res


def tableroPostEmpujar(t:Tablero,m:Movimiento)->Tablero:
    res:Tablero=copiar_tablero(t)
    pos_enemiga:Posicion = posicion_vecina_hacia(m.origen, m.pasos[0])
    pos_objetivo:Posicion = posicion_vecina_hacia(pos_enemiga, m.pasos[1])
    res=tableroTrasladandoPieza(res, pos_enemiga,pos_objetivo)
    res=tableroTrasladandoPieza(res, m.origen,pos_enemiga)
    res = activar_trampas(res)
    return res


def tableroPostArrastrar(t:Tablero,m:Movimiento)->Tablero:
    res:Tablero=copiar_tablero(t)
    pos_enemiga:Posicion=posicion_vecina_hacia(m.origen,opuesta(m.pasos[1]))
    pos_objetivo:Posicion=posicion_vecina_hacia(m.origen,m.pasos[0])
    res=tableroTrasladandoPieza(res, m.origen,pos_objetivo)
    res=tableroTrasladandoPieza(res,pos_enemiga ,m.origen)
    res = activar_trampas(res)
    return res

def hayQueCambiarDeTurno(j:Juego,m:Movimiento)->bool:
    return((j.pasos_consumidos + len(m.pasos))==MAX_PASOS)
#definir los 3 tableros posmovimientos, hay que tener cuidado de no modificar t ni m
# ahora bien, res debe ser un juegobienformado, y j

#Estoy asumiendo el correcto funcionamiento de:
#juego_bien_formado. posicion_vecina_hacia,tableroTrasladandoPieza(t)->t,esTableroDespuesDeActivarTodasLasTrampas
def realizar_movimiento(j : Juego, m : Movimiento) -> Juego:
    t:Tablero=copiar_tablero(j.tablero)
    t=tableroPostMovimiento(t,m)
    cambio_de_turno:Color=j.turno
    pasos_proximo:int=j.pasos_consumidos + len(m.pasos)
    if(hayQueCambiarDeTurno(j,m)):
        cambio_de_turno=oponente(j.turno)
        pasos_proximo=0
    return (Juego(t,cambio_de_turno,pasos_proximo))#asi vi que se definia un nuevo juego, nose si esta habilitado
    


        



#### Ejercicio 7

def hay_ganador_determinado(j : Juego) -> bool:
    raise Exception("No implementado")

def ganador_del_juego(j : Juego) -> Color:
    raise Exception("No implementado")

