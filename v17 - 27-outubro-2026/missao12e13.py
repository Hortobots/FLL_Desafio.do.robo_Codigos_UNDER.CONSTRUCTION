from base import *

def run():
    # 1. Inicia a missão (Zera o giroscópio e ativa o temporizador)
    largada("PESADO")
    
    # 2. Anda para frente (847 mm convertidos para cm = 84.7 cm)
    andar(84.7, velocidade=700, aceleracao=500)
    wait(200)
    
    # 3. Vira 22 graus para a direita
    girar_relativo(25, velocidade=300)
    wait(500)  # Espera meio segundo

    # 4. Move a garra para baixo
    mover_garra_a(400, velocidade=300)
    wait(500)  # Espera meio segundo
    
    # 5. Recolhe a garra subindo o mesmo tanto
    mover_garra_a(-383, velocidade=300)
    girar_relativo(-10, velocidade=100)
    andar(-20, velocidade=500, aceleracao=300)
    girar_relativo(39, velocidade=100)
    andar(9, velocidade=300, aceleracao=100)
    girar_relativo(10, velocidade=300)
    mover_garra_b(475, velocidade=900)
    girar_relativo(-70, velocidade=500)
    andar(-70, velocidade=1000, aceleracao=500)

if __name__ == "__main__":
    run()