class Assistent:
    name = ''
    country = None
    city = None
    latlng = None
    timeStartVar = None
    dates = []
    times = []
    texts = []

    def __init__(self, name):
        self.name = name

    def timeNow(self):
        from datetime import datetime

        time = datetime.now().time()

        return time

    def dateNow(self):
        from datetime import datetime

        date = datetime.utcnow().date()

        return date

    def reminder(self, text, year, month, day, hour, minute, second):
        import pyttsx3
        import datetime

        date = datetime.date(year, month, day)
        time = datetime.time(hour, minute, second)
        self.dates.append(date)
        self.times.append(time)
        self.texts.append(text)
        pyttsx = pyttsx3.init()
        pyttsx.say('Напоминание добавлено')
        pyttsx.runAndWait()

        return 'Напоминание добавлено'

    def timeStart(self):
        import datetime
        import pyttsx3

        pyttsx = pyttsx3.init()
        if self.timeStartVar == None:
            timeStartVar = datetime.datetime.utcnow()
            self.timeStartVar = timeStartVar
            pyttsx.say('Время пошло')
            pyttsx.runAndWait()

            return 'Время пошло'
        else:
            pyttsx.say('Вначале остановить секондомер')
            pyttsx.runAndWait()

            return 'Вначале остановить секондомер'

    def timeStop(self):
        import datetime
        import pyttsx3

        pyttsx = pyttsx3.init()
        timeStop = datetime.datetime.utcnow()
        time = timeStop - self.timeStartVar
        pyttsx.say(f'Время: {time}')
        self.timeStartVar = None

        return f'Время: {time}'


    def os(self):
        import os, sys
        OS = {'name': os.name, 'Dict vars': os.environ, 'user': os.getlogin()}

        return OS

    def open(self, path):
        import os
        import pyttsx3

        pyttsx = pyttsx3.init()
        file_path = r'{}'.format(path)
        os.system("start " + file_path)
        pyttsx.say('Прграмма открыта')
        pyttsx.runAndWait()

    def parser(url, intag, tag, incl, cl):
        import requests
        from bs4 import BeautifulSoup

        page = requests.get(url)
        all = []
        out = []
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'html.parser')
            all = soup.find_all(intag, class_=incl)
            for i in range(len(all)):
                if all[i].find(tag, class_=cl) is not None:
                    out.append(all[i].text)
            return out, page
        elif page.status_code == 404:
            return 'Server\'s error'
        elif page.status_code == 505:
            return 'Client\'s error'
        else:
            return 'Error'

    def geolocation(self, say):
        import geocoder
        import pyttsx3

        pyttsx = pyttsx3.init()
        g = geocoder.ip('me')
        city = g.city
        latlng = g.latlng
        country = g.country
        self.country = country
        self.city = city
        self.latlng = latlng
        if say:
            pyttsx.say(f'Страна: {country}, город: {city}, место: {latlng}')
            pyttsx.runAndWait()

        return country, city, latlng

    def weather(self):
        import requests
        from bs4 import BeautifulSoup
        import pyttsx3

        pyttsx = pyttsx3.init()
        if not self.city:
            country, city, lan = Assistent.geolocation(self, False)
            self.city = city
            self.country = country
            self.latlng = lan
        else:
            city = self.city
        url = f'https://yandex.ru/pogoda/{city}?utm_source=serp&utm_campaign=wizard&utm_medium=desktop&utm_content=wizard_desktop_main&utm_term=title'
        request = requests.get(url)
        bs = BeautifulSoup(request.text, 'html.parser')
        temp = bs.find('div', {'class': 'temp fact__temp fact__temp_size_s'}).text
        pyttsx.say(f'Погода: {temp}')
        pyttsx.runAndWait()

        return temp

    def search(self, text):
        import pyttsx3
        import webbrowser

        pyttsx = pyttsx3.init()
        url = 'https://yandex.ru/search/?text=' + '%20'.join(text.split(' ')) + '&lr=55'
        webbrowser.open(url, new=2)
        pyttsx.say('Открыл страницу')
        pyttsx.runAndWait()

        return url

    def toremember(self, text):
        import pyttsx3

        pyttsx = pyttsx3.init()
        with open('storage.txt', 'w') as f:
            f.write(text)
            pyttsx.say('Запомнила')
            pyttsx.runAndWait()

    def fromremember(self):
        import pyttsx3

        pyttsx = pyttsx3.init()
        with open('storage.txt') as f:
            data = f.read()
            pyttsx.say('Моя память:\n' + data)
            pyttsx.runAndWait()

            return data

    def intoremember(self, text):
        import pyttsx3

        pyttsx = pyttsx3.init()
        with open('storage.txt', 'a') as f:
            f.write(text+'\n')
            pyttsx.say('Добавила')
            pyttsx.runAndWait()

def max(a, b): return a if a>b else b


pathes = {'cmd': 'C:\windows\system32\cmd.exe', 'command': 'C:\windows\system32\cmd.exe'}

assistent = Assistent('Ассистент')
while True:
    event = input('Что нужно сделать: ').strip()
    if 'местоположение' in event:
        print(assistent.geolocation(True))
    elif 'погода' in event:
        print(assistent.weather())
    elif 'найди' in event:
        data = event.split('найди')
        data = data[0].strip() + data[1].strip()
        assistent.search(data)
    elif 'время' in event:
        print(assistent.timeNow())
    elif 'день' in event:
        print(assistent.dateNow())
    elif 'ос' in event:
        print(assistent.os())
    elif 'открой' in event:
        app = event.replace('открой', '').strip()
        assistent.open(pathes[app])
    elif 'запомни' in event:
        text = event.replace('запомни', '').strip()
        assistent.toremember(text)
    elif 'вспомни' in event:
        print(assistent.fromremember())
    elif 'добавь' in event:
        text = event.replace('добавь', '').strip()
        assistent.intoremember(text)
    elif 'старт' in event:
        print(assistent.timeStart())
    elif 'стоп' in event:
        print(assistent.timeStop())