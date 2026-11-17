from base import * 

def run():
    # 1. Inicia a missão (Zera o giroscópio e ativa o temporizador)
    largada("PESADO")
    
    # 2. Anda para frente (847 mm convertidos para cm = 84.7 cm)
    andar(85, velocidade=700, aceleracao=500)
    wait(200)
    
    # 3. Vira 22 graus para a direita
    girar_relativo(85, velocidade=300)
    wait(500)  # Espera meio segundo

    # 4. Move a garra para baixo
    mover_garra_a(400, velocidade=300)
    wait(500)  # Espera meio segundo
    
    # 5. Recolhe a garra subindo o mesmo tanto
    mover_garra_a(-383, velocidade=300)
    girar_relativo(10, velocidade=300)
    andar(-28, velocidade=500, aceleracao=300)
    girar_relativo(17, velocidade=100)
    girar_relativo(9, velocidade=300)
    andar(17, velocidade=300, aceleracao=500)
    girar_relativo(11, velocidade=300)
    mover_garra_b(490, velocidade=900)
    wait
    mover_garra_b(-490, velocidade=900)
    andar(-10, velocidade=1000, aceleracao=500)
    girar_relativo(-78, velocidade=500)
    andar(-75, velocidade=1000, aceleracao=500)

if __name__ == "__main__":
    run()