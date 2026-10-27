from unicodedata import name
import unittest
from arimaa import *

# Las piezas se representan con las siguientes letras:
#   E : elefante
#   M : camello
#   H : caballo
#   D : perro
#   C : gato
#   R : ratón
# donde
#   mayúscula : dorado
#   minúscula : plateado

def tablero_8x8_vacio():
    return leer_tablero([
              '--------', #7
              '--------', #6
              '--------', #5
              '--------', #4
              '--------', #3
              '--------', #2
              '--------', #1
              '--------', #0
              #01234567
            ])

def tablero_8x8_inicial_ejemplo():
    return leer_tablero([
              'hcdmedch', #7
              'rrrrrrrr', #6
              '--------', #5
              '--------', #4
              '--------', #3
              '--------', #2
              'RRRRRRRR', #1
              'HCDMEDCH', #0
              #01234567
            ])

#### Ejercicio 1

class test_tablero_bien_formado(unittest.TestCase):

    def test_8x8(self):
        """Prueba que un tablero válido de 8x8 devuelva True."""
        t: Tablero = tablero_8x8_inicial_ejemplo()
        self.assertTrue(tablero_bien_formado(t))

    def test_filas_insuficientes(self):
        """Prueba que un tablero con menos de 8 filas devuelva False."""
        t: Tablero = [["VACÍA"] * 8 for _ in range(7)]
        self.assertFalse(tablero_bien_formado(t))

    def test_mas_filas(self):
        """Prueba que un tablero con más de 8 filas devuelva False."""
        t: Tablero = [["VACÍA"] * 8 for _ in range(9)]
        self.assertFalse(tablero_bien_formado(t))

    def test_fila_corta(self):
        """Prueba un tablero con 8 filas pero con una fila de 3 columnas."""
        t: Tablero = [["VACÍA"] * 8 for _ in range(7)]
        t.append(["VACÍA", "VACÍA", "VACÍA"])
        self.assertFalse(tablero_bien_formado(t))

    def test_tablero_vacio(self):
        """Prueba el caso borde de una lista vacía."""
        self.assertFalse(tablero_bien_formado([]))    

class test_posicion_en_tablero(unittest.TestCase):

    def test_posicion_valida(self):
        """Prueba una posición válida en el centro del tablero."""
        self.assertTrue(posicion_en_tablero(Posicion(5, 3)))

    def test_posicion_limite_esquinas(self):
        """Prueba las esquinas válidas del tablero (0,0) y (7,7)."""
        self.assertTrue(posicion_en_tablero(Posicion(0, 0)))
        self.assertTrue(posicion_en_tablero(Posicion(7, 7)))

    def test_posicion_fila_fuera_rango(self):
        """Prueba posiciones con fila inválida (menor a 0 o mayor/igual a 8)."""
        self.assertFalse(posicion_en_tablero(Posicion(-1, 3)))
        self.assertFalse(posicion_en_tablero(Posicion(8, 3)))

    def test_posicion_columna_fuera_rango(self):
        """Prueba posiciones con columna inválida (menor a 0 o mayor/igual a 8)."""
        self.assertFalse(posicion_en_tablero(Posicion(3, -1)))
        self.assertFalse(posicion_en_tablero(Posicion(3, 8)))

