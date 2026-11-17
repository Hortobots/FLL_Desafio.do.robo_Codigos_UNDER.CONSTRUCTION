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
    girar_relativo(80, velocidade=800)
#anda 30cm com a velocidade e aceleração normal, depois anda 10cm com aceleração e velocidade lenta
    andar(33, velocidade=600, aceleracao=400)
    andar(14, velocidade=100, aceleracao=200)
    andar(-17, velocidade=800, aceleracao=500)
    girar_relativo(14, velocidade=700)
    mover_garra_b(384, velocidade=1000)
    andar(19, velocidade=700, aceleracao=500)
    mover_garra_b(-390, velocidade=1000)
    andar(-9, velocidade=800, aceleracao=500)
    girar_relativo(90, velocidade=1000)
    andar(75, velocidade=1000, aceleracao=1000)
if __name__ == "__main__":
    run()
