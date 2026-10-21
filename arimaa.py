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
        fila_copia:list[str]=[]
        for casilla in fila:
            fila_copia.append(casilla)
        res.append(fila_copia)
    return res

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
    res=False
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
    res=False
    if(hay_pieza_de_color(j.tablero,m.origen,j.turno) and (not (hay_pieza_congelada(j.tablero,m.origen))) and (direccionDeMovimientoHabilitada(j.tablero,m.origen,m.pasos[0])) and  (j.pasosConsumidos + len(m.pasos)<=MAX_PASOS) and (puedeRealizarAccion(j.tablero,m))):
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
    pos=m.origen
    pos_destino=posicion_vecina_hacia(pos,m.pasos[0])
    res=tableroTrasladandoPieza(t,pos,pos_destino)
    res=activar_trampas(res)
    return res

def tableroTrasladandoPieza(t:Tablero,origen:Posicion,destino:Posicion)->Tablero:


def tableroPostEmpujar(t:Tablero,m:Movimiento)->Tablero:

def tableroPostArrastrar(t:Tablero,m:Movimiento)->Tablero:


#definir los 3 tableros posmovimientos, hay que tener cuidado de no modificar t ni m
# ahora bien, res debe ser un juegobienformado, y j

#Estoy asumiendo el correcto funcionamiento de:
#juego_bien_formado. posicion_vecina_hacia,tableroTrasladandoPieza(t)->t,esTableroDespuesDeActivarTodasLasTrampas
def realizar_movimiento(j : Juego, m : Movimiento) -> Juego:
    raise Exception("No implementado")

#### Ejercicio 7

def hay_ganador_determinado(j : Juego) -> bool:
    raise Exception("No implementado")

def ganador_del_juego(j : Juego) -> Color:
    raise Exception("No implementado")

