from base import *

def run():
    # Inicializa a largada com o perfil pretendido (ajusta se necessário, ex: "PADRAO")
    largada("PADRAO")
    
    # 1. Anda reto por 352 mm para frente (usa a função do base.py)
    andar(352, velocidade=750)
    wait(500)

    # 2. Garra atua (-500 graus) - ajusta o nome da garra conforme o teu base.py (ex: garra, motor_garra, etc.)
    if 'garra' in globals():
        garra.run_angle(300, -500)
    elif 'garra_a' in globals():
        garra_a.run_angle(300, -500)
    wait(500)

    # 3. Mini ré (55 mm)
    andar(-55, velocidade=500)
    wait(500)

    # 4. Garra volta (500 graus)
    if 'garra' in globals():
        garra.run_angle(300, 500)
    elif 'garra_a' in globals():
        garra_a.run_angle(300, 500)
    wait(500)

    # 5. Outra mini ré (30 mm)
    andar(-30, velocidade=500)
    wait(500)

    # 6. Giro leve para a direita (se tiveres a função de girar no base.py)
    if 'girar' in globals():
        girar(12, velocidade=200)
    wait(500)

    # 7. Mini ré (25 mm)
    andar(-25, velocidade=500)
    wait(500)

    # 8. Mini ré (25 mm)
    andar(-25, velocidade=500)
    wait(500)

    # 9. Ré maior de afastamento final (150 mm)
    andar(-150, velocidade=850)

if __name__ == "__main__":
    run()