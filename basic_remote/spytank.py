
#!/usr/bin/env python
from __future__ import print_function
from __future__ import division
from struct import pack, unpack
# the above lines are meant for Python3 compatibility.
# they force the use of Python3 functionality for print()
# and the integer division
# mind your parentheses!

########################################################################
#
# Librairie des fonctions de permettant a la RPi de controler l'Arduino
# du SpyTank de la SmartFormation de FIJ, via la connexion USB
#
# History
# ------------------------------------------------
# Author    Date            Comments
# M. Osee   18 Juin 2020    Creation
#
########################################################################

import serialComm

########################################################################
# Définition des pattes de l'Arduino utilisées
########################################################################
# Pattes pour les LEDs
LED_GAUCHE = 2
LED_DROITE = 3
# Pattes pour le capteur de distance
ECHO = 4
TRIGGER = 5


def init(port='/dev/ttyUSB0'):
    """ Initialise la communication avec l'Arduino.
        Elle configure le port série pour communiquer avec l'Arduino et configure les pattes des LEDs et du capteur de distance
        Elle doit être appelée en premier. 
        Paramètre :
            port : identifiant du port série utilisé ('/dev/ttyUSB0' par défaut)
        Renvoie True si l'initialisation s'est bien passée, False sinon """

    # Initialisation de la communication
    serialComm.init(port)
    # Configuration des pattes utilisées
    if not(serialComm.pinMode(LED_GAUCHE, serialComm.OUTPUT)):
        print("Erreur à la configuration de la patte de la LED gauche")
    if not(serialComm.pinMode(LED_DROITE, serialComm.OUTPUT)):
        print("Erreur à la configuration de la patte de la LED gauche")
    if not(serialComm.pinMode(TRIGGER, serialComm.OUTPUT)):
        print("Erreur à la configuration de la patte echo")
    if not(serialComm.pinMode(ECHO, serialComm.INPUT)):
        print("Erreur à la configuration de la patte trigger")


def close():
    """ Arrête proprement la communication avec l'Arduino """ 
    serialComm.close()


def led(pin, etat):
    """ Ordonne a l'Arduino d'allumer ou éteindre une LED
        Parametres :
            pin : identifiant de la LED (LED_GAUCHE, LED_DROITE)
            etat : etat a imposer a la patte (0 pour éteindre, 1 pour allumer)
        Renvoie True si l'ordre a bien été exécuté, False sinon """

    if pin==LED_GAUCHE or pin==LED_DROITE:
        return serialComm.digitalWrite(pin, etat)
    else:
        print('led inconnue !')
        return False


def stop():
    """ Ordonne à l'Arduino d'arrêter les moteurs.
        Renvoie True si l'ordre a bien été exécuté, False sinon """

    return serialComm.moteurs(0, 0)   


def avance(vitesse):
    """ Ordonne à l'Arduino de faire avancer le spytank
        Paramètre:
          vitesse : vitesse à utiliser (-100 -> 100)
        Renvoie True si l'ordre a bien été exécuté, False sinon """

    serialComm.moteurs(vitesse, vitesse)


def recule(vitesse):
    """ Ordonne à l'Arduino de faire reculer le spytank
        Paramètre:
          vitesse : vitesse à utiliser (-100 -> 100)
        Renvoie True si l'ordre a bien été exécuté, False sinon """

    serialComm.moteurs(-vitesse, -vitesse)


def droite(vitesse):
    """ Ordonne à l'Arduino de faire tourner le spytank à droite
        Paramètre:
          vitesse : vitesse à utiliser (-100 -> 100)
        Renvoie True si l'ordre a bien été exécuté, False sinon """

    serialComm.moteurs(vitesse, -vitesse)


def gauche(vitesse):
    """ Ordonne à l'Arduino de faire tourner le spytank à gauche
        Paramètre:
          vitesse : vitesse à utiliser (-100 -> 100)
        Renvoie True si l'ordre a bien été exécuté, False sinon """

    serialComm.moteurs(-vitesse, vitesse)

def litDistance():
    """ Demande à l'Arduino la distance mesurée par le capteur ultrason
    Renvoie : 
      la distance mesurée (en cm),
      -1 si l'Arduino n'a pas correctement répondu """
    return serialComm.distance(TRIGGER, ECHO)
