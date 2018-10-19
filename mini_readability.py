from html.parser import HTMLParser
import urllib.request 
import re
import textwrap 
import sys
import os

class MyHTMLParser(HTMLParser): # класс для парсинга страницы

    def __init__(self):
        super().__init__()

        self.counter = False #счетчик для сбора данных
        self.list_of_tags = ["p","h1", "a"] # список аргументов 
        self.paragraph = [] # параграф  
        self.content = [] # весь текст
        self.link = [] # ссылка
        self.p_tag = False # счетчик р тега
        self.saver = None # обЪект класса ContentSaver
        self.config_file = None # кастомный конфиг
        
        self.config_file = open('config.txt') #считывание тегов из текстового файла
        tags = self.config_file.read()
        if tags:
            self.list_of_tags = tags

    def get_paragraph(self): # форматирование абзаца и добавление к остальному контенту
        self.counter = False              
        if re.findall(r'\w{1}',' '.join(self.paragraph)): 
            if self.content !=[]:
                self.content.append(("\n\n"+textwrap.fill(' '.join(self.paragraph)+ "\n", 80)))
            else: self.content.append((textwrap.fill(' '.join(self.paragraph)+ "\n", 80))) 
        self.paragraph = []         
        self.p_tag = False 

    def get_link(self, tag, attrs): # получение ссылок в тексте
        d = None
        if tag == "a": 
            for attr in attrs:
                if attr[0] == "href" and self.p_tag:
                    if self.validate(attr[0],attr[1]): 
                        self.link.append("["+attr[1]+"]")
                    else:
                        if self.p_tag is False: self.counter = False  
                else: 
                    if self.p_tag is False: self.counter = False 
        if tag == "p": 
            self.p_tag = True 

    def handle_starttag(self, tag, attrs): # функция обработки открывающего тега
        if tag not in self.list_of_tags:      
            return 
        self.counter = True
        self.get_link(tag,attrs)
    
    def handle_data(self, data): # функция обработки данных между тегами
        if self.counter: 
            self.paragraph.append(' '.join(data.split())) 
            if self.link !=[]:
                self.paragraph.append(''.join(self.link)) 
                self.link = [] 
    
    def handle_endtag(self, tag): # проверка закрывающего тега
        if tag in self.list_of_tags:
            if self.p_tag and tag != "p":
                return
        self.get_paragraph()

    def output(self): # передача готового контента в класс ContentSaver для последующей записи
        self.content = ' '.join(self.content)
        self.saver = ContentSaver()
        self.saver.take_it(self.content)

    def validate(self, link, http): # проверка сслыки на вызов скрипта или наличие перенаправления + что ссылка не является внутренней 
        if '#' in link or 'javascript:' in link:
            return False
        if re.findall(r'http', http):
            return True
        else: return False

class ContentSaver: # запуск парсера, создание директории и файла для контента, запись в файл
    
    def take_it(self,content): # запись контента в файл
        path = self.path_creator(url)
        if path:
            path+= '/index.txt'
        else:
            path = 'index.txt'
        f = open(path, 'w')
        try:
            f.write(content)
            print("Контент успешно сохранен")
        except: print("Ошибка записи контента в файл")
        f.close()
    
    def path_creator(self,url): # создание директории, в которой хранится файл
        file_path = re.sub(r'https://|http://', '', url)
        directory = os.path.dirname(file_path)
        try:
            os.makedirs(directory)
        except:
            print("В процессе создания директории произошла ошибка \nФайл будет сохранен в корне")
            directory = '' 
        return directory

    def parse_start(url): # открытие страницы, декодинг и запуск парсера
        response= None
        try:
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
        except:
            print("Url_open error")
        if response:
            try:
                content = response.read().decode(response.headers.get_content_charset())
                parser = MyHTMLParser()
                parser.feed(content)
                parser.output()
            except:
                print("Decode error")

if len(sys.argv) > 1: # проверка на наличие url в аргументах при запуске программы
    url = sys.argv[1]
    ContentSaver.parse_start(url)
else: 
    print("Введите url страницы")