class test_movimiento_bien_formado(unittest.TestCase):

    def test_movimiento_valido(self):
        """Prueba un movimiento totalmente válido (MOVER_A_SECAS con 1 paso)."""
        m: Movimiento = Movimiento(MOVER_A_SECAS, Posicion(0, 1), [NORTE])
        self.assertTrue(movimiento_bien_formado(m))

    def test_movimiento_arrastrar_valido(self):
        """Prueba un movimiento de ARRASTRAR válido con exactamente 2 pasos."""
        m: Movimiento = Movimiento(ARRASTRAR, Posicion(2, 2), [NORTE, ESTE])
        self.assertTrue(movimiento_bien_formado(m))

    def test_accion_invalida(self):
        """Prueba una acción que no pertenece a las acciones válidas."""
        m: Movimiento = Movimiento("VOLAR", Posicion(0, 1), [NORTE])
        self.assertFalse(movimiento_bien_formado(m))

    def test_origen_invalido(self):
        """Prueba un movimiento cuyo origen está fuera del tablero."""
        m: Movimiento = Movimiento(MOVER_A_SECAS, Posicion(-1, 0), [NORTE])
        self.assertFalse(movimiento_bien_formado(m))

    def test_cantidad_pasos_invalida_mover(self):
        """Prueba MOVER_A_SECAS con 2 pasos (debe ser exactamente 1 paso)."""
        m: Movimiento = Movimiento(MOVER_A_SECAS, Posicion(0, 1), [NORTE, SUR])
        self.assertFalse(movimiento_bien_formado(m))

    def test_cantidad_pasos_invalida_arrastrar(self):
        """Prueba ARRASTRAR con 1 solo paso (debe tener exactamente 2 pasos)."""
        m: Movimiento = Movimiento(ARRASTRAR, Posicion(2, 2), [NORTE])
        self.assertFalse(movimiento_bien_formado(m))

    def test_direccion_invalida(self):
        """Prueba una dirección que no existe en el juego."""
        m: Movimiento = Movimiento(MOVER_A_SECAS, Posicion(0, 1), ["ARRIBA"])
        self.assertFalse(movimiento_bien_formado(m))

class test_juego_bien_formado(unittest.TestCase):

    def test_juego_valido(self):
        """Prueba un juego válido en posición inicial con 0 pasos consumidos."""
        j: Juego = Juego(tablero_8x8_vacio(), DORADO, 0)
        self.assertTrue(juego_bien_formado(j))

    def test_juego_tablero_invalido(self):
        """Prueba un juego donde el tablero interno no está bien formado."""
        tablero_invalido = [["VACÍA"] * 8 for _ in range(5)]  # Solo 5 filas
        j: Juego = Juego(tablero_invalido, DORADO, 0)
        self.assertFalse(juego_bien_formado(j))

    def test_juego_pasos_consumidos_negativos(self):
        """Prueba un juego con pasos consumidos menores a 0."""
        j: Juego = Juego(tablero_8x8_vacio(), DORADO, -1)
        self.assertFalse(juego_bien_formado(j))

    def test_juego_pasos_consumidos_excesivos(self):
        """Prueba un juego con pasos consumidos iguales o mayores a MAX_PASOS (4)."""
        j: Juego = Juego(tablero_8x8_vacio(), DORADO, MAX_PASOS)
        self.assertFalse(juego_bien_formado(j))

#### Ejercicio 2

class test_posicion_vecina_hacia(unittest.TestCase):

    def test_vecina_al_norte(self):
        self.assertEqual(posicion_vecina_hacia(Posicion(0, 0), NORTE), Posicion(1, 0))

    def test_vecina_al_sur(self):
        self.assertEqual(posicion_vecina_hacia(Posicion(1, 0), SUR), Posicion(0, 0))

    def test_vecina_al_este(self):
        self.assertEqual(posicion_vecina_hacia(Posicion(1, 1), ESTE), Posicion(1, 2))

    def test_vecina_al_oeste(self):
        self.assertEqual(posicion_vecina_hacia(Posicion(1, 1), OESTE), Posicion(1, 0))

    def test_vecina_al_norte_borde(self):
        self.assertEqual(posicion_vecina_hacia(Posicion(7, 7), NORTE), Posicion(8, 7))

    def test_vecina_al_sur_borde(self):
        self.assertEqual(posicion_vecina_hacia(Posicion(0, 0), SUR), Posicion(-1, 0))

    def test_vecina_al_este_borde(self):
        self.assertEqual(posicion_vecina_hacia(Posicion(7, 7), ESTE), Posicion(7, 8))

    def test_vecina_al_oeste_borde(self):
        self.assertEqual(posicion_vecina_hacia(Posicion(0, 0), OESTE), Posicion(0, -1))


class test_son_posiciones_vecinas(unittest.TestCase):

    def test_vecinas_true(self):
        self.assertTrue(son_posiciones_vecinas(Posicion(0, 0), Posicion(1, 0)))

    def test_vecinas_falso(self):
        self.assertFalse(son_posiciones_vecinas(Posicion(0, 0), Posicion(7, 0)))

