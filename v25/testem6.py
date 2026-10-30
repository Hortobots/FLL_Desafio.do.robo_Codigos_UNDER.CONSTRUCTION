from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Direction, Port, Stop
from pybricks.tools import wait

hub = PrimeHub()

# Motores das rodas traseiras (Ajuste as portas conforme o seu robô)
left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.F, Direction.CLOCKWISE)

def andar_reto_pid(distancia_mm, velocidade_max=750, aceleracao=4.0):
    """Faz o robô andar em linha reta usando o giroscópio (positivo = frente, negativo = ré)."""
    left_motor.reset_angle(0)
    right_motor.reset_angle(0)
    hub.imu.reset_heading(0)
    
    circunferencia_roda = 58.1 * 3.14159
    graus_alvo = (abs(distancia_mm) / circunferencia_roda) * 360
    
    Kp = 4.0  
    Ki = 0.0  
    Kd = 0.8  
    
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
        if velocidade_atual < 30:
            velocidade_atual = 30
            
        fator_direcao = 1 if distancia_mm > 0 else -1
        
        erro = hub.imu.heading()
        integral += erro
        derivativa = erro - erro_anterior
        erro_anterior = erro
        
        correcao = (Kp * erro) + (Ki * integral) + (Kd * derivativa)
        
        vel_esq = (velocidade_atual - correcao) * fator_direcao
        vel_dir = (velocidade_atual + correcao) * fator_direcao
        
        left_motor.run(vel_esq)
        right_motor.run(vel_dir)
        wait(10)

    # Trava os motores ao terminar o movimento
    left_motor.hold()
    right_motor.hold()


def girar_90_graus(angulo_alvo=90, velocidade=200):
    """Faz o robô girar no próprio eixo usando o giroscópio."""
    hub.imu.reset_heading(0)
    
    if angulo_alvo > 0:
        while hub.imu.heading() < angulo_alvo:
            left_motor.run(velocidade)
            right_motor.run(-velocidade)
            wait(10)
    else:
        while hub.imu.heading() > angulo_alvo:
            left_motor.run(-velocidade)
            right_motor.run(velocidade)
            wait(10)
            
    left_motor.hold()
    right_motor.hold()


def girar_direita(graus_giro=15, velocidade=200):
    """Gira o robô para a direita usando o giroscópio."""
    hub.imu.reset_heading(0)
    
    while hub.imu.heading() < graus_giro:
        left_motor.run(velocidade)
        right_motor.run(-velocidade)
        wait(10)
        
    left_motor.hold()
    right_motor.hold()


def girar_esquerda(graus_giro=15, velocidade=200):
    """Gira o robô para a esquerda usando o giroscópio."""
    hub.imu.reset_heading(0)
    
    while hub.imu.heading() > -graus_giro:
        left_motor.run(-velocidade)
        right_motor.run(velocidade)
        wait(10)
        
    left_motor.hold()
    right_motor.hold()

# ==========================================
# SEQUÊNCIA DE MOVIMENTOS:
# ==========================================

# 1. Anda reto para a frente (690 mm)
andar_reto_pid(distancia_mm=690, velocidade_max=750, aceleracao=4.0)
wait(500)

# 2. Vira para a direita no lugar (48 graus)
girar_90_graus(angulo_alvo=48, velocidade=200)
wait(500)

# 3. Anda reto após a virada (280 mm)
andar_reto_pid(distancia_mm=280, velocidade_max=500, aceleracao=4.0)
wait(500)

# 4. Vira para a direita (45 graus)
girar_direita(graus_giro=45, velocidade=200)
wait(500)

# 5. Anda reto (ex: 150 mm) e para
andar_reto_pid(distancia_mm=200, velocidade_max=500, aceleracao=4.0)
wait(200)

# 6. Anda reto novamente (ex: 100 mm)
andar_reto_pid(distancia_mm=120, velocidade_max=100, aceleracao=1.0)