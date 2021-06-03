import requests
from bs4 import BeautifulSoup
import lxml
import fake_useragent
import pandas as pd
import time
import datetime
import timedelta
import webbrowser
import re


user = fake_useragent.UserAgent(use_cache_server=False,verify_ssl=False).random
header = {'user-agent': user}
user2 = fake_useragent.UserAgent(use_cache_server=False,verify_ssl=False).random
header2 = {'user-agent': user2}
refs = []

#Создание таблички
#data = pd.DataFrame(columns = ['today', 'callsign', 'flag', 'imo/mmsi', 'position', 'pos_recieved', 'speed', 'status', 'destination', 'ETA'])
data = pd.DataFrame(columns = ['collection_date', 'callsign', 'flag', 'mmsi', 'current_position', 'cord_n', 'cord_w', 'pos_recieved','speed', 'status', 'destination', 'ETA', 'reference'])
#Сегодняшняя дата
today = datetime.datetime.now() 
today_str = today.strftime('%Y-%m-%d') #Перевод

for i in range (1,107):
    link = f'https://www.vesselfinder.com/vessels?page={i}&type=7'

    response = requests.get(link, headers = header).text
    soup = BeautifulSoup(response, 'lxml')
    """
    main_s = soup.find('main', class_='mygrid3')
    col2 = main_s.find('div', class_='col2 page')
    section = col2.find('section', class_='listing')
    table = section.find('table', class_='results table is-hoverable is-fullwidth')
    tbody = table.find('tbody')
    trki = tbody.findAll('tr')

    #Получение списка наименований с 1 страницы
    print(f'\nСтраница {i}:')
    for tr in trki:
        tr1 = tr.find('td', class_='v2')
        tr2 = tr1.find('div',class_='sli')
        sli = tr2.find('div', class_='slna')
        print(sli.text)
    """
    
    ### Парсинг стартового окна с параметром 'military' ###
    main_s = soup.find('main', class_='mygrid3')
    col2 = main_s.find('div', class_='col2 page')
    section = col2.find('section', class_='listing')
    table = section.find('table', class_='results table is-hoverable is-fullwidth')
    tbody = table.find('tbody')
    trki = tbody.findAll('tr')

    #print(f'\nСтраница {i}:')
    for tr in trki:
        tr1 = tr.find('td', class_='v2')
        tr2 = tr1.find('a', class_='ship-link')
        ref = tr2.get('href')
        refs.append(f'https://www.vesselfinder.com{ref}')
        #print(f'https://www.vesselfinder.com{ref}')

'''
for i in refs:#range(0,len(refs)):
    response2 = requests.get(i, headers = header).text
    soup2 = BeautifulSoup(response2, 'lxml')
    main_2 = soup2.find('main', class_='mygrid3')
    col22 = main_2.find('div', class_='col2 page')
    section1 = col22.find('div', class_='column ship-section')
    p1 = section1.find('p', class_='text2')
    print(p1)
'''  

