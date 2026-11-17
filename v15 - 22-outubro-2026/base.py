from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# ==========================================
# 1. INICIALIZAÇÃO DO HARDWARE
# ==========================================
hub = PrimeHub()

# Motores de Tração (Portas B e F)
left_motor = Motor(Port.F, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.B, Direction.CLOCKWISE)

# Motores dos Anexos / Garras (Portas A e E)
claw_motor_1 = Motor(Port.A)
claw_motor_2 = Motor(Port.E)

# ==========================================
# 2. CONFIGURAÇÃO DA DRIVEBASE & PID
# ==========================================
DIAMETRO_RODA = 58.1   # mm
DISTANCIA_EIXOS = 105   # mm

robot = DriveBase(
    left_motor=left_motor,
    right_motor=right_motor,
    wheel_diameter=DIAMETRO_RODA,
    axle_track=DISTANCIA_EIXOS
)

# Ajuste Fino do PID Interno do Pybricks
robot.distance_control.pid(710, 50, 30)
robot.heading_control.pid(710, 40, 35)

# Configuração de Velocidades e Acelerações Padrão
VELOCIDADE_PADRAO = 400    # mm/s
ACELERACAO_PADRAO = 500    # mm/s²
VEL_GIRO_PADRAO = 400      # deg/s
ACEL_GIRO_PADRAO = 300     # deg/s²

robot.settings(
    straight_speed=VELOCIDADE_PADRAO,
    straight_acceleration=ACELERACAO_PADRAO,
    turn_rate=VEL_GIRO_PADRAO,
    turn_acceleration=ACEL_GIRO_PADRAO
)

# ==========================================
# 3. FUNÇÕES BASE DE MOVIMENTO COM IMU
# ==========================================

def ressetar_giroscopio(angulo=0):
    """Zera a orientação do giroscópio do hub."""
    hub.imu.reset_heading(angulo)

def andar(distancia_mm, velocidade=None, aceleracao=None, parada=Stop.HOLD):
    """Anda em linha reta usando o PID integrado do Pybricks."""
    vel_atual, acel_atual, turn_vel, turn_acel = robot.settings()
    
    v = velocidade if velocidade is not None else vel_atual
    a = aceleracao if aceleracao is not None else acel_atual
    
    robot.settings(straight_speed=v, straight_acceleration=a)
    robot.straight(distancia_mm, then=parada, wait=True)
    robot.settings(straight_speed=vel_atual, straight_acceleration=acel_atual)

def virar_imu(angulo_alvo, velocidade_giro=400):
    """
    Gira o robô para um ângulo absoluto ou relativo usando o IMU do Hub.
    Isso evita travamentos e garante que o giroscópio controle a curva.
    """
    # Define a velocidade de giro temporária
    vel_atual_giro = robot.settings()[2]
    robot.settings(turn_rate=velocidade_giro)
    
    # Executa o giro usando o heading control integrado do Pybricks baseada no IMU
    robot.turn(angulo_alvo)
    
    # Restaura a velocidade padrão de giro
    robot.settings(turn_rate=vel_atual_giro)