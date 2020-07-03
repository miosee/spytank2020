#!/usr/bin/env python
import spytank

z ="z : avancer"
s ="s : reculer"
q = "q : tourner a gauche"
d = "d : tourner a droite"
vp = "a : plus vite"
vm = "e : moins vite"
x = "x : stop"
vitesse = 70

print(z,s,q,d,vp,vm,x)

spytank.init()

while True:
    lettre = input(">>> ")
    if lettre == "z" :
        spytank.avance(vitesse)
    elif lettre == "s" :
        spytank.recule(vitesse)
    elif lettre == "q" :
        spytank.gauche(vitesse)
    elif lettre == "d" :
        spytank.droite(vitesse)
    elif lettre == "a" :
        if vitesse < 100 :
            vitesse = vitesse + 10
    elif lettre == "e" :
        if vitesse > 30 :
            vitesse = vitesse - 10
    elif lettre == "x" :
        spytank.stop()
