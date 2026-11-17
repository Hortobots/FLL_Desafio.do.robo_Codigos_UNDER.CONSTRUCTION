from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Color, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

class RoboMundial:
    def __init__(self):
        self.hub = PrimeHub()
        self.tracao_ok = False
        self.garra_a = None
        self.garra_b = None
        self.cronometro = StopWatch()  # Cronómetro automático de missão

        # PERFIS DE COMPETIÇÃO COM OS VALORES EXATOS
        self.PERFIS = {
            "LEVE":     {"kp": 6800,  "ki": 90,  "kd": 35,  "vel": 400, "acel": 500},
            "VELOZ":    {"kp": 12000, "ki": 120, "kd": 600, "vel": 700, "acel": 850},
            "RETORNO":  {"kp": 28000, "ki": 120, "kd": 500, "vel": 650, "acel": 800},
            "PRECISAO": {"kp": 80500, "ki": 150, "kd": 500, "vel": 300, "acel": 600},
            "PESADO":   {"kp": 25000, "ki": 150, "kd": 600, "vel": 320, "acel": 400}  # KP reduzido e aceleração mais suave
        }

        self._inicializar_hardware()

    def _inicializar_hardware(self):
        try:
            # Tração confirmada nas Portas B e F
            self.motor_esq = Motor(Port.B, Direction.COUNTERCLOCKWISE)
            self.motor_dir = Motor(Port.F, Direction.CLOCKWISE)
            
            # Diâmetro de 58.1 mm e Axle Track de 105 mm
            self.drive = DriveBase(self.motor_esq, self.motor_dir, wheel_diameter=58.1, axle_track=105)
            self.drive.use_gyro(True)
            self.tracao_ok = True
        except Exception as e:
            print(f"[ERRO CRÍTICO] Falha nos Motores de Tração: {e}")
            self.hub.light.on(Color.RED)
            return

        # Inicializa acessórios nas portas A e E
        try:
            self.garra_a = Motor(Port.A)
        except Exception:
            print("[AVISO] Motor na Porta A não detetado.")

        try:
            self.garra_b = Motor(Port.E)
        except Exception:
            print("[AVISO] Motor na Porta E não detetado.")

        self.hub.light.on(Color.GREEN)
        self.perfil("LEVE")

    def perfil(self, nome: str):
        if not self.tracao_ok: return
        cfg = self.PERFIS.get(nome.upper(), self.PERFIS["LEVE"])
        # Aplica o PID personalizado de cada perfil
        self.drive.distance_control.pid(kp=cfg["kp"], ki=cfg["ki"], kd=cfg["kd"])
        self.drive.heading_control.pid(kp=cfg["kp"], ki=cfg["ki"], kd=cfg["kd"])
        self.drive.settings(straight_speed=cfg["vel"], straight_acceleration=cfg["acel"])

    def largada(self, nome_perfil: str = "LEVE"):
        """Inicia a missão: zera o giroscópio, aplica o perfil e reinicia o cronómetro."""
        if not self.tracao_ok: return
        self.drive.stop()
        wait(50)
        self.hub.imu.reset_heading(0)
        self.perfil(nome_perfil)
        self.hub.light.on(Color.GREEN)
        self.cronometro.reset()
        print(f"\n[LARGADA] Cronómetro iniciado | Perfil: {nome_perfil}")

    def tempo(self) -> float:
        """Retorna e exibe no terminal o tempo decorrido desde a largada."""
        segundos = self.cronometro.time() / 1000.0
        print(f"[TEMPO] {segundos:.2f}s")
        return segundos

    def andar(self, distancia_cm: float, velocidade: float = None, aceleracao: float = None):
        if not self.tracao_ok: return
        v_orig, a_orig, _, _ = self.drive.settings()
        v_exec = abs(velocidade) if velocidade is not None else v_orig
        a_exec = aceleracao if aceleracao is not None else a_orig

        self.drive.settings(straight_speed=v_exec, straight_acceleration=a_exec)
        self.drive.straight(distancia_cm * 10.0)
        self.drive.settings(straight_speed=v_orig, straight_acceleration=a_orig)
        self.tempo()

    def girar(self, angulo_absoluto: float, velocidade: float = 300):
        if not self.tracao_ok: return
        erro = angulo_absoluto - self.hub.imu.heading()
        _, _, v_rot_orig, _ = self.drive.settings()
        self.drive.settings(turn_rate=velocidade)
        self.drive.turn(erro)
        self.drive.settings(turn_rate=v_rot_orig)
        self.tempo()

    def girar_relativo(self, angulo_relativo: float, velocidade: float = 300):
        if not self.tracao_ok: return
        rumo_atual = self.hub.imu.heading()
        self.girar(rumo_atual + angulo_relativo, velocidade)

    def curva(self, raio_cm: float, angulo: float, velocidade: float = None):
        if not self.tracao_ok: return
        v_orig, _, _, _ = self.drive.settings()
        v_exec = abs(velocidade) if velocidade is not None else v_orig
        raio_mm = raio_cm * 10.0
        self.drive.settings(straight_speed=v_exec)
        self.drive.curve(radius=raio_mm, angle=angulo)
        self.drive.settings(straight_speed=v_orig)
        self.tempo()

    def alinhar_parede(self, tempo_ms: int = 1200, angulo_pos_alinhamento: float = 0, velocidade_re: float = -150):
        if not self.tracao_ok: return
        self.drive.drive(velocidade_re, 0)
        wait(tempo_ms)
        self.drive.stop()
        wait(50)
        self.hub.imu.reset_heading(angulo_pos_alinhamento)
        self.tempo()

    def mover_garra_a(self, graus: float, velocidade: float = 350, aceleracao: float = None, esperar: bool = True):
        """Move o motor da Porta A."""
        if not self.garra_a: return
        v_max_orig, a_max_orig = self.garra_a.control.limits()[:2]
        if aceleracao is not None:
            self.garra_a.control.limits(speed=abs(velocidade), acceleration=abs(aceleracao))
        else:
            self.garra_a.control.limits(speed=abs(velocidade))
        self.garra_a.run_angle(abs(velocidade), graus, then=Stop.HOLD, wait=esperar)
        self.garra_a.control.limits(speed=v_max_orig, acceleration=a_max_orig)
        if esperar: self.tempo()

    def mover_garra_b(self, graus: float, velocidade: float = 350, aceleracao: float = None, esperar: bool = True):
        """Move o motor da Porta E."""
        if not self.garra_b: return
        v_max_orig, a_max_orig = self.garra_b.control.limits()[:2]
        if aceleracao is not None:
            self.garra_b.control.limits(speed=abs(velocidade), acceleration=abs(aceleracao))
        else:
            self.garra_b.control.limits(speed=abs(velocidade))
        self.garra_b.run_angle(abs(velocidade), graus, then=Stop.HOLD, wait=esperar)
        self.garra_b.control.limits(speed=v_max_orig, acceleration=a_max_orig)
        if esperar: self.tempo()

    def checar_bateria(self) -> int:
        tensao = self.hub.battery.voltage()
        porcentagem = max(0, min(100, int((tensao - 7200) / (8300 - 7200) * 100)))
        print(f"[TELEMETRIA] Tensão: {tensao}mV | Bateria: {porcentagem}%")
        if tensao < 7400:
            self.hub.light.on(Color.RED)
            self.hub.speaker.beep(frequency=300, duration=800)
        return porcentagem

# Instância Global e Mapeamento de Atalhos
bot = RoboMundial()

largada = bot.largada
perfil = bot.perfil
tempo = bot.tempo
andar = bot.andar
girar = bot.girar
girar_relativo = bot.girar_relativo
curva = bot.curva
alinhar_parede = bot.alinhar_parede
mover_garra_a = bot.mover_garra_a
mover_garra_b = bot.mover_garra_b
checar_bateria = bot.checar_bateria
hub = bot.hub