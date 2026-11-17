from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Direction, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# ==========================================
# 1. INICIALIZAÇÃO DO HARDWARE
# ==========================================
hub = PrimeHub()

# Motores de Tração (Portas B e F)
motor_esquerdo = Motor(Port.B, Direction.COUNTERCLOCKWISE)
motor_direito = Motor(Port.F, Direction.CLOCKWISE)

# Motor da Garra / Anexo (Porta A)
motor_garra = Motor(Port.A)

# ==========================================
# 2. CONFIGURAÇÃO DA DRIVEBASE & PID
# ==========================================
DIAMETRO_RODA = 58.1    # mm
DISTANCIA_EIXOS = 105   # mm

robo = DriveBase(motor_esquerdo, motor_direito, wheel_diameter=DIAMETRO_RODA, axle_track=DISTANCIA_EIXOS)

# Ajuste fino do PID interno
robo.distance_control.pid(6700, 90, 35)
robo.heading_control.pid(6700, 90, 35)

# Velocidades e acelerações padrão
robo.settings(straight_speed=400, straight_acceleration=500, turn_rate=300, turn_acceleration=300)

# ==========================================
# 3. FUNÇÕES DE APOIO (MOVIMENTO E GARRA)
# ==========================================
def andar_distancia(distancia_mm, velocidade=400, aceleracao=500, esperar_ms=0):
    """Move o robô em linha reta (positivo para frente, negativo para trás) com parâmetros ajustáveis."""
    vel_anterior, acel_anterior, _, _ = robo.settings()
    
    robo.settings(straight_speed=velocidade, straight_acceleration=aceleracao)
    robo.straight(distancia_mm)
    
    robo.settings(straight_speed=vel_anterior, straight_acceleration=acel_anterior)
    
    if esperar_ms > 0:
        wait(esperar_ms)

def virar_angulo(angulo_graus, velocidade_giro=300, esperar_ms=0):
    """Gira o robô para um ângulo específico (positivo = direita, negativo = esquerda)."""
    _, _, giro_anterior, _ = robo.settings()
    
    robo.settings(turn_rate=velocidade_giro)
    robo.turn(angulo_graus)
    
    robo.settings(turn_rate=giro_anterior)
    
    if esperar_ms > 0:
        wait(esperar_ms)

def mover_garra(velocidade=400, angulo_graus=360, esperar_ms=0):
    """Move o motor da garra por um ângulo específico."""
    motor_garra.run_angle(velocidade, angulo_graus)
    
    if esperar_ms > 0:
        wait(esperar_ms)

# ==========================================
# 4. ROTINA PRINCIPAL DA MISSÃO
# ==========================================
def main():
    # 1. Anda para frente (847 mm)
    andar_distancia(distancia_mm=847, velocidade=500, aceleracao=600, esperar_ms=200)
    
    # 2. Vira 20 graus para a direita
    virar_angulo(angulo_graus=20, velocidade_giro=300, esperar_ms=100)
    
    # 3. Abaixa a garra
    mover_garra(velocidade=500, angulo_graus=-380, esperar_ms=150)
    
    # 4. Levanta a garra (Corrigido o recuo e o sinal do ângulo)
    mover_garra(velocidade=500, angulo_graus=380, esperar_ms=150)
    
    # 5. Dá ré (-400 mm)
    andar_distancia(distancia_mm=-400, velocidade=500, aceleracao=600, esperar_ms=100)
    
    # 6. Gira para a esquerda para se alinhar (-30 graus)
    virar_angulo(angulo_graus=-30, velocidade_giro=300, esperar_ms=100)
    
    # 7. Anda reto por 230 mm após o alinhamento
    andar_distancia(distancia_mm=230, velocidade=500, aceleracao=600, esperar_ms=100)
    
    # 8. Vira 76 graus para a direita
    virar_angulo(angulo_graus=78, velocidade_giro=295, esperar_ms=100)
    
    # 9. Anda reto por 125 mm
    andar_distancia(distancia_mm=139, velocidade=462, aceleracao=600, esperar_ms=200)

if __name__ == "__main__":
    main()