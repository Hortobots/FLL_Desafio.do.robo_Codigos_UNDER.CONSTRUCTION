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


# --- FUNÇÃO DA ROTINA DA GARRA, PAUSA E RÉ ---

def garras_com_re(velocidade_garra, angulo_giro, tempo_pausa_ms):
    """
    1. Zera a contagem das garras.
    2. Gira as garras para frente (posição final desejada).
    3. Aguarda o tempo de pausa.
    4. Dá uma ré com o robô (-180 mm a velocidade 700).
    5. Retorna as garras para a posição inicial (0).
    """
    claw_motor_1.reset_angle(0)
    claw_motor_2.reset_angle(0)

    # 1. Garra vai para frente (só após o robô ter parado)
    claw_motor_1.run_target(velocidade_garra, angulo_giro, then=Stop.HOLD, wait=False)
    claw_motor_2.run_target(velocidade_garra, -angulo_giro, then=Stop.HOLD, wait=True)

    # 2. Pausa na posição esticada
    wait(tempo_pausa_ms)

    # 3. Robô dá a ré (-180 mm) mantendo o PID e rampa
    andar_pid(-180, velocidade_max=700)

    # 4. Retorna a garra para a posição inicial (0)
    claw_motor_1.run_target(velocidade_garra, 0, then=Stop.HOLD, wait=False)
    claw_motor_2.run_target(velocidade_garra, 0, then=Stop.HOLD, wait=True)


# --- EXECUÇÃO DA MISSÃO ---

# 1. O robô anda 720 mm para frente (parando 60 mm antes do original 780)
andar_pid(735, velocidade_max=800)

# Pausa de segurança após parar
wait(500)

# 2. Executa a rotina da garra (desce até 1400 graus, pausa, dá ré e recolhe)
garras_com_re(velocidade_garra=600, angulo_giro=1400, tempo_pausa_ms=1500)