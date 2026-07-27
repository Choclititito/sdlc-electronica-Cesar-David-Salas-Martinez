from fsm_demo import (  #Importamos las funciones del archivo proporcionado
    TrafficLightFSM,
    TrafficLightState,
)

"""Cada prueba tiene la parte de creacion de variable para poder crear un semaforo nuevo y no haya problemas entre los tests"""
"""El comando assert funciona para preguntarle al programa si la variable es igual a lo que nosotros ponemos"""


def test_estado_inicial():
    """Prueba 1: Verifica que el FSM inicie en RED y con 0 ciclos."""
    fsm = TrafficLightFSM() #Se crea una variable 
    
    # Comprobamos el estado a través de la propiedad segura (@property)
    assert fsm.state == TrafficLightState.RED
    # Comprobamos el contador interno
    assert fsm._cycle_count == 0

def test_transicion_red_a_green():
    """Prueba 2: Verifica que el primer cambio pase de RED a GREEN."""
    fsm = TrafficLightFSM() #Creamos la variable
    
    nuevo_estado = fsm.transition() #Hacemos la transicion
    
    assert nuevo_estado == TrafficLightState.GREEN #Comprobamos que si se haya cumplido el cambio
    assert fsm.state == TrafficLightState.GREEN #Comprobamos que el estado si haya cambiado

def test_ciclo_completo_vuelve_a_red():
    """Prueba 3: Verifica la secuencia RED -> GREEN -> YELLOW -> RED."""
    fsm = TrafficLightFSM() #Creamos la variable

    assert fsm.state == TrafficLightState.RED #Comprobamos estado inicial

    fsm.transition() # Transición 1: RED -> GREEN
    assert fsm.state == TrafficLightState.GREEN #Comprobamos

    fsm.transition() # Transición 2: GREEN -> YELLOW
    assert fsm.state == TrafficLightState.YELLOW #Comprobamos

    fsm.transition() # Transición 3: YELLOW -> RED
    assert fsm.state == TrafficLightState.RED #Comprobamos el cumplido del ciclo completo

def test_conteo_de_ciclos():
    """Prueba 4: Verifica que el contador sume correctamente tras cada transición."""
    fsm = TrafficLightFSM()
    
    # Estado inicial
    assert fsm._cycle_count == 0
    
    # Primera transición
    fsm.transition()
    assert fsm._cycle_count == 1
    
    # Segunda transicion
    fsm.transition()
    assert fsm._cycle_count == 2
    
    # Tercera transicion
    fsm.transition()
    assert fsm._cycle_count == 3