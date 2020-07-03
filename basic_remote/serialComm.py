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
# Librairie des fonctions de communication entre la RPi et l'Arduino du
# SpyTank de la SmartFormation de FIJ, via le port série de la connexion
# USB.
#
# History
# ------------------------------------------------
# Author    Date            Comments
# M. Osee   18 Juin 2020    Creation
#
########################################################################


import serial
import time


OUTPUT = 1
INPUT  = 0

########################################################################
# Definition de l'identifiant des commandes
########################################################################
# Commandes de mouvements
CMD_PIN_MODE      = 1
CMD_DIGITAL_READ  = 2
CMD_DIGITAL_WRITE = 3
CMD_ANALOG_WRITE  = 5
CMD_MOTEURS       = 6
CMD_DISTANCE      = 7


arduino = serial.Serial()




def pinMode(pin, mode):
    """ Demande a l'Arduino d'imposer le mode d'une patte digitale
    Parametres :
      pin : identifiant de la patte a modifier (2 -> 21)
      mode : mode a imposer a la patte (0 = INPUT, 1 = OUTPUT)
    Renvoie True si l'ordre a bien ete envoye, False sinon """

    if sendByte(CMD_PIN_MODE):
        if sendByte(pin):
            if sendByte(mode):
                return True
    return False


def digitalWrite(pin, etat):
    """ Demande a l'Arduino d'imposer l'etat d'une patte de sortie digitale
    Parametres :
      pin : identifiant de la patte a modifier (2 -> 21)
      etat : etat a imposer a la patte (0 = LOW, 1 = HIGH)
    Renvoie True si l'ordre a bien ete envoye, False sinon """

    if sendByte(CMD_DIGITAL_WRITE):
        if sendByte(pin):
            if sendByte(etat):
                return True
    return False


def moteurs(gauche, droit):
    """ Demande à l'Arduino d'imposer les vitesses des moteurs
    Parametres :
      gauche : vitesse à imposer au moteur gauche (-100 -> 100)
      droit : vitesse à imposer au moteur droit (-100 -> 100)
    Renvoie : 
      True si l'ordre a bien ete envoye, False sinon """

    if sendByte(CMD_MOTEURS):
        if sendByte(gauche):
            if sendByte(droit):
                return True
    return False

def distance(trigger, echo):
    """ Demande à l'Arduino la distance mesurée par le capteur ultrason
    Parametres :
      echo : identifiant de la Din connectée à la patte echo du capteur
      echo : identifiant de la Din connectée à la patte trigger du capteur
    Renvoie : 
      la distance mesurée (en cm),
      -1 si l'Arduino n'a pas correctement répondu """

    if sendByte(CMD_DISTANCE):
        if sendByte(trigger):
            if sendByte(echo):
                try:
                    b0 = unpack('B', arduino.read())
                    return b0
                except:
                    return -1
    return -1


########################################################################
# Fonctions Hardware
########################################################################

def init(port='/dev/ttyUSB0'):
    arduino.port = port
    arduino.baudrate = 9600
    arduino.parity=serial.PARITY_NONE
    arduino.stopbits=serial.STOPBITS_ONE
    arduino.bytesize=serial.EIGHTBITS
    arduino.timeout=1
    try:
        arduino.open()
    except OSError:
        print("Erreur de connexion à l'Arduino")

def close():
    arduino.close()

def sendByte(data):
    tmp1 = pack('b', data)
    # print('sending', tmp1)
    tmp2 = ''
    count = 0
    while (tmp2 != tmp1) and (count < 5):
        count = count+1
        arduino.write(tmp1)
        # arduino.reset_input_buffer()
        time.sleep(0.001)
        tmp2 = arduino.read()
        # print (tmp2)
    if count < 5:
        return True
    return False