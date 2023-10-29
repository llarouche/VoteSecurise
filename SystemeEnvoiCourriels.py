#coding:utf-8
'''
Created on 1 janv. 2022

@author: Louis-Alain
'''
import smtplib, ssl
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from unidecode import unidecode

class SystemeEnvoiCourriels(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        self.mPort = 465  # For SSL
        self.mPassword = input("Mot de passe pour serveur SMTP:")
        self.mExpediteur="ne-pas-repondre@automain.com"
            
    def EnvoiSondage(self,iPrenom,iCourrielDestinataire,iLien):
        print("Envoi à %s"%iCourrielDestinataire)
       
        message = MIMEMultipart("alternative")
        message["Subject"] = "Lien pour sondage vetements 2024"
        message["From"] = "Sondage Cyclepop <%s>"%self.mExpediteur
        message["To"] = "%s <%s>"%(unidecode(iPrenom),iCourrielDestinataire)
        
        # Create the plain-text and HTML version of your message
        text = """\
        Bonjour %s,
            
        voici votre lien personnalisé pour participer au sondage sur les vetements 2024.
            
        Lien: %s
        
        Si vous ne pouvez pas cliquer sur le lien, copier le lien en appuyant longtemps sur celui-ci, sélectionnez 'Copier', et collez le lien dans un fureteur web.
            
        Ce lien ne peut être utilisé qu'une seule fois, ne le partagez pas.
            
        Cordialement,
        L'équipe du sondage sur les vêtements 2024 ."""%(iPrenom,iLien)
        html = """\
        <html>
          <body>
            <p>Bonjour %s,<br><br>
            
               voici votre lien personnalisé pour participer au sondage sur les vetements 2024.<br><br>
               
               Lien: <a href="%s">Cliquer ici.</a><br><br>
               
               Ce lien ne peut être utilisé qu'une seule fois, ne le partagez pas.<br><br>
               Cordialement,<br>
               L'équipe du sondage sur les vêtements 2024.
            </p>
          </body>
        </html>
        """%(iPrenom,iLien)
        
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        
        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)
        
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.netfirms.com", 465, context=context) as server:
            server.login(self.mExpediteur, self.mPassword)
            server.sendmail(
                self.mExpediteur, iCourrielDestinataire, message.as_string()
            )

    