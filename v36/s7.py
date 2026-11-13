from base import * 

def run():
    # 1. Inicia a missão (Zera o giroscópio e ativa o temporizador)
    largada("PESADO")
    
    # 2. Anda para frente (847 mm convertidos para cm = 84.7 cm)
    andar(73, velocidade=700, aceleracao=500)
    wait(200)

    # 3. Vira 22 graus para a esquerda
    girar_relativo(-26, velocidade=300)
    wait(500)  

    # 4. Anda para frente (847 mm convertidos para cm = 84.7 cm)
    andar(10, velocidade=700, aceleracao=500)
    wait(200)

    #5. Recolhe a garra subindo o mesmo tanto
    andar(-5, velocidade=500, aceleracao=300)
    girar_relativo(-40, velocidade=300)
    girar_relativo(50,velocidade=300)
    andar(-5, velocidade=300, aceleracao=500)
    girar_relativo(16,velocidade=300)
    andar(-70, velocidade=300, aceleracao=500)

if __name__ == "__main__":
    run()
