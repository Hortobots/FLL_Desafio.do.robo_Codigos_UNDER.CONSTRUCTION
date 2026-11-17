from base import * 

def run():
    largada("PESADO")
    andar (58, velocidade=700, aceleracao=500)
    mover_garra_a(85, velocidade=600)
    andar (-21, velocidade=700, aceleracao=500)
   # mover_garra_a(-65, velocidade=600)
    girar_relativo(-8, velocidade=300)
    mover_garra_a(-200, velocidade=1000)
    # girar_relativo(-5, velocidade=300)
    andar (-40, velocidade=700, aceleracao=200)
    # mover_garra_a(-90, velocidade=1000, esperar=False)
    # andar (-40, velocidade=700, aceleracao=500)



    
    
if __name__ == "__main__":
    run()