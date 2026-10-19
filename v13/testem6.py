from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Direction, Port, Stop
from pybricks.tools import wait

hub = PrimeHub()

# Motores das rodas traseiras (Tração traseira)
left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.F, Direction.CLOCKWISE)

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


# --- FUNÇÃO: GIRAR COM O IMU ---

def girar_90(angulo=-90, velocidade=200):
    """
    Gira o robô usando o giroscópio do Hub.
    Positivo = gira para a direita | Negativo = gira para a esquerda.
    """
    hub.imu.reset_heading(0)
    
    fator = 1 if angulo > 0 else -1
    
    while abs(hub.imu.heading()) < abs(angulo):
        left_motor.run(velocidade * fator)
        right_motor.run(-velocidade * fator)
        wait(10)
        
    left_motor.hold()
    right_motor.hold()


# --- SEQUÊNCIA DE MOVIMENTOS ---

# 1. Anda reto por 660 mm para frente
andar_reto_pid(675, velocidade_max=750, aceleracao=4.0)

# Pausa breve
wait(500)

# 2. Gira 90 graus para a esquerda
girar_90(-90, velocidade=200)

# Pausa breve
wait(500)

# 3. Dá ré por 300 mm (basta colocar o valor em negativo na mesma função)
andar_reto_pid(-300, velocidade_max=500, aceleracao=4.0)

