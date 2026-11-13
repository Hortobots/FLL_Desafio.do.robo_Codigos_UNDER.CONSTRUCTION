from base import *
 
def run():
    # 1. Inicia a missão (Zera o giroscópio e ativa o temporizador)
    #largada("PESADO")
   
     # 2. Anda para frente (847 mm convertidos para cm = 84.7 cm)
    andar(90, velocidade=650, aceleracao=350)
    wait(200)
 
    # 3. Vira 22 graus para a direita
    girar_relativo(11, velocidade=300)
    wait(500)  # Espera meio segundo
 
    # 4. Move a garra para baixo
    mover_garra_a(-167, velocidade=300)
    wait(500)  # Espera meio segundo
 
    # 5. Recolhe a garra subindo o mesmo tanto
    andar(-3, velocidade=500, aceleracao=300)
    mover_garra_a(-4, velocidade=900)
    mover_garra_a(105, velocidade=900)
    mover_garra_a(-70, velocidade=900)
    mover_garra_a(-50, velocidade=900)
    andar(4, velocidade=500, aceleracao=300)
    andar(2, velocidade=500, aceleracao=300)
    mover_garra_a(900, velocidade=900)
   
if __name__ == "__main__":
    run()
 
 
 