from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from smtplib import SMTP
import requests
import os
import lxml
import unidecode

def txt_generator(houses):
    new_houses = []
    with open(os.getcwd()+'/results/results.txt', 'r+') as file: 
        data_lines = file.readlines()
        for house in houses:
            if house not in data_lines:
               file.writelines(house)
               new_houses.append(house)
        file.close()
    return new_houses

def send_email(new_houses):
    [print(house) for house in new_houses]
    message = MIMEMultipart('plain')
    message['From'] = 'your_mail@outlook.es' # origin mail
    message['To'] = 'destination_mail@gmail.com' # destination mail
    message['Subject'] = 'New Houses To View'
    attached = MIMEBase('application', 'octect-stream')
    attached.set_payload(open('results/results.txt','rb').read())
    attached.add_header('content-Disposition', 'attachment; filename="houses_global.txt"')
    message.attach(attached)
    [message.attach(MIMEText(house, 'plain')) for house in new_houses]
    
    smtp = SMTP('smtp.live.com') #Or gmail.com, yahoo.com ...
    smtp.starttls()

    smtp.login('your_mail@outlook.es','your_pass')
    smtp.sendmail('your_mail@outlook.es','destination_mail@gmail.com', message.as_string().encode('utf-8'))
    smtp.quit()
    
if __name__ == '__main__': 

    url = 'https://www.pisos.com/venta/pisos-pinar_del_rey/' # search
    try:
        page = requests.get(url, headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
            }, timeout=5)
    except requests.exceptions.ConnectionError:
        print('Connection refused')
    soup = BeautifulSoup(page.content, 'lxml')
    results = soup.find_all('div', attrs={'data-listado-row':'true'})
    
    houses = []

    for result in results:
        link = result.find('meta', attrs={'itemprop':'url'}).get('content')
        price = (result.find('div', attrs={'class':'price'}).text).strip()
        location = (result.find('div', attrs={'class':'location'}).text).strip()
        meters = (result.find_all('div', attrs={'class':'item'})[0].text).strip()

        house = unidecode.unidecode('https://www.pisos.com' + link + ' | ' + price + ' | ' + location + ' | ' + meters + '\n')
        houses.append(house)

    new_houses = txt_generator(houses)

    if len(new_houses) > 0:
        send_email(new_houses)
        print('mail sent')
    else:
        print("no new houses")