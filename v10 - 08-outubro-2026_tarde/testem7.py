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


# --- FUNÇÃO 1: ANDAR RETO COM PID CORRIGIDO ---

def andar_reto_pid(distancia_mm, velocidade_max=750, aceleracao=4.0):
    left_motor.reset_angle(0)
    right_motor.reset_angle(0)
    hub.imu.reset_heading(0)  # Zera a bússola/giroscópio ao iniciar
    
    circunferencia_roda = 58.1 * 3.14159  # mm por rotação
    graus_alvo = (distancia_mm / circunferencia_roda) * 360
    
    # Constantes do PID
    Kp = 3.0  
    Ki = 0.0  
    Kd = 0.5  
    
    erro_anterior = 0
    integral = 0
    
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
        
        # --- CÁLCULO DO PID ---
        erro = hub.imu.heading()  # Alvo é 0.
        integral += erro
        derivativa = erro - erro_anterior
        erro_anterior = erro
        
        correcao = (Kp * erro) + (Ki * integral) + (Kd * derivativa)
        
        # Sinais invertidos para garantir que o robô volte para o centro corretamente
        vel_esq = (velocidade_atual + correcao) * fator_direcao
        vel_dir = (velocidade_atual - correcao) * fator_direcao
        
        left_motor.run(vel_esq)
        right_motor.run(vel_dir)
        
        wait(10)

    left_motor.hold()
    right_motor.hold()


# --- FUNÇÃO 2: VIRAR 20 GRAUS À ESQUERDA ---

def virar_esquerda_20():
    hub.imu.reset_heading(0)
    velocidade_giro = 150
    
    left_motor.run(-velocidade_giro)
    right_motor.run(velocidade_giro)
    
    while hub.imu.heading() > -18:
        wait(5)
        
    left_motor.hold()
    right_motor.hold()


# --- FUNÇÃO 3: DAR RÉ (COM PID) ---

def dar_re_pid(distancia_mm, velocidade_max=500):
    left_motor.reset_angle(0)
    right_motor.reset_angle(0)
    hub.imu.reset_heading(0)
    
    circunferencia_roda = 58.1 * 3.14159
    graus_alvo = (distancia_mm / circunferencia_roda) * 360
    
    Kp = 3.0
    Kd = 0.5
    erro_anterior = 0
    
    while True:
        posicao_atual = abs(left_motor.angle() + right_motor.angle()) / 2
        
        if posicao_atual >= graus_alvo:
            break
            
        erro = hub.imu.heading()
        derivativa = erro - erro_anterior
        erro_anterior = erro
        
        correcao = (Kp * erro) + (Kd * derivativa)
        
        # Sinais ajustados para a ré
        vel_esq = (-velocidade_max + correcao)
        vel_dir = (-velocidade_max - correcao)
        
        left_motor.run(vel_esq)
        right_motor.run(vel_dir)
        
        wait(10)
        
    left_motor.hold()
    right_motor.hold()


# --- SEQUÊNCIA DE MOVIMENTOS ---

# 1. Anda reto por 800 mm usando o PID
andar_reto_pid(800, velocidade_max=750, aceleracao=4.0)

# Pausa breve de segurança
wait(500)

# 2. Vira 20 graus para a esquerda
virar_esquerda_20()

# Pausa final de 1 segundo antes da ré
wait(1000)

# 3. Dá ré por 300 mm e para
dar_re_pid(300, velocidade_max=500)