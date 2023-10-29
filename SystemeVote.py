#coding:utf-8
'''
Created on 23 oct. 2023

@author: Louis-Alain
'''
import os
from cryptography.fernet import Fernet
import SystemeEnvoiCourriels
import pandas

class SystemeVote(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.mPath=os.path.dirname(os.path.abspath(__file__))
        self.mFichierBrutMembres="Membres2023.csv"
        self.mFichierCourriels="CourrielsNoms.csv"
        self.mFichierCourrielsClefs="CourrielsNomsClefs.csv"
        self.mFichierClef="MotDePasse.txt"
        self.mClef=""
        self.mCodes=dict()
    
    def GenererClef(self):
        wClefTexte=Fernet.generate_key()
        self.mClef=Fernet(wClefTexte)
        with open(self.mPath+"\\"+self.mFichierClef,'w') as wFich:
            wFich.write("%s"%wClefTexte)
            wFich.close()        
            
    def ChargerClef(self):
        self.mClef=""
        with open(self.mPath+"\\"+self.mFichierClef,'r') as wFich:
            self.mClef=bytes(wFich.readline(),"utf-8")[2:-1]
            wFich.close()  

    def ImporterCourrielsValides(self):
        wLignesSales=list()
        wCsvPd=pandas.read_csv(self.mPath+"\\"+self.mFichierBrutMembres)
        wLignesReduites=list()
        wMembresValides=wCsvPd.loc[wCsvPd['Statut membre'] == "En règle"]
        wColonnesReduites=wMembresValides[['x','Courriel']]
        wColonnesReduites=wColonnesReduites.rename(columns={"x": "Prénom"})
        wUniques=wColonnesReduites["Courriel"].unique()

        wDf=pandas.DataFrame(data=None,columns=["Prénom","Courriel","Clef"])
        for wU in wUniques:
            wMembreDoublon=wColonnesReduites.loc[wCsvPd['Courriel'] == wU]
            wMembre=wMembreDoublon.iloc[0]
            #wMembre["Prénom"]=wMembre["Prénom"].capitalize()
            wDf=wDf.append(wMembre)
            
        wDf.to_csv(self.mPath+"\\"+self.mFichierCourriels)
        return wDf
        
    def SauverCodes(self,iListe):
        
        pass
    
    def GetCodes(self):
        pass
    
    def GenererCodes(self):
        
        # Charger le mot de passe
        self.ChargerClef()
        
        wMembres=self.ImporterCourrielsValides()
        
        # Créer les codes
        for index, row in wMembres.iterrows():
            wCourriel=row["Courriel"]
            wClefCourrielLong=Fernet(self.mClef).encrypt_at_time(bytes(wCourriel,'utf-8'),0)
            wClefCourriel=str(wClefCourrielLong[-10:])[2:-2]
            row["Clef"]=wClefCourriel
        
        wMembres.to_csv(self.mPath+"\\"+self.mFichierCourrielsClefs)
        
    def EnvoyerCourriels(self):
        
        wSysCourriels=SystemeEnvoiCourriels.SystemeEnvoiCourriels()
        # Ouvrir la liste de codes (avec courriels)
        wCsvPd=pandas.read_csv(self.mPath+"\\"+self.mFichierCourrielsClefs)
        
        # Envoyer un courriel par adresse
        for index, row in wCsvPd.iterrows():
            wCourriel=row["Courriel"]
            wClef=row["Clef"]
            wPrenom=row["Prénom"]
            wLien="https://s.surveylegend.com/-NhZqhYQQx7v1QHEJoXy?courriel=%s&clef=%s"%(wCourriel,wClef)
            wSysCourriels.EnvoiSondage(wPrenom, wCourriel, wLien)
        
        
        