import spytank
import time

spytank.init('/dev/ttyUSB0')

print('led gauche')
spytank.led(spytank.LED_GAUCHE, 1)
time.sleep(0.3)
spytank.led(spytank.LED_GAUCHE, 0)
time.sleep(0.3)
print('  --')
print('led droite')
spytank.led(spytank.LED_DROITE, 1)
time.sleep(0.3)
spytank.led(spytank.LED_DROITE, 0)
time.sleep(0.3)

print('  --')
print('avance')
spytank.avance(80)
time.sleep(4)
spytank.stop()
time.sleep(0.5)
print('recule')
spytank.recule(80)
time.sleep(4)
spytank.stop()
time.sleep(0.5)
print('droite')
spytank.droite(80)
time.sleep(4)
spytank.stop()
time.sleep(0.5)
print('gauche')
spytank.gauche(80)
time.sleep(4)
spytank.stop()

print('  --')
print('Distance')
for a in range(10):
    print(spytank.litDistance())
    time.sleep(1)

spytank.close()
