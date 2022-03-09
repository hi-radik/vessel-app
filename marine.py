import requests
from bs4 import BeautifulSoup
import lxml
import fake_useragent
import webbrowser
import re
import os
import pandas as pd
import datetime

print('Marine working!')

#user = fake_useragent.UserAgent(use_cache_server=False,verify_ssl=False).random
header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15'}
#user2 = fake_useragent.UserAgent(use_cache_server=False,verify_ssl=False).random
header2 = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15'}
refs = []

#Создание таблички
#data = pd.DataFrame(columns = ['today', 'callsign', 'flag', 'imo/mmsi', 'position', 'pos_recieved', 'speed', 'status', 'destination', 'ETA'])
data = pd.DataFrame(columns = ['collection_date', 'callsign', 'vessel_type', 'flag', 'mmsi', 'current_position', 'cord_n', 'cord_w', 'pos_recieved','speed', 'status', 'destination', 'ETA', 'reference'])
#Сегодняшняя дата
today = datetime.datetime.now()
today_str = today.strftime('%Y-%m-%d') #Перевод

for i in range (1,109):
    link = f'https://www.vesselfinder.com/vessels?page={i}&type=7'
    #
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
    try:
        main_s = soup.find('main', class_='mygrid3')
        col2 = main_s.find('div', class_='col2 page')
        section = col2.find('section', class_='listing')
        table = section.find('table', class_='results table is-hoverable is-fullwidth')
        tbody = table.find('tbody')
        trki = tbody.findAll('tr')
    except:
        continue

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
print('I am still working!')
for i in refs:#range(0,len(refs)):
    try:
        #
        response2 = requests.get(i, headers = header2).text
    except requests.exceptions.ConnectionError as e:
        pass
    summa = 0
    summa += 1
    print(summa)
    soup2 = BeautifulSoup(response2, 'lxml')
    try:
        main_2 = soup2.find('main', class_='mygrid3')
        col22 = main_2.find('div', class_='col2 page')
        section23 = col22.find('section', class_='column ship-section')
        columns = section23.find('div', class_='columns')
        vx_top = columns.find('div', class_='column vfix-top')
    except:
        continue

    ##Current Position
    div_column_section = col22.find('div', class_='column ship-section')
    p_column_section = div_column_section.find('p',class_='text2')
    try:
        res1 = re.split(r'at', p_column_section.text)
        if res1[0] != '\n':
            res2 = re.split(r'\(', res1[1])
            res3 = res2[0].lstrip()
            current_position = res3.rstrip()
        else:
            current_position = '-'
    except:
        current_position = '-'
    #print(current_position)
    ##Destination

    print('Yeaaah!')
    try:
        if 'port of' in p_column_section.text:
            dd = vx_top.find('div',class_='s0')
        else:
            destination = '-'
            ETA = '-'
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
                            #print(ETA)
                        else:
                            ETA = '-'

                    ff = ee.find('a',class_='_npNa')
                    destination = ff.text
                    #print(destination)
                else:
                    destination = '-'
                    ETA = '-'
            else:
                ETA = '-'
                destination = '-'
        else:
            destination = '-'
            ETA = '-'

    except:
        destination = '-'
        ETA = '-'

    ##Coordinates
    #cord_N
    div_column_section = col22.find('div', class_='column ship-section')
    p_column_section = div_column_section.find('p',class_='text2')
    try:
        res1 = re.split(r'\/', p_column_section.text)
        if res1[0] != '\n':
            res2 = re.split(r'coordinates ', res1[0])
            res3 = re.findall(r'[0123456789.]+', res2[1])
            cord_n = res3[0]
            #print(res3[0])
        else:
            cord_n = '-'
    except:
        cord_n = '-'
    #_cord_W
    div_column_section = col22.find('div', class_='column ship-section')
    p_column_section = div_column_section.find('p',class_='text2')
    try:
        res1 = re.split(r'\/', p_column_section.text)
        if res1[0] != '\n':
            res2 = re.findall(r'[0123456789.]+', res1[1])
            cord_w = res2[0]
            #print(res2[0])
        else:
            cord_w = '-'
    except:
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
                    tr5 = table_main.findAll('tr')[7]
                    if tr5 != None:
                        try:
                            callsign = tr5.find('td',class_='v3').text
                        except:
                            callsign = '-'
                        #print(callsign)
                    else:
                        callsign = '-'
        ##Flag
        flx = vx_top_0.findAll('div', class_='flx')[1]
        if flx != None:
            table_0 = flx.find('table',class_='aparams')
            if table_0 != None:
                table_main = table_0.find('tbody')
                if table_main != None:
                    tr5 = table_main.findAll('tr')[8]
                    if tr5 != None:
                        try:
                            flag = tr5.find('td',class_='v3').text
                        except:
                            flag = '-'
                        #print(flag)
                    else:
                        flag = '-'

        ##Imo/mmsi
        flx = vx_top_0.findAll('div', class_='flx')[1]
        if flx != None:
            table_0 = flx.find('table',class_='aparams')
            if table_0 != None:
                table_main = table_0.find('tbody')
                if table_main != None:
                    tr5 = table_main.findAll('tr')[6]
                    if tr5 != None:
                        try:
                            mmsi1 = tr5.find('td',class_='v3 v3np').text
                            mmsi_1 = re.split(r'/', mmsi1)
                            try:
                                mmsi = mmsi_1[1].replace(' ', '')
                            except:
                                mmsi = mmsi_1[0].replace(' ', '')
                        #print(mmsi)
                        #Reference
                            reference = f'https://www.vesselfinder.com/?mmsi={mmsi}'
                        except:
                            mmsi = '-'
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
                    tr5 = table_main.findAll('tr')[5]
                    if tr5 != None:
                        try:
                            pos_recieved_0 = tr5.find('td',class_='v3 ttt1').text
                            pos_recieved1 = pos_recieved_0.replace('i','')
                            pos_recieved = pos_recieved1.rstrip()
                        except:
                            pos_recieved = '-'
                        #print(pos_recieved)
                    else:
                        pos_recieved = '-'


        ##Speed
        flx = vx_top_0.findAll('div', class_='flx')[1]
        if flx != None:
                table_0 = flx.find('table',class_='aparams')
                if table_0 != None:
                    table_main = table_0.find('tbody')
                    if table_main != None:
                        tr5 = table_main.findAll('tr')[2]
                        if tr5 != None:
                            try:
                                speed_0 = tr5.find('td',class_='v3').text
                                speed1 = re.split(r'/', speed_0)
                            except:
                                speed= '-'
                            try:
                                speedx = speed1[1].replace(' ', '')
                            except:
                                speedx = speed1[0].replace(' ', '')
                            speed2 = speedx.replace('kn','')
                            if speed2 != '-' and speed2 != '':
                                try:
                                    speed_float = float(speed2) * 1.852
                                    speedr = round(speed_float,1)
                                    speed = str(speedr)
                                except:
                                    speed= '-'

                                #############HEREEE
                            else:
                                speed = '-'
                            #print(speed)

        ##type
        vessel_type = 'Military'

        ##Status
        flx = vx_top_0.findAll('div', class_='flx')[1]
        if flx != None:
            table_0 = flx.find('table',class_='aparams')
            if table_0 != None:
                table_main = table_0.find('tbody')
                if table_main != None:
                    tr5 = table_main.findAll('tr')[4]
                    if tr5 != None:
                        try:
                            status1 = tr5.find('td',class_='v3').text
                            if len(status1) == 62:
                                status = '-'
                            else:
                                status = status1.replace('\n', '')
                        except:
                            status = '-'


                        #print(status)
                    else:
                        status = '-'

    #Заполнение таблички
    data.loc[len(data)] = [today_str, callsign, vessel_type, flag, mmsi, current_position, cord_n, cord_w, pos_recieved, speed, status, destination, ETA, reference]
