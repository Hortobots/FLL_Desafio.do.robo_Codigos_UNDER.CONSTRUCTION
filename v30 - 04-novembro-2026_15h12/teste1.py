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


# --- 2. FUNÇÕES DE MOVIMENTO COM ACELERAÇÃO E DESACELERAÇÃO REAIS ---

def andar_pid(distancia_mm, velocidade_max=200):
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
    aceleracao_taxa = 3.0  # O quanto a velocidade aumenta por ciclo (quanto menor, mais suave)

    while abs(left_motor.angle()) < abs(graus_alvo):
        graus_atuais = abs(left_motor.angle())
        dist_percorrida = (graus_atuais / 360) * circunferencia
        dist_restante = distancia_total - dist_percorrida

        # Define a velocidade alvo baseada na distância (Rampa Trapezoidal)
        # Se estiver perto do começo ou do fim, o alvo diminui forçadamente.
        if dist_percorrida < 80:  # Aceleração nos primeiros 8 cm
            vel_alvo_limite = (dist_percorrida / 80) * abs(velocidade_max)
            vel_alvo_limite = max(20, vel_alvo_limite) # Garante o mínimo para mover
        elif dist_restante < 80:  # Desaceleração nos últimos 8 cm
            vel_alvo_limite = (dist_restante / 80) * abs(velocidade_max)
            vel_alvo_limite = max(20, vel_alvo_limite)
        else:
            vel_alvo_limite = abs(velocidade_max)

        # Suaviza a transição da velocidade atual em direção ao alvo (Aceleração/Desaceleração gradual)
        if velocidade_atual < vel_alvo_limite:
            velocidade_atual += aceleracao_taxa
            if velocidade_atual > vel_alvo_limite:
                velocidade_atual = vel_alvo_limite
        elif velocidade_atual > vel_alvo_limite:
            velocidade_atual -= aceleracao_taxa
            if velocidade_atual < vel_alvo_limite:
                velocidade_atual = vel_alvo_limite

        velocidade_base = velocidade_atual * fator_direcao

        # Correção do PID com IMU para manter reto
        erro = 0 - hub.imu.heading()
        derivativo = erro - erro_anterior
        erro_anterior = erro
        correcao = (K_p * erro) + (K_d * derivativo)

        vel_esq = velocidade_base + correcao
        vel_dir = velocidade_base - correcao

        left_motor.run(vel_esq)
        right_motor.run(vel_dir)
        wait(10)

    # Parada segura
    left_motor.hold()
    right_motor.hold()


def girar_com_imu(angulo_desejado, velocidade_max=60):
    """
    Giro com rampa de aceleração e frenagem suave no IMU.
    """
    hub.imu.reset_heading(0)
    estavel = 0
    velocidade_atual = 15
    aceleracao_taxa = 1.5

    while True:
        angulo_atual = hub.imu.heading()
        erro = angulo_desejado - angulo_atual
        
        if abs(erro) < 1.0:
            estavel += 1
            if estavel > 10:
                break
        else:
            estavel = 0

        # O alvo de velocidade diminui conforme se aproxima do ângulo (desaceleração natural)
        vel_alvo = abs(erro) * 2.5
        if vel_alvo > velocidade_max:
            vel_alvo = velocidade_max
        
        # Velocidade mínima para vencer o atrito
        if vel_alvo < 15 and abs(erro) > 1.0:
            vel_alvo = 15

        # Suaviza a velocidade (Rampa)
        if velocidade_atual < vel_alvo:
            velocidade_atual += aceleracao_taxa
            if velocidade_atual > vel_alvo:
                velocidade_atual = vel_alvo
        elif velocidade_atual > vel_alvo:
            velocidade_atual -= aceleracao_taxa
            if velocidade_atual < vel_alvo:
                velocidade_atual = vel_alvo

        # Direção correta do giro
        fator_sinal = 1 if erro > 0 else -1
        vel_motor = velocidade_atual * fator_sinal

        left_motor.run(vel_motor)
        right_motor.run(-vel_motor)
        
        wait(10)

    left_motor.hold()
    right_motor.hold()


def virar_esquerda(angulo_graus, velocidade=60):
    girar_com_imu(-abs(angulo_graus), velocidade)


def virar_direita(angulo_graus, velocidade=60):
    girar_com_imu(abs(angulo_graus), velocidade)


def acionar_garras(velocidade, tempo_ms):
    claw_motor_1.run(velocidade)
    claw_motor_2.run(velocidade)
    wait(tempo_ms)
    claw_motor_1.stop()
    claw_motor_2.stop()


# --- 3. EXECUÇÃO DA MISSÃO ---

# 1. Andar para frente com aceleração progressiva e frenagem no fim
andar_pid(400, velocidade_max=800)

# 2. Acionar a garra
acionar_garras(300, 1000)

# 3. Girar 90 graus com aceleração e desaceleração suaves
virar_esquerda(90, velocidade=60)

# 4. Andar mais um pouco para frente
andar_pid(200, velocidade_max=800)