#coding:utf-8
'''
Created on 23 oct. 2023

@author: Louis-Alain
'''
import sys
from SystemeVote import SystemeVote

if __name__ == '__main__':
    print("Vote Securise pour Cyclepop")
    print("Version 0.0.0.0")
    print("")
    print("Conseil: lancer avec l'argument -u pour afficher les sorties de printf sur le champ (python -u Vote Securise.py 1).")
    
    wSystemeVote=SystemeVote()
    
    if len(sys.argv) == 2:
        wId=int(sys.argv[1])
        if wId==1:
            wSystemeVote.GenererClef()
        elif wId==2:
            wSystemeVote.GenererCodes()
        elif wId==3:
            wSystemeVote.EnvoyerCourriels()
        
    else:
        print("Usage: Doit être lancé avec l'id. ex: \n VoteSecurise.py 1")
        exit(1) 
    
    
    pass