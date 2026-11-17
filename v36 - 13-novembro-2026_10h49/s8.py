from base import * 

def run():
    # 1. Inicia a missão (Zera o giroscópio e ativa o temporizador)
    largada("PESADO")

    # 2. Anda para frente (847 mm convertidos para cm = 84.7 cm)
    andar(48, velocidade=700, aceleracao=500)
    wait(200)

    # 3. Move a garra para baixo
    mover_garra_a(75, velocidade=250)
    wait(500)

    # 4. Recolhe a garra subindo o mesmo tanto
    mover_garra_a(50, velocidade=700, esperar=False)
    andar(-3, velocidade=500, aceleracao=300)
    mover_garra_a(120, velocidade=250)
    andar(-45, velocidade=700, aceleracao=300)
   
if __name__ == "__main__":
    run()