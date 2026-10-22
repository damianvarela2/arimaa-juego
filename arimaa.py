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

def activar_trampas(t : Tablero) -> Tablero:
    raise Exception("No implementado")

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