for i in range (1,3317):
    print(3317)
    link = f'https://www.vesselfinder.com/vessels?page={i}&type=4'
    #
    response = requests.get(link, headers = header).text
    soup = BeautifulSoup(response, 'lxml')

    ### Парсинг стартового окна с параметром 'military' ###
    body_w = soup.find('div', class_='body-wrapper')
    body_i = body_w.find('div', class_='body-inner')
    try:
        main_s = body_i.find('main', class_='mygrid3')
        col2 = main_s.find('div', class_='col2 page')
        section = col2.find('section', class_='listing')
        table = section.find('table', class_='results table is-hoverable is-fullwidth')
        tbody = table.find('tbody')
        trki = tbody.findAll('tr')
    except:
        continue

    #print(f'\nСтраница {i}:')
    for tr in trki:
        tr1 = tr.find('td', class_='v2')
        tr2 = tr1.find('a', class_='ship-link')
        ref = tr2.get('href')
        refs.append(f'https://www.vesselfinder.com{ref}')
        #print(f'https://www.vesselfinder.com{ref}')


print('I am still working!')
for i in refs:#range(0,len(refs)):
    try:
        #
        response2 = requests.get(i, headers = header2).text
    except requests.exceptions.ConnectionError as e:
        pass
    soup2 = BeautifulSoup(response2, 'lxml')
    try:
        main_2 = soup2.find('main', class_='mygrid3')
        col22 = main_2.find('div', class_='col2 page')
        section23 = col22.find('section', class_='column ship-section')
        columns = section23.find('div', class_='columns')
        vx_top = columns.find('div', class_='column vfix-top')
    except:
        continue

    ##Current Position
    div_column_section = col22.find('div', class_='column ship-section')
    p_column_section = div_column_section.find('p',class_='text2')
    try:
        res1 = re.split(r'at', p_column_section.text)
        if res1[0] != '\n':
            res2 = re.split(r'\(', res1[1])
            res3 = res2[0].lstrip()
            current_position = res3.rstrip()
        else:
            current_position = '-'
    except:
        current_position = '-'
    #print(current_position)
    ##Destination

    print('Yeaaah!')
    try:
        if 'port of' in p_column_section.text:
            dd = vx_top.find('div',class_='s0')
        else:
            destination = '-'
            ETA = '-'
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
                            #print(ETA)
                        else:
                            ETA = '-'

                    ff = ee.find('a',class_='_npNa')
                    destination = ff.text
                    #print(destination)
                else:
                    destination = '-'
                    ETA = '-'
            else:
                ETA = '-'
                destination = '-'
        else:
            destination = '-'
            ETA = '-'

    except:
        destination = '-'
        ETA = '-'


    ##Coordinates
    #cord_N
    div_column_section = col22.find('div', class_='column ship-section')
    p_column_section = div_column_section.find('p',class_='text2')
    try:
        res1 = re.split(r'\/', p_column_section.text)
        if res1[0] != '\n':
            res2 = re.split(r'coordinates ', res1[0])
            res3 = re.findall(r'[0123456789.]+', res2[1])
            cord_n = res3[0]
            #print(res3[0])
        else:
            cord_n = '-'
    except:
        cord_n = '-'
    #_cord_W
    div_column_section = col22.find('div', class_='column ship-section')
    p_column_section = div_column_section.find('p',class_='text2')
    try:
        res1 = re.split(r'\/', p_column_section.text)
        if res1[0] != '\n':
            res2 = re.findall(r'[0123456789.]+', res1[1])
            cord_w = res2[0]
            #print(res2[0])
        else:
            cord_w = '-'
    except:
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
                    tr5 = table_main.findAll('tr')[7]
                    if tr5 != None:
                        try:
                            callsign = tr5.find('td',class_='v3').text
                        except:
                            callsign = '-'
                        #print(callsign)
                    else:
                        callsign = '-'
        ##Flag
        flx = vx_top_0.findAll('div', class_='flx')[1]
        if flx != None:
            table_0 = flx.find('table',class_='aparams')
            if table_0 != None:
                table_main = table_0.find('tbody')
                if table_main != None:
                    tr5 = table_main.findAll('tr')[8]
                    if tr5 != None:
                        try:
                            flag = tr5.find('td',class_='v3').text
                        except:
                            flag = '-'
                        #print(flag)
                    else:
                        flag = '-'

        ##Imo/mmsi
        flx = vx_top_0.findAll('div', class_='flx')[1]
        if flx != None:
            table_0 = flx.find('table',class_='aparams')
            if table_0 != None:
                table_main = table_0.find('tbody')
                if table_main != None:
                    tr5 = table_main.findAll('tr')[6]
                    if tr5 != None:
                        try:
                            mmsi1 = tr5.find('td',class_='v3 v3np').text
                            mmsi_1 = re.split(r'/', mmsi1)
                            try:
                                mmsi = mmsi_1[1].replace(' ', '')
                            except:
                                mmsi = mmsi_1[0].replace(' ', '')
                        #print(mmsi)
                        #Reference
                            reference = f'https://www.vesselfinder.com/?mmsi={mmsi}'
                        except:
                            mmsi = '-'
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
                    tr5 = table_main.findAll('tr')[5]
                    if tr5 != None:
                        try:
                            pos_recieved_0 = tr5.find('td',class_='v3 ttt1').text
                            pos_recieved1 = pos_recieved_0.replace('i','')
                            pos_recieved = pos_recieved1.rstrip()
                        except:
                            pos_recieved = '-'
                        #print(pos_recieved)
                    else:
                        pos_recieved = '-'


        ##Speed
        flx = vx_top_0.findAll('div', class_='flx')[1]
        if flx != None:
                table_0 = flx.find('table',class_='aparams')
                if table_0 != None:
                    table_main = table_0.find('tbody')
                    if table_main != None:
                        tr5 = table_main.findAll('tr')[2]
                        if tr5 != None:
                            try:
                                speed_0 = tr5.find('td',class_='v3').text
                                speed1 = re.split(r'/', speed_0)
                            except:
                                speed= '-'
                            try:
                                speedx = speed1[1].replace(' ', '')
                            except:
                                speedx = speed1[0].replace(' ', '')
                            speed2 = speedx.replace('kn','')
                            if speed2 != '-' and speed2 != '':
                                try:
                                    speed_float = float(speed2) * 1.852
                                    speedr = round(speed_float,1)
                                    speed = str(speedr)
                                except:
                                    speed= '-'

                                #############HEREEE
                            else:
                                speed = '-'
                            #print(speed)

        ##type
        vessel_type = 'Cargo'

        ##Status
        flx = vx_top_0.findAll('div', class_='flx')[1]
        if flx != None:
            table_0 = flx.find('table',class_='aparams')
            if table_0 != None:
                table_main = table_0.find('tbody')
                if table_main != None:
                    tr5 = table_main.findAll('tr')[4]
                    if tr5 != None:
                        try:
                            status1 = tr5.find('td',class_='v3').text
                            if len(status1) == 62:
                                status = '-'
                            else:
                                status = status1.replace('\n', '')
                        except:
                            status = '-'


                        #print(status)
                    else:
                        status = '-'

    #Заполнение таблички
    data.loc[len(data)] = [today_str, callsign, vessel_type, flag, mmsi, current_position, cord_n, cord_w, pos_recieved, speed, status, destination, ETA, reference]
data.drop_duplicates()
os.chdir('/home/hiradik/marine_data')
data.to_csv(f'{today_str}.csv', index=False)
