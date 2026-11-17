from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Direction, Port, Stop
from pybricks.tools import wait

hub = PrimeHub()

# Motores das rodas traseiras (Tração traseira)
left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.F, Direction.CLOCKWISE)

# Motor da garra (conectado na Porta A)
claw_motor = Motor(Port.A)

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


# --- FUNÇÃO: MINIMINI GIRO PARA A DIREITA ---

def girar_minimini_direita(graus_giro=15, velocidade=200):
    """
    Gira o robô levemente para a direita usando o giroscópio.
    """
    hub.imu.reset_heading(0)
    
    while hub.imu.heading() < graus_giro:
        left_motor.run(velocidade)
        right_motor.run(-velocidade)
        wait(10)
        
    left_motor.hold()
    right_motor.hold()


# --- SEQUÊNCIA DE MOVIMENTOS ---

# 1. Anda reto por 350 mm para frente
andar_reto_pid(352, velocidade_max=750, aceleracao=4.0)

# Pausa breve
wait(500)

# 2. Faz a garra (Porta A) girar -500 graus
claw_motor.run_angle(300, -500)

# Pausa breve
wait(500)

# 3. Dá uma mini ré menor (50 mm)
andar_reto_pid(-55, velocidade_max=500, aceleracao=4.0)

# Pausa breve
wait(500)

# 4. Faz a garra voltar para onde estava (500 graus positivos)
claw_motor.run_angle(300, 500)

# Pausa breve
wait(500)

# 5. Dá outra mini ré menor (25 mm)
andar_reto_pid(-28, velocidade_max=500, aceleracao=4.0)

# Pausa breve
wait(500)

# 6. Dá uma minimini giradinha para a direita (15 graus)
girar_minimini_direita(graus_giro=12, velocidade=200)

# Pausa breve
wait(500)

# 7. Dá uma mini ré de 25 mm
andar_reto_pid(-25, velocidade_max=500, aceleracao=4.0)

# Pausa breve
wait(500)

# 8. Dá outra mini ré de 25 mm
andar_reto_pid(-25, velocidade_max=500, aceleracao=4.0)


# 9. Dá uma ré maior no final (150 mm) para se afastar
andar_reto_pid(-150, velocidade_max=850, aceleracao=4.0)