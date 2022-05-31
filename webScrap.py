

from bs4 import BeautifulSoup
import re
import requests
import os
import smtplib
#import yagmail
from urllib.request import urlopen

class HespressScrapin():
  
    def __init__(self):
        self.link="https://covid.hespress.com/"

        self.result = requests.get(self.link)
        self.src = self.result.content
        self.soup = BeautifulSoup(self.src, 'lxml')
        

    def getConfirmed(self):
        x=self.soup.find_all("span",{"class":"badge badge-warning pr-2 pl-2"})            
        for tag in x:
            confirmed=int(tag.findAll(text=True)[0])
            
            return confirmed

    def getDeaths(self):
        tmp=self.soup.find_all("span",{"class":"badge badge-danger pr-2 pl-2"})
        for tag in tmp:
            deths=int(tag.findAll(text=True)[0])
            
            return deths

    def getHealed(self):
        tmp=self.soup.find_all("span",{"class":"badge badge-success pr-2 pl-2"})
        
        for tag in tmp:
            
            healed=(tag.findAll(text=True))
            
            
        return int(healed[0])

    def getHeader(self):
        html=urlopen(self.link)
        return html.info()

    def getLastModified(self):
        html=urlopen(self.link)
        return html.headers['last-modified']

if __name__=="__main__":

    myTest=HespressScrapin()
    deaths=myTest.getDeaths()
    confirmed=myTest.getConfirmed()
    healed=myTest.getHealed()
    date=myTest.getLastModified()
    print("number of confirmed : ",confirmed)
    print('number of deths : ',deaths)
    print("number of healed : ",healed)
    print('last Modification : ',date)

    file= open("last Update.txt","r+")
    
    m=file.read()
    print(m)
    
    if(m!=date):
        print("m is ",m)
        print(date)
        server=smtplib.SMTP_SSL("smtp.gmail.com",465)
        user="firad.fardi@gmail.com"
        password="Gmail123Gmail"
        to="email.emaill@gmail.com"
        message=f"Subject: COVID 19 Mise a jour \n\nLe nombre des cas confirmes est : {confirmed}\nLe nombre des cas guerie est : {healed}\nLe nombre des deces est : {deaths}\nStay SAFE "
        tmp="Le nombre des cas guérie est : {healed} Le nombre des décès est : {deaths} Stay SAFE"
        server.login(user,password)
        #server.sendmail(user,to,message)
        print('e-mail Sent')
        server.quit()
        file.seek(0)
        file.truncate(0)
        file.write(date)
        file.close()
    else:
        print('no update')