class test_casilla_en_posicion(unittest.TestCase):

    def test_casilla_en_posicion_tablero_inicial(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertEqual(casilla_en_posicion(t, Posicion(0, 0)), Pieza(CABALLO, DORADO))

    def test_casilla_en_posicion_tablero_en_juego(self):
        t = leer_tablero([
              '-r----rr', #7
              '-mrh----', #6
              '-r---r--', #5
              'd-EH---c', #4
              '-M--hD-d', #3
              '-R-e----', #2
              '---H-R-C', #1
              'R-R---RR', #0
              #01234567
            ])
        self.assertEqual(casilla_en_posicion(t, Posicion(0, 0)), Pieza(CONEJO, DORADO))

    def test_casilla_en_posicion_tablero_en_juego_VACIA(self):
        t = leer_tablero([
              '-r----rr', #7
              '-mrh----', #6
              '-r---r--', #5
              'd-EH---c', #4
              '-M--hD-d', #3
              '-R-e----', #2
              '---H-R-C', #1
              'R-R---RR', #0
              #01234567
            ])
        self.assertEqual(casilla_en_posicion(t, Posicion(1, 0)), VACIA)

class test_hay_casilla_vacia(unittest.TestCase):

    def test_casilla_vacia_tablero_inicial_TRUE(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertTrue(hay_casilla_vacia(t, Posicion(2, 1)))

    def test_casilla_vacia_tablero_inicial_FALSE(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertFalse(hay_casilla_vacia(t, Posicion(0, 0)))

    def test_casilla_vacia_tablero_en_juego_TRUE(self):
        t = leer_tablero([
              '-r----rr', #7
              '-mrh----', #6
              '-r---r--', #5
              'd-EH---c', #4
              '-M--hD-d', #3
              '-R-e----', #2
              '---H-R-C', #1
              'R-R---RR', #0
              #01234567
            ])
        self.assertTrue(hay_casilla_vacia(t, Posicion(1, 0)))

    def test_casilla_vacia_tablero_en_juego_FALSE(self):
        t = leer_tablero([
              '-r----rr', #7
              '-mrh----', #6
              '-r---r--', #5
              'd-EH---c', #4
              '-M--hD-d', #3
              '-R-e----', #2
              '---H-R-C', #1
              'R-R---RR', #0
              #01234567
            ])
        self.assertFalse(hay_casilla_vacia(t, Posicion(0, 0)))

class test_hay_pieza_de_color(unittest.TestCase):

    def test_hay_pieza_de_color_ok(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertTrue(hay_pieza_de_color(t, Posicion(1, 4), DORADO))

#### Ejercicio 3

class test_hay_casilla_vacia_hacia(unittest.TestCase):

    def test_hay_casilla_vacia_hacia(self):
        t = leer_tablero([
              '-r----rr', #7
              '-mrh----', #6
              '-r---r--', #5
              'd-EH---c', #4
              '-M--hD-d', #3
              '-R-e----', #2
              '---H-R-C', #1
              'R-R---RR', #0
              #01234567
            ])
        self.assertTrue(hay_casilla_vacia_hacia(t, Posicion(0, 0), NORTE))
    def test_no_hay_casilla_vacia_hacia(self):
            t = leer_tablero([
                  '-r----rr', #7
                  '-mrh----', #6
                  '-r---r--', #5
                  'd-EH---c', #4
                  '-M--hD-d', #3
                  '-R-e----', #2
                  'r--H-R-C', #1
                  'R-R---RR', #0
                  #01234567
                ])
            self.assertFalse(hay_casilla_vacia_hacia(t, Posicion(0, 0), NORTE))

class test_hay_pieza_amiga_vecina(unittest.TestCase):

    def test_hay_pieza_amiga_vecina(self):
        t = leer_tablero([
              'R-hRD-Rr', #7
              'M----d--', #6
              '-h-rrCR-', #5
              'R-rcE---', #4
              '--drRR--', #3
              '-HD-H--m', #2
              '--r-RCc-', #1
              're---r--', #0 
              #01234567
            ])
        self.assertTrue(hay_pieza_amiga_vecina(t, Posicion(4, 3)))
    def test_no_hay_pieza_amiga_vecina(self):
        t = leer_tablero([
              'R-hRD-Rr', #7
              'M----d--', #6
              '-h--rCR-', #5
              'R--c----', #4
              '--d-R---', #3
              '-HD-H--m', #2
              '--r-RCc-', #1
              're---r--', #0
              #01234567
            ])
        self.assertFalse(hay_pieza_amiga_vecina(t, Posicion(4, 3)))
class test_hay_pieza_enemiga_mas_debil_hacia(unittest.TestCase):

    def test_hay_pieza_enemiga_mas_debil_hacia(self):
        t = leer_tablero([
              '--Hdm---', #7
              'r--HhC--', #6
              'e---R-C-', #5
              'ME--d---', #4
              'h--RDcRr', #3
              'R-R-r--r', #2
              '-RRcrRD-', #1
              '--r---rr', #0
              #01234567
            ])
        self.assertTrue(hay_pieza_enemiga_mas_debil_hacia(t, Posicion(1, 3), OESTE))

    def test_no_hay_pieza_enemiga_mas_debil_hacia(self):
        t = leer_tablero([
              '--Hdm---', #7
              'r--HhC--', #6
              'e---R-C-', #5
              'ME--d---', #4
              'h--RDcRr', #3
              'R-R-r--r', #2
              '-R-crRD-', #1
              '--r---rr', #0
              #01234567
            ])
        self.assertFalse(hay_pieza_enemiga_mas_debil_hacia(t, Posicion(1, 3), OESTE))
class test_hay_pieza_enemiga_mas_fuerte_vecina(unittest.TestCase):

    def test_hay_pieza_enemiga_mas_fuerte_vecina(self):
        t = leer_tablero([
              'R-e--mRr', #7
              '------dE', #6
              'h--Rr-RR', #5
              'c--R-C--', #4
              '-rCHDrr-', #3
              '----rc--', #2
              'h-R-M-R-', #1
              'rr-D-dH-', #0
              #01234567
            ])
        self.assertTrue(hay_pieza_enemiga_mas_fuerte_vecina(t, Posicion(3, 1)))

class test_hay_pieza_congelada(unittest.TestCase):

    def test_hay_pieza_congelada(self):
        t = leer_tablero([
              '--d--H-D', #7
              '-hMc--r-', #6
              '--r--C-H', #5
              '--------', #4
              '-CeD----', #3
              '---R----', #2
              '--------', #1
              '--------', #0
              #01234567
            ])
        self.assertTrue(hay_pieza_congelada(t, Posicion(6, 1)))

#### Ejercicio 4
#hay que probar, que no haya pieza de color, que haya pieza congelada, que la direccion de movimiento no este habilitada, que los pasos esten todos consumidos y esto para cada accion
#que se pueda hacer todo para cada accion
class test_puede_realizar_movimiento(unittest.TestCase):

    def test_mover_a_secas_ok(self):
        t:Tablero = leer_tablero([
              '--eMr---', #7
              '--------', #6
              '-R----r-', #5
              '--------', #4
              '--mMd---', #3
              '---D----', #2
              '--------', #1
              '-mD--mDR', #0
              #01234567
            ])
        j:Juego = Juego(t, PLATEADO, 0)
        m:Movimiento = Movimiento(MOVER_A_SECAS, Posicion(0, 1), [NORTE])
        self.assertTrue(puede_realizar_movimiento(j, m))
    def test_empujar_ok(self):
        t:Tablero = leer_tablero([
              '--eMr---', #7
              '--------', #6
              '-R----r-', #5
              '--------', #4
              '--mMd---', #3
              '---D----', #2
              '--------', #1
              '-mD--mDR', #0
              #01234567
        ])
        j:Juego = Juego(t, PLATEADO, 0)
        m:Movimiento = Movimiento(EMPUJAR, Posicion(0, 1), [ESTE,NORTE])
        self.assertTrue(puede_realizar_movimiento(j, m))

    def test_arrastrar_ok(self):
        t:Tablero = leer_tablero([
              '--eMr---', #7
              '--------', #6
              '-R----r-', #5
              '--------', #4
              '--mMd---', #3
              '---D----', #2
              '--------', #1
              '-mD--mDR', #0
              #01234567
        ])
        j:Juego = Juego(t, PLATEADO, 0)
        m:Movimiento = Movimiento(ARRASTRAR, Posicion(0, 1), [NORTE,OESTE])
        self.assertTrue(puede_realizar_movimiento(j, m))
    def test_no_hay_pieza_de_color_arrastrar(self):
        t:Tablero = leer_tablero([
              '--eMr---', #7
              '--------', #6
              '-R----r-', #5
              '--------', #4
              '--mMd---', #3
              '---D----', #2
              '--------', #1
              '-mD--mDR', #0
              #01234567
        ])
        j:Juego = Juego(t, PLATEADO, 0)
        m:Movimiento = Movimiento(ARRASTRAR, Posicion(0, 0), [NORTE,ESTE])
        self.assertFalse(puede_realizar_movimiento(j, m))

    def test_no_hay_pieza_de_color_mover_a_secas(self):
        t:Tablero = leer_tablero([
              '--eMr---', #7
              '--------', #6
              '-R----r-', #5
              '--------', #4
              '--mMd---', #3
              '---D----', #2
              '--------', #1
              '-mD--mDR', #0
              #01234567
        ])
        j:Juego = Juego(t, PLATEADO, 0)
        m:Movimiento = Movimiento(MOVER_A_SECAS, Posicion(0, 0), [NORTE])
        self.assertFalse(puede_realizar_movimiento(j, m))

    def test_no_hay_pieza_de_color_empujar(self):
        t:Tablero = leer_tablero([
              '--eMr---', #7
              '--------', #6
              '-R----r-', #5
              '--------', #4
              '--mMd---', #3
              '---D----', #2
              '--------', #1
              '-mD--mDR', #0
              #01234567
        ])
        j:Juego = Juego(t, PLATEADO, 0)
        m:Movimiento = Movimiento(EMPUJAR, Posicion(0, 0), [NORTE,ESTE])
        self.assertFalse(puede_realizar_movimiento(j, m))
    def test_mover_enemigo_arrastrar(self):
        t:Tablero = leer_tablero([
              '--eMr---', #7
              '--------', #6
              '-R----r-', #5
              '--------', #4
              '--mMd---', #3
              '---D----', #2
              '--------', #1
              '-mD--mDR', #0
              #01234567
        ])
        j:Juego = Juego(t, PLATEADO, 0)
        m:Movimiento = Movimiento(ARRASTRAR, Posicion(0, 2), [NORTE,ESTE])
        self.assertFalse(puede_realizar_movimiento(j, m))

    def test_mover_enemigo_mover_a_secas(self):
        t:Tablero = leer_tablero([
              '--eMr---', #7
              '--------', #6
              '-R----r-', #5
              '--------', #4
              '--mMd---', #3
              '---D----', #2
              '--------', #1
              '-mD--mDR', #0
              #01234567
        ])
        j:Juego = Juego(t, PLATEADO, 0)
        m:Movimiento = Movimiento(MOVER_A_SECAS, Posicion(0, 6), [NORTE])
        self.assertFalse(puede_realizar_movimiento(j, m))

    def test_mover_enemigo_empujar(self):
        t:Tablero = leer_tablero([
              '--eMr---', #7
              '--------', #6
              '-R----r-', #5
              '--------', #4
              '--mMd---', #3
              '---D----', #2
              '--------', #1
              '-mD--mDR', #0
              #01234567
        ])
        j:Juego = Juego(t, PLATEADO, 0)
        m:Movimiento = Movimiento(EMPUJAR, Posicion(3, 3), [NORTE,ESTE])
        self.assertFalse(puede_realizar_movimiento(j, m))

    def test_mover_pieza_congelada_mover_a_secas(self):
        t:Tablero = leer_tablero([
                    '--eMr---', #7
                    '--------', #6
                    '-R----r-', #5
                    '--------', #4
                    '--mMd---', #3
                    '---D----', #2
                    '--------', #1
                    '-mD--mDR', #0
                    #01234567
                ])
        j:Juego = Juego(t, PLATEADO, 0)
        m:Movimiento = Movimiento(MOVER_A_SECAS, Posicion(7, 4), [SUR])
        self.assertFalse(puede_realizar_movimiento(j,m))

    def test_direccion_invalida_mover_a_secas(self):
        t:Tablero = leer_tablero([
                    '--eMr---', #7
                    '--------', #6
                    '-R----r-', #5
                    '--------', #4
                    '--mMd---', #3
                    '---D----', #2
                    '--------', #1
                    '-mD--mDR', #0
                    #01234567
                ])
        j:Juego = Juego(t, PLATEADO, 0)
        m:Movimiento = Movimiento(MOVER_A_SECAS, Posicion(5, 6), [NORTE])
        self.assertFalse(puede_realizar_movimiento(j,m))
    def test_direccion_invalida_mover_a_secas2(self):
        t:Tablero = leer_tablero([
                    '--eMr---', #7
                    '--------', #6
                    '-R----r-', #5
                    '--------', #4
                    '--mMd---', #3
                    '---D----', #2
                    '--------', #1
                    '-mD--mDR', #0
                    #01234567
                ])
        j:Juego = Juego(t, DORADO, 0)
        m:Movimiento = Movimiento(MOVER_A_SECAS, Posicion(5, 1), [SUR])
        self.assertFalse(puede_realizar_movimiento(j,m))

    
                         
    def test_mover_pieza_congelada_arrastrar(self):
        t:Tablero = leer_tablero([
            '--eDhM--', #7
            '--------', #6
            '-R----r-', #5
            '--------', #4
            '--mMd---', #3
            '---D----', #2
            '--------', #1
            '-mD--mDR', #0
            #01234567
                    ])
        j:Juego = Juego(t, PLATEADO, 0)
        m:Movimiento = Movimiento(ARRASTRAR, Posicion(7, 4), [SUR,ESTE])
        self.assertFalse(puede_realizar_movimiento(j,m))



    def test_pasos_consumidos_arrastrar(self):
        t:Tablero = leer_tablero([
            '--eMr---', #7
            '--------', #6
            '-R----r-', #5
            '--------', #4
            '--mMd---', #3
            '---D----', #2
            '--------', #1
            '-mD--mDR', #0
            #01234567
        ])
        j: Juego = Juego(t, PLATEADO, 3)
        m: Movimiento = Movimiento(ARRASTRAR, Posicion(7, 2), [SUR,OESTE])
        self.assertFalse(puede_realizar_movimiento(j, m))
        

    def test_mover_pieza_congelada_empujar(self):
        t:Tablero = leer_tablero([
            '--eMr---', #7
            '--------', #6
            '-R----r-', #5
            '--------', #4
            '--mMdR--', #3
            '---D----', #2
            '--------', #1
            '-mD--mDR', #0
            #01234567
                    ])
        j:Juego = Juego(t, PLATEADO, 0)
        m:Movimiento = Movimiento(EMPUJAR, Posicion(3, 4), [ESTE,NORTE])
        self.assertFalse(puede_realizar_movimiento(j,m))


    def test_pasos_consumidos_empujar(self):
        t:Tablero = leer_tablero([
            '--eMr---', #7
            '--------', #6
            '-R----r-', #5
            '--------', #4
            '--mMd---', #3
            '---D----', #2
            '--------', #1
            '-mD--mDR', #0
            #01234567
        ])
        j: Juego = Juego(t, PLATEADO, 3)
        m: Movimiento = Movimiento(EMPUJAR, Posicion(7, 2), [ESTE,SUR])
        self.assertFalse(puede_realizar_movimiento(j, m))

    def test_destino_ocupado_movera_a_secas(self):
        t:Tablero = leer_tablero([
                    '--eMr---', #7
                    '--------', #6
                    '-R----r-', #5
                    '--------', #4
                    '--mMd---', #3
                    '---D----', #2
                    '--------', #1
                    '-mD--mDR', #0
                    #01234567
                ])
        j:Juego = Juego(t, DORADO, 0)
        m:Movimiento = Movimiento(MOVER_A_SECAS, Posicion(3, 3), [SUR])
        self.assertFalse(puede_realizar_movimiento(j,m))

    def test_empujar_contra_borde(self):
        t:Tablero = leer_tablero([
            '--eMr---', #7
            '--------', #6
            '-R----r-', #5
            '--------', #4
            '--mMd---', #3
            '---D----', #2
            '--------', #1
            '-mD--mDc', #0
            #01234567
        ])
        j:Juego = Juego(t, PLATEADO, 0)
        m:Movimiento = Movimiento(EMPUJAR, Posicion(0, 1), [ESTE, SUR])
        self.assertFalse(puede_realizar_movimiento(j, m))

    def test_arrastrar_fuera_borde(self):
        t:Tablero = leer_tablero([
            '--cMr---', #7
            '--------', #6
            '-R----r-', #5
            '--------', #4
            '--mMd---', #3
            '---D----', #2
            '--------', #1
            '-mD--eDc', #0
            #01234567
        ])
        j: Juego = Juego(t, PLATEADO, 0)
        m: Movimiento = Movimiento(ARRASTRAR, Posicion(0, 1), [NORTE,NORTE])
        self.assertFalse(puede_realizar_movimiento(j, m))
    def test_igual_fuerza(self):
        t:Tablero = leer_tablero([
            '--cMr---', #7
            '--------', #6
            '-R----r-', #5
            '--------', #4
            '--mMm---', #3
            '---D----', #2
            '--------', #1
            '-mD--eDc', #0
            #01234567
        ])
        j: Juego = Juego(t, PLATEADO, 0)
        m1: Movimiento = Movimiento(ARRASTRAR, Posicion(3, 4), [NORTE,ESTE])
        m2: Movimiento = Movimiento(EMPUJAR, Posicion(3, 4), [OESTE,NORTE])
        self.assertFalse(puede_realizar_movimiento(j, m1))
        self.assertFalse(puede_realizar_movimiento(j, m2))





#### Ejercicio 5

class test_activar_trampas(unittest.TestCase):

    def test_activar_trampas_ok(self):
        t0 = leer_tablero([
               '-eRD--rd', #7
               '--------', #6
               'H-r--E--', #5
               '-H--r-Cr', #4
               'R-------', #3
               'R-H--m--', #2
               'R-------', #1
               'c-D---R-', #0
               #01234567
             ])
        t1 = leer_tablero([
               '-eRD--rd', #7
               '--------', #6
               'H-------', #5
               '-H--r-Cr', #4
               'R-------', #3
               'R-------', #2
               'R-------', #1
               'c-D---R-', #0
               #01234567
             ])
        t2 = activar_trampas(t0)
        self.assertNotEqual(t0, t1)
        self.assertEqual(t2, t1)

#### Ejercicio 6

class test_realizar_movimiento(unittest.TestCase):
 
    def test_mover_a_secas(self):
        t0:Tablero = leer_tablero([
               'rrrrrrrr', #7
               'ccddhh-e', #6
               '--------', #5
               '---m----', #4
               '--------', #3
               '--------', #2
               'EMHHDDCC', #1
               'RRRRRRRR', #0
               #01234567
             ])
        tN:Tablero = leer_tablero([
               'rrrrrrrr', #7
               'ccddhh-e', #6
               '---m----', #5
               '--------', #4
               '--------', #3
               '--------', #2
               'EMHHDDCC', #1
               'RRRRRRRR', #0
               #01234567
             ])
        j0:Juego = Juego(t0, PLATEADO, 0) 
        jN:Juego = Juego(tN, PLATEADO, 1) 
        mN:Movimiento = Movimiento(MOVER_A_SECAS, Posicion(4, 3), [NORTE])
        self.assertTrue(puede_realizar_movimiento(j0, mN))
        self.assertEqual(realizar_movimiento(j0, mN), jN)
    def test_empujar(self):
        t0:Tablero = leer_tablero([
               'rrrr-rrr', #7
               'ccddhh-e', #6
               '--------', #5
               '---mR---', #4
               '--------', #3
               '--------', #2
               'EMHHDDCC', #1
               'RRRR-RRR', #0
               #01234567
             ])
        tN:Tablero = leer_tablero([
               'rrrr-rrr', #7
               'ccddhh-e', #6
               '--------', #5
               '----m---', #4
               '----R---', #3
               '--------', #2
               'EMHHDDCC', #1
               'RRRR-RRR', #0
               #01234567
             ])
        j0:Juego = Juego(t0, PLATEADO, 0) 
        jN:Juego = Juego(tN, PLATEADO, 2) 
        mN:Movimiento = Movimiento(EMPUJAR, Posicion(4, 3), [ESTE,SUR])
        self.assertTrue(puede_realizar_movimiento(j0, mN))
        self.assertEqual(realizar_movimiento(j0, mN), jN)
    def test_arrastrar(self):
        t0:Tablero = leer_tablero([
               'rrrr-rrr', #7
               'ccddhh-e', #6
               '--------', #5
               '---mR---', #4
               '--------', #3
               '--------', #2
               'EMHHDDCC', #1
               'RRRR-RRR', #0
               #01234567
             ])
        tN:Tablero = leer_tablero([
               'rrrr-rrr', #7
               'ccddhh-e', #6
               '--------', #5
               '--mR----', #4
               '--------', #3
               '--------', #2
               'EMHHDDCC', #1
               'RRRR-RRR', #0
               #01234567
             ])
        j0:Juego = Juego(t0, PLATEADO, 0) 
        jN:Juego = Juego(tN, PLATEADO, 2) 
        mN:Movimiento = Movimiento(ARRASTRAR, Posicion(4, 3), [OESTE,OESTE])
        self.assertTrue(puede_realizar_movimiento(j0, mN))
        self.assertEqual(realizar_movimiento(j0, mN), jN)
    def test_cambio_de_turno_al_consumir_max_pasos(self):
        t0: Tablero = leer_tablero([
                'rrrrrrrr', #7
                'ccddhh-e', #6
                '--------', #5
                '---m----', #4
                '--------', #3
                '--------', #2
                'EMHHDDCC', #1
                'RRRRRRRR', #0
                #01234567
                ])
        tN: Tablero = leer_tablero([
                'rrrrrrrr', #7
                'ccddhh-e', #6
                '---m----', #5
                '--------', #4
                '--------', #3
                '--------', #2
                'EMHHDDCC', #1
                'RRRRRRRR', #0
                #01234567
                ])
        j0: Juego = Juego(t0, PLATEADO, 3) 
        jN: Juego = Juego(tN, DORADO, 0)
        m: Movimiento = Movimiento(MOVER_A_SECAS, Posicion(4, 3), [NORTE])
        self.assertTrue(puede_realizar_movimiento(j0, m))
        self.assertEqual(realizar_movimiento(j0, m), jN)
    def test_mover_y_hay_trampa(self):
        t0_trampa: Tablero = leer_tablero([
               'rrrr-rrr', #7
               'ccddhh-e', #6
               '--m-----', #5
               '--R-----', #4
               '--------', #3
               '--------', #2
               'EMHHDDCC', #1
               'RRRR-RRR', #0
               #01234567
             ])
        tN_trampa: Tablero = leer_tablero([
               'rrrr-rrr', #7
               'ccddhh-e', #6
               '---m----', #5
               '--------', #4
               '--------', #3
               '--------', #2
               'EMHHDDCC', #1
               'RRRR-RRR', #0
               #01234567
             ])
        j0:Juego = Juego(t0_trampa, PLATEADO, 2)
        jN:Juego = Juego(tN_trampa, DORADO, 0)
        m:Movimiento = Movimiento(ARRASTRAR, Posicion(5, 2), [ESTE, NORTE])
        self.assertTrue(puede_realizar_movimiento(j0, m))
        self.assertEqual(realizar_movimiento(j0, m), jN)


    def test_mover_y_hay_trampa_con_amigo(self):
        t0_trampa: Tablero = leer_tablero([
               'rrrr-rrr', #7
               'ccddhh-e', #6
               '-C------', #5
               '--R-----', #4
               '--m-----', #3
               '--------', #2
               'EMHHDDCC', #1
               'RRRR-RRR', #0
               #01234567
             ])
        tN_trampa: Tablero = leer_tablero([
               'rrrr-rrr', #7
               'ccddhh-e', #6
               '-CR-----', #5
               '--m-----', #4
               '--------', #3
               '--------', #2
               'EMHHDDCC', #1
               'RRRR-RRR', #0
               #01234567
             ])
        j0:Juego = Juego(t0_trampa, PLATEADO, 2)
        jN:Juego = Juego(tN_trampa, DORADO, 0)
        m:Movimiento = Movimiento(EMPUJAR, Posicion(3, 2), [NORTE, NORTE])
        self.assertTrue(puede_realizar_movimiento(j0, m))
        self.assertEqual(realizar_movimiento(j0, m), jN)


#### Ejercicio 7

# class test_ganador_del_juego(unittest.TestCase):

#     def test_promueve_conejo_dorado_turno_del_oponente(self):
#         t = leer_tablero([
#               'rr----Rr', #7
#               'c-----me', #6
#               '---Ed-R-', #5
#               '-M---R--', #4
#               '---R----', #3
#               '-rrrr---', #2
#               '-H---DCC', #1
#               'R-----RR', #0
#               #01234567
#             ])
#         j = Juego(t, PLATEADO, 0)
#         self.assertTrue(hay_ganador_determinado(j))
#         self.assertEqual(ganador_del_juego(j), DORADO)


if __name__ == '__main__':
    unittest.main()
