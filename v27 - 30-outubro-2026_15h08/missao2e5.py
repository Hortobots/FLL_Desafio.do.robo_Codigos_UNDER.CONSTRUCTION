from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

andar(15, velocidade=500, aceleraçao=600)
mover_garra_a(140, velocidade=500, aceleracao=600)
andar(-15, velocidade=500, aceleracao=600)
