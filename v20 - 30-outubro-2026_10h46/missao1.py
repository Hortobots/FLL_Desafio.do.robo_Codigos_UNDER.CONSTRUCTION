from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait

hub = PrimeHub()

# Motores das rodas traseiras (Tração traseira)
left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.F, Direction.CLOCKWISE)

# Motores das garras (mantidos caso precise no futuro)
claw_motor_1 = Motor(Port.A)
claw_motor_2 = Motor(Port.E)

# Configuração da Base de Pilotagem
robot = DriveBase(left_motor, right_motor, wheel_diameter=58.1, axle_track=105)


# --- FUNÇÃO DE MOVIMENTO RETO COM PID E RAMPA DE VELOCIDADE ---

def andar_pid(distancia_mm, velocidade_max=300):
    """
    Andar em linha reta com perfil trapezoidal real de velocidade 
    (aceleração progressiva no início e frenagem suave no fim) + IMU.
    Positivo = Vai para frente
    Negativo = Volta para trás
    """
    hub.imu.reset_heading(0)
    
    K_p = 5
    K_d = 1
    erro_anterior = 0

    left_motor.reset_angle(0)
    right_motor.reset_angle(0)

    circunferencia = 3.14159 * 58.1
    graus_alvo = (abs(distancia_mm) / circunferencia) * 360
    distancia_total = abs(distancia_mm)
    fator_direcao = 1 if distancia_mm > 0 else -1

    # Controle de velocidade atual para fazer a rampa progressiva
    velocidade_atual = 200  # Começa bem devagar
    aceleracao_taxa = 2.0  # Taxa menor para acelerar de forma suave

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

        # Correção do PID com IMU para manter o robô perfeitamente reto
        erro = 0 - hub.imu.heading()
        derivativo = erro - erro_anterior
        erro_anterior = erro
        correcao = (K_p * erro) + (K_d * derivativo)

        vel_esq = velocidade_base + correcao
        vel_dir = velocidade_base - correcao

        left_motor.run(vel_esq)
        right_motor.run(vel_dir)
        wait(10)

    # Parada segura no final da distância
    left_motor.hold()
    right_motor.hold()


# --- EXECUÇÃO DA MISSÃO ---

# 1. Vai um pouco mais para frente (Aumentado para 600 mm)
andar_pid(700, velocidade_max=800)

# Espera 1 segundo parado no destino
wait(1000)

# 2. Volta exatamente a mesma distância para o lugar de onde saiu (-600 mm)
andar_pid(-700, velocidade_max=300)