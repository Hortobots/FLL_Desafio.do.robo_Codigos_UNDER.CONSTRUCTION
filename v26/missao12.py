from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Direction, Port, Stop
from pybricks.tools import wait

hub = PrimeHub()

# Configura o motor da porta A invertendo o sentido padrão dele
motor_a = Motor(Port.A, Direction.COUNTERCLOCKWISE)

def mover_motor_a(graus, velocidade=500):
    motor_a.run_angle(velocidade, graus, then=Stop.HOLD, wait=True)

mover_motor_a(400, velocidade=400)