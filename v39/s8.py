from base import * 

def run():
    # 1. Inicia a missão (Zera o giroscópio e ativa o temporizador)
    largada("PESADO")
    
    # 2. Anda para frente (847 mm convertidos para cm = 84.7 cm)
    andar(43, velocidade=700, aceleracao=500)
    wait(200)

    # 3. Move a garra para baixo
    mover_garra_b(-364, velocidade=300)
    wait(500)  # Espera meio segundo

    # 4. Anda para frente (847 mm convertidos para cm = 84.7 cm)
    andar(-20, velocidade=690, aceleracao=500)
    wait(200)

    # 5. Recolhe a garra subindo o mesmo tanto
    mover_garra_b(-200, velocidade=300)
    andar(17, velocidade=500, aceleracao=300)
    mover_garra_b(200, velocidade=300)
    andar(-17, velocidade=500, aceleracao=300)
    andar(-19, velocidade=500, aceleracao=300)
if __name__ == "__main__":
    run()
   