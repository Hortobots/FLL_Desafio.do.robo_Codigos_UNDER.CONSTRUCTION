from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait

hub = PrimeHub()

# Motores das rodas traseiras (Tração traseira)
left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.F, Direction.CLOCKWISE)

# Motores das garras
claw_motor_1 = Motor(Port.A)
claw_motor_2 = Motor(Port.E)

# Configuração da Base de Pilotagem
robot = DriveBase(left_motor, right_motor, wheel_diameter=58.1, axle_track=105)


# --- FUNÇÃO 1: ANDAR RETO ---

def andar_reto(distancia_mm, velocidade_max=1000, aceleracao=5.0):
    left_motor.reset_angle(0)
    right_motor.reset_angle(0)
    
    circunferencia_roda = 58.1 * 3.14159  # mm por rotação
    graus_alvo = (distancia_mm / circunferencia_roda) * 360
    
    while True:
        posicao_atual = (left_motor.angle() + right_motor.angle()) / 2
        
        if abs(posicao_atual) >= abs(graus_alvo):
            break
            
        distancia_percorrida = abs(posicao_atual)
        distancia_restante = abs(graus_alvo) - distancia_percorrida
        
        velocidade_atual = min(
            velocidade_max,
            aceleracao * distancia_percorrida,
            aceleracao * distancia_restante
        )
        
        if velocidade_atual < 50:
            velocidade_atual = 50
            
        fator_direcao = 1 if distancia_mm > 0 else -1
        
        left_motor.run(velocidade_atual * fator_direcao)
        right_motor.run(velocidade_atual * fator_direcao)
        
        wait(10)

    left_motor.hold()
    right_motor.hold()


# --- FUNÇÃO 2: VIRAR À ESQUERDA COM AJUSTE DE INÉRCIA ---

def virar_esquerda_90():
    """
    Gira para a esquerda. O valor -85 compensa a inércia para parar exatamente em -90°.
    Se passar muito de 90°, ajuste para -82 ou -80. Se faltar, ajuste para -88.
    """
    hub.imu.reset_heading(0)
    
    velocidade_giro = 200
    
    # Motores invertidos para girar para a esquerda
    left_motor.run(-velocidade_giro)
    right_motor.run(velocidade_giro)
    
    # Para a esquerda, o heading fica negativo
    while hub.imu.heading() > -85:
        wait(5)
        
    left_motor.hold()
    right_motor.hold()


# --- SEQUÊNCIA DE MOVIMENTOS ---

# 1. Anda reto por 600 mm
andar_reto(600, velocidade_max=750, aceleracao=4.0)

# Pausa breve de segurança entre os comandos
wait(500)

# 2. Vira para a esquerda
virar_esquerda_90()

# 3. Garante que ele pare totalmente e espera 1 segundo
left_motor.hold()
right_motor.hold()
wait(1000)