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


# --- FUNÇÃO: ANDAR RETO COM PID ---

def andar_reto_pid(distancia_mm, velocidade_max=750, aceleracao=4.0):
    left_motor.reset_angle(0)
    right_motor.reset_angle(0)
    hub.imu.reset_heading(0)  # Zera o giroscópio ao iniciar o movimento
    
    circunferencia_roda = 58.1 * 3.14159  # mm por rotação
    graus_alvo = (abs(distancia_mm) / circunferencia_roda) * 360
    
    # Constantes do PID para manter o robô reto
    Kp = 3.5  
    Ki = 0.0  
    Kd = 0.5  
    
    erro_anterior = 0
    integral = 0
    
    while True:
        posicao_atual = (abs(left_motor.angle()) + abs(right_motor.angle())) / 2
        
        if posicao_atual >= graus_alvo:
            break
            
        distancia_percorrida = posicao_atual
        distancia_restante = graus_alvo - distancia_percorrida
        
        velocidade_atual = min(
            velocidade_max,
            aceleracao * distancia_percorrida,
            aceleracao * distancia_restante
        )
        
        if velocidade_atual < 50:
            velocidade_atual = 50
            
        fator_direcao = 1 if distancia_mm > 0 else -1
        
        # --- CÁLCULO DO PID ---
        erro = hub.imu.heading()  # Alvo é 0
        integral += erro
        derivativa = erro - erro_anterior
        erro_anterior = erro
        
        correcao = (Kp * erro) + (Ki * integral) + (Kd * derivativa)
        
        vel_esq = (velocidade_atual - correcao) * fator_direcao
        vel_dir = (velocidade_atual + correcao) * fator_direcao
        
        left_motor.run(vel_esq)
        right_motor.run(vel_dir)
        
        wait(10)

    left_motor.hold()
    right_motor.hold()


def virar(angulo_graus, velocidade=150):
    """
    Faz o robô girar no próprio eixo.
    Positivo = para a direita | Negativo = para a esquerda.
    """
    robot.turn(angulo_graus, then=Stop.HOLD, wait=True)


# --- SEQUÊNCIA DE MOVIMENTOS ---

# 1. Anda reto por 650 mm para frente
andar_reto_pid(635, velocidade_max=750, aceleracao=3.0)

# Pausa breve de segurança
wait(500)

# 2. Vira 35 graus para a esquerda
virar(-35, velocidade=400)

andar_reto_pid(80, velocidade_max=270, aceleracao=4.0)

wait(100)

virar(10, velocidade=500)

andar_reto_pid(-115, velocidade_max=500, aceleracao=4.0)

# Pausa final com motores travados
wait(1000)