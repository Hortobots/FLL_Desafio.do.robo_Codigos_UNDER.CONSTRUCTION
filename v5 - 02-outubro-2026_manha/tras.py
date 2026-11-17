from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# Inicializa o Hub do SPIKE Prime
hub = PrimeHub()

# Configura os motores nas portas corretas (exemplo: Porta A e Porta B)
# Se o motor precisar girar ao contrário para ir frente, você pode ajustar com 'positive_direction'
motor_esquerdo = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
motor_direito = Motor(Port.B, positive_direction=Direction.CLOCKWISE)

# Configura a base do robô (DriveBase)
# Substitua 56 pelo diâmetro da roda em mm e 114 pela distância entre as rodas
robo = DriveBase(motor_esquerdo, motor_direito, wheel_diameter=56, axle_track=114)

# --- OPÇÃO 1: Andar para trás por uma distância exata (ex: 300 mm / 30 cm) ---
robo.straight(-300)  # O valor negativo faz o robô recuar

# --- OPÇÃO 2: Andar para trás continuamente até mandar parar ---
# robo.drive(-200, 0)  # -200 mm/s de velocidade em linha reta
# wait(2000)           # Anda para trás por 2 segundos
# robo.stop()          # Para o robô