from base import * 

def run():
    # 1. Inicia a missão (Zera o giroscópio e ativa o temporizador)
    largada("PESADO")
    
    # 2. Anda para frente (890 mm convertidos para cm = 89 cm)
    andar(89, velocidade=650, aceleracao=350)

    # 3. levanta a garra 
    mover_garra_a(-500, velocidade=1000, aceleracao=1000)

    # 4. anda pra trás 
    andar(-10.67, velocidade=500, aceleracao=600)

    # 5. abaixa a garra
    mover_garra_a(900, velocidade=1000, aceleracao=1000)

    # 6. anda pra frente 
    andar(7.467, velocidade=700, aceleracao=500)

    # 7. joga a garra pra cima e volta para base
    mover_garra_a(-1900, velocidade=1000, aceleracao=1000)
    andar(-100, velocidade=1000, aceleracao=1000)

if __name__ == "__main__":
    run()
   

