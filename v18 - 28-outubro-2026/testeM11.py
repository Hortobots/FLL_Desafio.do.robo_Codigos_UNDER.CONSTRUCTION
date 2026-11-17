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


# --- FUNÇÃO 1: ANDAR RETO / RÉ COM PID CORRIGIDO ---

def andar_reto_pid(distancia_mm, velocidade_max=750, aceleracao=4.0):
    left_motor.reset_angle(0)
    right_motor.reset_angle(0)
    hub.imu.reset_heading(0)  # Zera o giroscópio ao iniciar o movimento
    
    circunferencia_roda = 58.1 * 3.14159  # mm por rotação
    graus_alvo = (abs(distancia_mm) / circunferencia_roda) * 360
    
    # Constantes do PID para manter o robô reto
    Kp = 3.0  
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
            
        # Se distancia_mm for negativa, o fator inverte a direção para trás (-1)
        fator_direcao = 1 if distancia_mm > 0 else -1
        
        # --- CÁLCULO DO PID ---
        erro = hub.imu.heading()  # Alvo é 0. Se desviar, o erro corrige.
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


# --- FUNÇÃO 2: VIRAR À ESQUERDA (FLEXÍVEL) ---

def virar_esquerda(angulo_alvo, velocidade_giro=150):
    """
    Gira para a esquerda (sentido anti-horário -> valores negativos no IMU).
    Basta passar o ângulo desejado (ex: 20 para um giro menor).
    """
    hub.imu.reset_heading(0)
    meta_negativa = -abs(angulo_alvo)
    
    left_motor.run(-velocidade_giro)
    right_motor.run(velocidade_giro)
    
    # Continua girando enquanto o heading for maior que a meta negativa
    while hub.imu.heading() > meta_negativa:
        wait(5)
        
    left_motor.hold()
    right_motor.hold()


# --- SEQUÊNCIA DE MOVIMENTOS ---

# 1. Anda reto por 800 mm para frente
andar_reto_pid(800, velocidade_max=750, aceleracao=4.0)

# Pausa breve de segurança
wait(500)

# 2. Vira para a esquerda (Ajustado para 20 graus para ficar menor)
virar_esquerda(20, velocidade_giro=150)

# Pausa breve de segurança
wait(500)

# 3. Dá ré por 200 mm devagar mantendo o PID ativo
andar_reto_pid(-120, velocidade_max=150, aceleracao=1.0)

# Pausa breve de segurança
wait(600)

# 4. Vira para a esquerda (90 graus / com compensação de inércia para 82)
virar_esquerda(85, velocidade_giro=150)

# Pausa breve de segurança
wait(500)

# 5. Anda um pouco para frente (150 mm) mantendo o PID reto
andar_reto_pid(150, velocidade_max=500, aceleracao=4.0)

# 6. Pausa final com motores travados
wait(1000)