for i in refs:#range(0,len(refs)):
    try:
        response2 = requests.get(i, headers = header2).text
    except requests.exceptions.ConnectionError as e:
        pass
    soup2 = BeautifulSoup(response2, 'lxml')
    main_2 = soup2.find('main', class_='mygrid3')
    col22 = main_2.find('div', class_='col2 page')
    section23 = col22.find('section', class_='column ship-section')
    columns = section23.find('div', class_='columns')
    vx_top = columns.find('div', class_='column vfix-top')

    ##Current Position
    div_column_section = col22.find('div', class_='column ship-section')
    p_column_section = div_column_section.find('p',class_='text2')
    res1 = re.split(r'at', p_column_section.text)
    if res1[0] != '\n':
        res2 = re.split(r'\(', res1[1])
        res3 = res2[0].lstrip()
        current_position = res3.rstrip()
    else:
        current_position = '-'
    print(current_position)
    ##Destination

    if 'port of' in p_column_section.text:
        dd = vx_top.find('div',class_='s0')
        if dd != None:
            cc = dd.find('div',class_='flx _rLk')
            if cc != None:
                ee = cc.find('div',class_='vi__r1 vi__sbt')
                if ee != None:
                    ##ETA
                    xx = ee.find('div',class_='_value')
                    if xx != None:
                        xx1 = xx.find('span', class_='_mcol12')
                        if xx1 != None:
                            re1 = re.split(r'ETA: ', xx1.text)
                            try:
                                ETA = re1[1]
                            except:
                                ETA = '-'
                            print(ETA)
                        else:
                            ETA = '-'

                    ff = ee.find('a',class_='_npNa')
                    destination = ff.text
                    print(destination)
                else:
                    destination = '-'
                    ETA = '-'
            else:
                ETA = '-'
                destination = '-'
        else:       
            destination = '-'
            ETA = '-'
    else:
        destination = '-'
        ETA = '-'
    

    ##Coordinates
    #cord_N
    div_column_section = col22.find('div', class_='column ship-section')
    p_column_section = div_column_section.find('p',class_='text2')
    res1 = re.split(r'\/', p_column_section.text)
    if res1[0] != '\n':
        res2 = re.split(r'coordinates ', res1[0])
        res3 = re.findall(r'[0123456789.]+', res2[1])
        cord_n = res3[0]
        #print(res3[0])
    else:
        cord_n = '-'
    #_cord_W
    div_column_section = col22.find('div', class_='column ship-section')
    p_column_section = div_column_section.find('p',class_='text2')
    res1 = re.split(r'\/', p_column_section.text)
    if res1[0] != '\n':
        res2 = re.findall(r'[0123456789.]+', res1[1])
        cord_w = res2[0]
        #print(res2[0])
    else:
        cord_w = '-'
    


    if vx_top != None:
        vx_top_0 = vx_top.find('div', class_='s0')

        ##Callsign
        flx = vx_top_0.findAll('div', class_='flx')[1]
        if flx != None:
            table_0 = flx.find('table',class_='aparams')
            if table_0 != None:
                table_main = table_0.find('tbody')
                if table_main != None:
                    tr5 = table_main.findAll('tr')[5]
                    if tr5 != None:
                        callsign = tr5.find('td',class_='v3').text
                        print(callsign)
                    else:
                        callsign = '-'
        ##Flag
        flx = vx_top_0.findAll('div', class_='flx')[1]
        if flx != None:
            table_0 = flx.find('table',class_='aparams')
            if table_0 != None:
                table_main = table_0.find('tbody')
                if table_main != None:
                    tr5 = table_main.findAll('tr')[6]
                    if tr5 != None:
                        flag = tr5.find('td',class_='v3').text
                        print(flag)
                    else:
                        flag = '-'

        ##Imo/mmsi
        flx = vx_top_0.findAll('div', class_='flx')[1]
        if flx != None:
            table_0 = flx.find('table',class_='aparams')
            if table_0 != None:
                table_main = table_0.find('tbody')
                if table_main != None:
                    tr5 = table_main.findAll('tr')[4]
                    if tr5 != None:
                        mmsi1 = tr5.find('td',class_='v3').text
                        mmsi_1 = re.split(r'/', mmsi1)
                        mmsi = mmsi_1[1].replace(' ', '')
                        print(mmsi)
                        #Reference
                        reference = f'https://www.vesselfinder.com/?mmsi={mmsi}'
                    else:
                        mmsi = '-'


        ##Position
        

        ##Pos_recieved
        flx = vx_top_0.findAll('div', class_='flx')[1]
        if flx != None:
            table_0 = flx.find('table',class_='aparams')
            if table_0 != None:
                table_main = table_0.find('tbody')
                if table_main != None:
                    tr5 = table_main.findAll('tr')[3]
                    if tr5 != None:
                        pos_recieved_0 = tr5.find('td',class_='v3').text
                        pos_recieved = pos_recieved_0.replace('i','')
                        #pos_recieved = pos_recieved_1.replace(' ','')
                        print(pos_recieved)
                    else:
                        pos_recieved = '-'


        ##Speed
        flx = vx_top_0.findAll('div', class_='flx')[1]
        if flx != None:
                table_0 = flx.find('table',class_='aparams')
                if table_0 != None:
                    table_main = table_0.find('tbody')
                    if table_main != None:
                        tr5 = table_main.findAll('tr')[0]
                        if tr5 != None:
                            speed_0 = tr5.find('td',class_='v3').text
                            speed1 = re.split(r'/', speed_0)
                            speedx = speed1[1].replace(' ', '')
                            speed2 = speedx.replace('kn','')
                            if speed2 != '-':
                                speed_float = float(speed2) * 1.852
                                speedr = round(speed_float,1)
                                speed = str(speedr)
                                #############HEREEE
                            else:
                                speed = '-'
                            print(speed)
    

        ##Status
        flx = vx_top_0.findAll('div', class_='flx')[1]
        if flx != None:
            table_0 = flx.find('table',class_='aparams')
            if table_0 != None:
                table_main = table_0.find('tbody')
                if table_main != None:
                    tr5 = table_main.findAll('tr')[2]
                    if tr5 != None:
                        status = tr5.find('td',class_='v3').text
                        print(status)
                    else:
                        status = '-'

    #Заполнение таблички    
    data.loc[len(data)] = [today_str, callsign, flag, mmsi, current_position, cord_n, cord_w, pos_recieved, speed, status, destination, ETA, reference]
data.to_csv(f'{today_str}.csv', index=False)

''' #Запись в файл
refs_txt = open('refs.txt', 'w')
for element in refs:
     refs_txt.write(f'https://www.vesselfinder.com{element}')
     refs_txt.write('\n')
refs_txt.close()
'''






     
