import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt
import six
import csv



url = 'https://www.worldometers.info/coronavirus/'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
info = soup.findAll('div', {'class': 'maincounter-number'})

def get_stats():
    with open('stats.txt', 'w', newline='') as file:
        for i, v in enumerate(('Cases', 'Deaths', 'Recovered')):
            file.writelines(f'{v}: {info[i].get_text().strip()}\n')

def get_table():
    table = soup.find('table', {'id': 'main_table_countries'})
    table_body = table.find('tbody')
    header = 'Country,Total Cases,New Cases,Total Deaths,New Deaths,Active Cases,Total Recovered,Serious, Tot Cases/1M pop'.split(',')
    data = []
    rows = table_body.find_all('tr')
    tabulate.PRESERVE_WHITESPACE = True
    for row in rows:
        cols = row.find_all('td')
        cols = [i.text.strip() for i in cols]
        data.append([i for i in cols])
    df = pd.DataFrame(data, columns = header)

    # print(df.iloc[[39]])
    # img = Image.new('RGB', (960, 2000), color='white')
    # img.save('pil_white.png')
    # d = ImageDraw.Draw(img)
    # fontsize = 20
    # font = ImageFont.truetype("arial.ttf", fontsize)
    # d.text((10, 10), tabulate(df, headers=header, showindex=False), fill= 'black', font = font)
    # img.save('pil_text.png')

    with open('stats.csv', 'w', newline='') as file :
        export_csv = df.to_csv(r'/home/tommy/PycharmProjects/coronastats/stats.csv',index=False, header=header)
    with open('corona_table.txt', 'w', newline='') as file1 :
        file1.write(tabulate(df, headers=header, showindex=False))

def get_news():
    inner_content = soup.find('div', {'id': 'innercontent'})
    lists = inner_content.findAll('ul')
    delete_list = ["[source]"]
    with open('news.txt', 'w', newline='') as file:
        for i in lists:
            x = i.findAll('li')
            bullets = [x[i].text.strip().rstrip(' [source]') for i in range(len(x))]
            for x in bullets:
                file.write(f". {x}\n")
       


get_stats()
get_table()
get_news()
