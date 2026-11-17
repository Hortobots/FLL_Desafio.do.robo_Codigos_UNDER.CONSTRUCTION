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


# --- FUNÇÃO DE MOVIMENTO RETO COM PID E RAMPA ---

def andar_pid(distancia_mm, velocidade_max=800):
    """
    Andar em linha reta com perfil trapezoidal real de velocidade 
    (aceleração progressiva no início e frenagem suave no fim) + IMU.
    """
    hub.imu.reset_heading(0)
    
    K_p = 3.0
    K_d = 1.0
    erro_anterior = 0

    left_motor.reset_angle(0)
    right_motor.reset_angle(0)

    circunferencia = 3.14159 * 58.1
    graus_alvo = (distancia_mm / circunferencia) * 360
    distancia_total = abs(distancia_mm)
    fator_direcao = 1 if distancia_mm > 0 else -1

    # Controle de velocidade atual para fazer a rampa progressiva
    velocidade_atual = 20  # Começa bem devagar
    aceleracao_taxa = 3.0  # O quanto a velocidade aumenta por ciclo

    while abs(left_motor.angle()) < abs(graus_alvo):
        graus_atuais = abs(left_motor.angle())
        dist_percorrida = (graus_atuais / 360) * circunferencia
        dist_restante = distancia_total - dist_percorrida

        # Define a velocidade alvo baseada na distância (Rampa Trapezoidal)
        if dist_percorrida < 80:  # Aceleração nos primeiros 8 cm
            vel_alvo_limite = (dist_percorrida / 80) * abs(velocidade_max)
            vel_alvo_limite = max(20, vel_alvo_limite)
        elif dist_restante < 80:  # Desaceleração nos últimos 8 cm
            vel_alvo_limite = (dist_restante / 80) * abs(velocidade_max)
            vel_alvo_limite = max(20, vel_alvo_limite)
        else:
            vel_alvo_limite = abs(velocidade_max)

        # Suaviza a transição da velocidade atual
        if velocidade_atual < vel_alvo_limite:
            velocidade_atual += aceleracao_taxa
            if velocidade_atual > vel_alvo_limite:
                velocidade_atual = vel_alvo_limite
        elif velocidade_atual > vel_alvo_limite:
            velocidade_atual -= aceleracao_taxa
            if velocidade_atual < vel_alvo_limite:
                velocidade_atual = vel_alvo_limite

        velocidade_base = velocidade_atual * fator_direcao

        # Correção do PID com IMU para manter perfeitamente reto
        erro = 0 - hub.imu.heading()
        derivativo = erro - erro_anterior
        erro_anterior = erro
        correcao = (K_p * erro) + (K_d * derivativo)

        vel_esq = velocidade_base + correcao
        vel_dir = velocidade_base - correcao

        left_motor.run(vel_esq)
        right_motor.run(vel_dir)
        wait(10)

    # Parada segura das rodas
    left_motor.hold()
    right_motor.hold()


# --- EXECUÇÃO DA MISSÃO ---

# 1. Zera a posição inicial das garras
claw_motor_1.reset_angle(0)
claw_motor_2.reset_angle(0)

# 2. O robô anda a primeira parte sozinho (ex: os primeiros 100 mm / 10 cm)
andar_pid(100, velocidade_max=800)

# 3. AGORA a garra começa a ir para frente (1260 graus) COM 'wait=False' 
# enquanto o robô continua andando o restante do caminho (400 mm)
claw_motor_1.run_target(600, 1260, then=Stop.HOLD, wait=False)
claw_motor_2.run_target(600, -1260, then=Stop.HOLD, wait=False)

# 4. O robô faz os 400 mm restantes (totalizando 500 mm) enquanto a garra abre junto
andar_pid(400, velocidade_max=800)

# 5. Pequena pausa para garantir que tudo estabilizou
wait(500)

# 6. O robô dá a ré longa e rápida (-180 mm)
andar_pid(-180, velocidade_max=700)

# 7. Por fim, recolhe a garra de volta para a posição inicial (0)
claw_motor_1.run_target(600, 0, then=Stop.HOLD, wait=False)
claw_motor_2.run_target(600, 0, then=Stop.HOLD, wait=True