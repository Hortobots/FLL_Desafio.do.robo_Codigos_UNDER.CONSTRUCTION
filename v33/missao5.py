from base import * 

def run():
    # 1. Inicia a missão (Zera o giroscópio e ativa o temporizador)
    largada("PESADO")
    
     # 2. Anda para frente (847 mm convertidos para cm = 84.7 cm)
    andar(95, velocidade=650, aceleracao=350)
    wait(200)

    # 3. Vira 22 graus para a direita
    girar_relativo(22, velocidade=300)
    wait(500)  # Espera meio segundo

    # 4. Move a garra para baixo
    mover_garra_a(400, velocidade=300)
    wait(500)  # Espera meio segundo

    
if __name__ == "__main__":
    run()

