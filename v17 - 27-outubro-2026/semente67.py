from base import *
from pybricks.tools import wait
 
def run():
    largada("LEVE")
#anda 40cm com sua velocidade e aceleração estabelecidas ao ponto onde o robô possa andar reto
    andar(45, velocidade=600, aceleracao=400)
#move garra da direita com graus e velocidade estabelecida
    mover_garra_a(140, velocidade=1000)
    mover_garra_a(-10, velocidade=1000)
#anda 25cm com sua velocidade e aceleração estabelecidas ao ponto one o robô possa andar reto 
    andar(30, velocidade=600, aceleracao=400)
#vira
    girar_relativo(82, velocidade=800)
#anda 30cm com a velocidade e aceleração normal, depois anda 10cm com aceleração e velocidade lenta
    andar(30, velocidade=600, aceleracao=400)
    andar(12, velocidade=100, aceleracao=200)
    andar(-15, velocidade=800, aceleracao=500)
    girar_relativo(20, velocidade=700)
    andar(22, velocidade=700, aceleracao=500)
    girar_relativo(70 , velocidade=500)
    girar_relativo(-10, velocidade=500)
    girar_relativo(10, velocidade=500)
if __name__ == "__main__":
    run()
