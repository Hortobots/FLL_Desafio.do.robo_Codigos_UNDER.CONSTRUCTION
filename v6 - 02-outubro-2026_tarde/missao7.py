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


# --- FUNÇÃO DE MOVIMENTO COM ACELERAÇÃO PERSONALIZADA POR BLOCO ---

def andar_pid(distancia_mm, velocidade_max=1000, aceleracao=5.0):
    """
    Andar com perfil trapezoidal e taxa de aceleração personalizada para cada bloco.
    - aceleracao: quanto maior o número, mais rápido o robô atinge a velocidade máxima.
    """
    hub.imu.reset_heading(0)
    
    K_p = 3.0
    K_d = 1.0
    erro_anterior = 0

    left_motor.reset_angle(0)
    right_motor.reset_angle(0)

    circunferencia = 3.14159 * 58.1
    graus_alvo = (abs(distancia_mm) / circunferencia) * 360
    distancia_total = abs(distancia_mm)
    fator_direcao = 1 if distancia_mm > 0 else -1

    velocidade_atual = 50  # Torque inicial para não patinar

    while abs(left_motor.angle()) < graus_alvo:
        graus_atuais = abs(left_motor.angle())
        dist_percorrida = (graus_atuais / 360) * circunferencia
        dist_restante = distancia_total - dist_percorrida

        # Define a velocidade alvo baseada na distância (Rampa Trapezoidal)
        if dist_percorrida < 60:  # Aceleração nos primeiros 6 cm
            vel_alvo_limite = (dist_percorrida / 60) * abs(velocidade_max)
            vel_alvo_limite = max(50, vel_alvo_limite)
        elif dist_restante < 60:  # Desaceleração nos últimos 6 cm
            vel_alvo_limite = (dist_restante / 60) * abs(velocidade_max)
            vel_alvo_limite = max(50, vel_alvo_limite)
        else:
            vel_alvo_limite = abs(velocidade_max)

        # Usa a taxa de aceleração definida especificamente neste bloco
        if velocidade_atual < vel_alvo_limite:
            velocidade_atual += aceleracao
            if velocidade_atual > vel_alvo_limite:
                velocidade_atual = vel_alvo_limite
        elif velocidade_atual > vel_alvo_limite:
            velocidade_atual -= aceleracao
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


# --- FUNÇÃO DA ROTINA DA GARRA, PAUSA E RÉ ---

def garras_com_re(velocidade_garra, angulo_giro, tempo_pausa_ms):
    """
    1. Zera a contagem das garras.
    2. Abaixa a garra PRIMEIRO.
    3. Aguarda o tempo de pausa.
    4. Dá a primeira ré com aceleração própria.
    5. Retorna as garras para a posição inicial (0 - levanta).
    6. Pausa breve e dá a ré final com aceleração própria.
    """
    claw_motor_1.reset_angle(0)
    claw_motor_2.reset_angle(0)

    # 1. Garra abaixa PRIMEIRO
    claw_motor_1.run_target(velocidade_garra, angulo_giro, then=Stop.HOLD, wait=False)
    claw_motor_2.run_target(velocidade_garra, -angulo_giro, then=Stop.HOLD, wait=True)

    # 2. Pausa com a garra abaixada
    wait(tempo_pausa_ms)

    # 3. Primeira ré (-180 mm) com aceleração específica (ex: 6.0)
    andar_pid(-180, velocidade_max=1000, aceleracao=6.0)

    # 4. Retorna a garra para a posição inicial (0 - levanta)
    claw_motor_1.run_target(velocidade_garra, 0, then=Stop.HOLD, wait=False)
    claw_motor_2.run_target(velocidade_garra, 0, then=Stop.HOLD, wait=True)

    # Pausa de segurança para garantir que a garra subiu totalmente
    wait(200)

    # 5. RÉ FINAL (-450 mm) com aceleração específica para a fuga (ex: 8.0 para ser bem forte)
    andar_pid(-450, velocidade_max=1000, aceleracao=8.0)


# --- EXECUÇÃO DA MISSÃO ---

# 1. O robô anda para frente com uma aceleração própria (ex: 4.0)
andar_pid(780, velocidade_max=1000, aceleracao=3.0)

# Pausa de segurança após parar
wait(500)

# 2. Executa a rotina completa
garras_com_re(velocidade_garra=1000, angulo_giro=170, tempo_pausa_ms=1500)