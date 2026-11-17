from base import *
from pybricks.tools import wait
 
def run():
    largada("LEVE")
#anda 40cm com sua velocidade e aceleração estabelecidas ao ponto onde o robô possa andar reto
    andar(46, velocidade=600, aceleracao=400)
#move garra da direita com graus e velocidade estabelecida
    mover_garra_a(140, velocidade=1000)
    mover_garra_a(-120, velocidade=1000)
#anda 25cm com sua velocidade e aceleração estabelecidas ao ponto one o robô possa andar reto 
    andar(28, velocidade=600, aceleracao=400)
#vira
    girar_relativo(85, velocidade=800)
#anda 30cm com a velocidade e aceleração normal, depois anda 10cm com aceleração e velocidade lenta
    andar(33, velocidade=600, aceleracao=400)
    andar(11, velocidade=80, aceleracao=200)
    andar(-17, velocidade=800, aceleracao=500)
    girar_relativo(20, velocidade=700)
    mover_garra_b(420, velocidade=1000)
    andar(21, velocidade=700, aceleracao=500)
    mover_garra_b(-360, velocidade=1000)
    andar(-9, velocidade=800, aceleracao=500)
    girar_relativo(90, velocidade=1000)
    andar(72, velocidade=1000, aceleracao=1000)
if __name__ == "__main__":
    run()
