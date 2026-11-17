from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Direction, Port
from pybricks.tools import wait

hub = PrimeHub()

motor_esquerdo = Motor(Port.A, Direction.COUNTERCLOCKWISE)
motor_direito = Motor(Port.B)

# Zera o ângulo do giroscópio e os graus dos motores ao iniciar
hub.imu.reset_heading(0)
motor_esquerdo.reset_angle(0)
motor_direito.reset_angle(0)

# Constantes do PID
K_p = 2.0  
K_i = 0.0  
K_d = 1.0  

alvo_angulo = 0  
erro_anterior = 0
integral = 0

# Parâmetros de movimento
velocidade_base = 300
graus_alvo = 1000  # Distância para ir para frente

# 1. Loop de movimento com PID (Indo para frente)
while True:
    graus_atuais = (abs(motor_esquerdo.angle()) + abs(motor_direito.angle())) / 2
    
    if graus_atuais >= graus_alvo:
        break

    angulo_atual = hub.imu.heading()
    
    erro = alvo_angulo - angulo_atual
    integral += erro
    derivativo = erro - erro_anterior
    correcao = (K_p * erro) + (K_i * integral) + (K_d * derivativo)
    
    vel_esq = velocidade_base + correcao
    vel_dir = velocidade_base - correcao
    
    motor_esquerdo.run(vel_esq)
    motor_direito.run(vel_dir)
    
    erro_anterior = erro
    wait(10)

# Para e freia após ir para frente
motor_esquerdo.brake()
motor_direito.brake()
wait(500)

# 2. Dá a mini ré
velocidade_re = -200
tempo_re = 500  # Duração da ré em milissegundos

motor_esquerdo.run(velocidade_re)
motor_direito.run(velocidade_re)
wait(tempo_re)

# Para e freia após a ré
motor_esquerdo.brake()
motor_direito.brake()
wait(500)

# 3. Vira 90 graus para a direita usando o giroscópio
angulo_desejado = 90
velocidade_giro = 150

while hub.imu.heading() < angulo_desejado:
    # Roda esquerda vai para frente e direita para trás (giro no próprio eixo)
    motor_esquerdo.run(velocidade_giro)
    motor_direito.run(-velocidade_giro)
    wait(10)

# Para e freia de vez após a virada
motor_esquerdo.brake()
motor_direito.brake()