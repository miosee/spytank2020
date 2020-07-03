import click
import spytank
import time

z ="z : avancer"
s ="s : reculer"
q = "q : tourner a gauche"
d = "d : tourner a droite"
vp = "a : plus vite"
vm = "e : moins vite"
x = "x : stop"
f = "f : sortir du programme"
vitesse = 70
continuer = True
# 1 pour avancer ; 2 pour reculer; 3 gauche; 4 droite
direction = 1
print(z,s,q,d,vp,vm,x,f)
spytank.init()

while continuer:
    lettre = click.getchar()
    if lettre == "z" :
        spytank.avance(vitesse)
        direction = 1
    elif lettre == "s" :
        spytank.recule(vitesse)
        direction = 2
    elif lettre == "q" :
        spytank.gauche(vitesse)
        direction = 3
    elif lettre == "d" :
        spytank.droite(vitesse)
        direction = 4
    elif lettre == "+" :
        if vitesse < 100 :
            vitesse = vitesse + 10

        if direction == 1 :
            spytank.avance(vitesse)
        elif direction == 2 :
            spytank.recule(vitesse)
        elif direction == 3 :
            spytank.gauche(vitesse)
        elif direction == 4 :
            spytank.droite(vitesse)

    elif lettre == "-" :
        if vitesse > 30 :
            vitesse = vitesse - 10
            
        if direction == 1 :
            spytank.avance(vitesse)
        elif direction == 2 :
            spytank.recule(vitesse)
        elif direction == 3 :
            spytank.gauche(vitesse)
        elif direction == 4 :
            spytank.droite(vitesse)
    elif lettre == "x" :
        spytank.stop()
    elif lettre == "f" :
        continuer = False
        spytank.stop()

    time.sleep(1)
