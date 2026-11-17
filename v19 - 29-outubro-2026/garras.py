from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Direction, Port, Stop
from pybricks.tools import wait

hub = PrimeHub()

# Motores das garras (Portas A e E)
claw_motor_1 = Motor(Port.A)
claw_motor_2 = Motor(Port.E)

# --- FUNÇÃO DE MOVIMENTO DAS GARRAS EM SENTIDOS OPOSTOS COM RAMPA ---

def mover_garras_opostas(graus_alvo, velocidade_max=500):
    """
    Move os motores das garras em direções opostas (para abrir/fechar),
    com rampa de aceleração e frenagem suave, operando com mais força e alcance.
    """
    claw_motor_1.reset_angle(0)
    claw_motor_2.reset_angle(0)

    fator_direcao = 1 if graus_alvo > 0 else -1
    distancia_total = abs(graus_alvo)

    velocidade_atual = 20  # Começa devagar para evitar trancos
    aceleracao_taxa = 15.0 # Aceleração um pouco mais rápida para atingir a força total mais rápido

    while abs(claw_motor_1.angle()) < distancia_total:
        graus_atuais = abs(claw_motor_1.angle())
        graus_restantes = distancia_total - graus_atuais

        # Perfil trapezoidal ajustado para distâncias maiores (ex: 50 primeiros e últimos graus)
        if graus_atuais < 50:  
            vel_alvo_limite = (graus_atuais / 50) * abs(velocidade_max)
            vel_alvo_limite = max(20, vel_alvo_limite)
        elif graus_restantes < 50:  
            vel_alvo_limite = (graus_restantes / 50) * abs(velocidade_max)
            vel_alvo_limite = max(20, vel_alvo_limite)
        else:
            vel_alvo_limite = abs(velocidade_max)

        # Suaviza a transição da velocidade (Rampa)
        if velocidade_atual < vel_alvo_limite:
            velocidade_atual += aceleracao_taxa
            if velocidade_atual > vel_alvo_limite:
                velocidade_atual = vel_alvo_limite
        elif velocidade_atual > vel_alvo_limite:
            velocidade_atual -= aceleracao_taxa
            if velocidade_atual < vel_alvo_limite:
                velocidade_atual = vel_alvo_limite

        vel_motor = velocidade_atual * fator_direcao

        # MOTOR 1 gira para um lado e o MOTOR 2 gira para o lado oposto (-)
        claw_motor_1.run(vel_motor)
        claw_motor_2.run(-vel_motor)
        wait(10)

    # Parada segura mantendo a posição travada com força máxima de retenção
    claw_motor_1.hold()
    claw_motor_2.hold()


# --- EXECUÇÃO DA MISSÃO ---

# Gira por mais tempo/voltas (ex: 720 graus = 2 voltas completas) com mais velocidade e força
mover_garras_opostas(720, velocidade_max=600)