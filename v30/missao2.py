from base import * 

def run():
    # 1. Inicia a missão (Zera o giroscópio e ativa o temporizador)
    largada("PESADO")

    # 2. Anda para frente (847 mm convertidos para cm = 84.7 cm)
    andar(45), velocidade=700, aceleracao=500)
    wait(200)

if __name__ == "__main__":
    run()