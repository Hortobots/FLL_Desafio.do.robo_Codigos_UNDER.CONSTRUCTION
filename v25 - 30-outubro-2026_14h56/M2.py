from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

# Motores das rodas traseiras (Portas B e F conforme o seu ajuste anterior)
left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.F, Direction.CLOCKWISE)

# Motores das garras (Conectados nas portas livres, ex: C e D)
# ATENÇÃO: Mude a porta se suas garras estiverem em outras letras
claw_motor_1 = Motor(Port.A)
claw_motor_2 = Motor(Port.E)

# Configuração da Base de Pilotagem com as suas medidas exatas
# axle_track = 105 mm | wheel_diameter = 58.1 mm
robot = DriveBase(left_motor, right_motor, wheel_diameter=58.1, axle_track=105)


# --- 2. FUNÇÕES DE MOVIMENTO SIMPLES E PRECISAS ---

def andar(distancia_mm, velocidade=200):
    """
    Faz o robô andar para frente (positivo) ou para trás (negativo)
    em linha reta por uma distância exata em milímetros.
    """
    robot.straight(distancia_mm, then=Stop.HOLD, wait=True)

def virar(angulo_graus, velocidade=150):
    """
    Faz o robô girar no próprio eixo.
    Positivo = para a direita | Negativo = para a esquerda.
    """
    robot.turn(angulo_graus, then=Stop.HOLD, wait=True)

def acionar_garras(velocidade, tempo_ms):
    """
    Move os motores das garras por um tempo determinado.
    """
    claw_motor_1.run(velocidade)
    claw_motor_2.run(velocidade)
    wait(tempo_ms)
    claw_motor_1.stop()
    claw_motor_2.stop()


# --- 3. EXECUÇÃO DA MISSÃO ---
# Exemplo de sequência lógica para o robô realizar na mesa de FLL:

# 1. Andar para frente 40 cm (400 mm)
andar(400)

# 2. Abrir/fechar a garra (gira o motor por 1 segundo a 300 de velocidade)
acionar_garras(300, 1000)

# 3. Girar 90 graus para a direita
virar(90)

# 4. Andar mais um pouco para frente
andar(200)