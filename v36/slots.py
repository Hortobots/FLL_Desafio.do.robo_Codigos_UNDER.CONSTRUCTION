from pybricks.tools import hub_menu, StopWatch
from pybricks.parameters import Color, Stop
from base import hub, bot

# Importa os módulos de missão com os nomes corretos (S1 a S6)
import s1, s2, s3, s4, s5, s6, s7, s8

# Sequência de strings exibida no menu do Hub (com o "0" no fim para sair)
SEQUENCIA = ["1", "2", "3", "4", "5", "6","7","8", "0"]

# Dicionário associando a tecla do menu à respetiva função
MISSOES = {
    "1": s1.run,
    "2": s2.run,
    "3": s3.run,
    "4": s4.run,
    "5": s5.run,
    "6": s6.run,
    "7": s7.run,
    "8": s8.run,
}

posicao = 0
cronometro = StopWatch()

# Função definitiva para matar o PID e soltar os motores a 100%
def soltar_motores():
    try:
        # Para a DriveBase e anula o comando de percurso
        if hasattr(bot, 'drive') and bot.drive:
            bot.drive.stop(Stop.COAST)
    except:
        pass
        
    try:
        # Força os motores individuais a 0% de potência em corrente contínua (mata o PID de posição)
        if hasattr(bot, 'motor_esq') and bot.motor_esq:
            bot.motor_esq.dc(0)
            bot.motor_esq.stop(Stop.COAST)
        if hasattr(bot, 'motor_dir') and bot.motor_dir:
            bot.motor_dir.dc(0)
            bot.motor_dir.stop(Stop.COAST)
    except:
        pass
        
    try:
        if hasattr(bot, 'garra_a') and bot.garra_a:
            bot.garra_a.dc(0)
            bot.garra_a.stop(Stop.COAST)
        if hasattr(bot, 'garra_b') and bot.garra_b:
            bot.garra_b.dc(0)
            bot.garra_b.stop(Stop.COAST)
    except:
        pass

# Ciclo principal infinito do gestor de slots
while True:
    hub.light.on(Color.BLUE)  # Luz azul indica menu de slots pronto
    
    # Organiza a ordem do menu com base na última posição guardada
    ordem_menu = SEQUENCIA[posicao:] + SEQUENCIA[:posicao]
    
    # Exibe o menu no Hub e aguarda a escolha do utilizador
    escolha = hub_menu(*ordem_menu)
    
    # SE ESCOLHERES O "0": Solta os motores e sai definitivamente para o ecrã inicial do Pybricks
    if escolha == "0":
        print("\n[SLOT 0] Soltando motores e voltando ao ecrã inicial do Pybricks...")
        soltar_motores()
        hub.light.on(Color.YELLOW)
        hub.speaker.beep(frequency=500, duration=200)
        raise SystemExit  # Este é o único sítio onde fechamos o script de propósito
        
    # SE ESCOLHERES UMA MISSÃO VÁLIDA (1 a 6):
    elif escolha in MISSOES:
        print(f"\n[SLOT {escolha}] Executando...")
        cronometro.reset()
        
        try:
            hub.light.on(Color.GREEN)  # Luz verde indica missão a correr
            MISSOES[escolha]()           # Executa a função run() da missão escolhida
            
            # Ao terminar com sucesso, corta o PID e solta os motores
            soltar_motores()
            
            tempo = cronometro.time() / 1000.0
            print(f"[OK] Slot {escolha} concluído em {tempo:.2f}s")
            hub.speaker.beep(frequency=600, duration=150)
            
            # Se a missão correu até ao fim, avança automaticamente para a próxima
            posicao = (SEQUENCIA.index(escolha) + 1) % len(SEQUENCIA)
            
        except SystemExit:
            # Captura o clique no botão central (interrupção a meio da missão)
            soltar_motores()
            hub.light.on(Color.BLUE)
            hub.speaker.beep(frequency=400, duration=100)
            print(f"\n[INTERROMPIDO] Motores livres! A voltar para o slot {escolha}...")
            
            # Mantém o cursor exatamente na missão que estavas a testar
            posicao = SEQUENCIA.index(escolha)
            
        except Exception as e:
            # Captura eventuais erros de código
            soltar_motores()
            hub.light.on(Color.RED)
            hub.speaker.beep(frequency=200, duration=800)
            print(f"[ERRO NO SLOT {escolha}]:", e)
            
            posicao = SEQUENCIA.index(escolha)