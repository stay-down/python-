# encoding:utf-8

import requests
import re
import time
import csv
import pymysql

POMES = []

def wrte_csv(POMES):
    print(POMES)
    headers = ['标题','朝代','作者','内容']

    with open('D://poems.csv','a',newline='') as fp:
       writer = csv.DictWriter(fp,headers)
       writer.writeheader()
       writer.writerows(POMES)


    # with open('classrom_csv', 'w', encoding='utf-8', newline='') as fp:
    #     writer = csv.DictWriter(fp.headers)
    #     writer.writeheader()
    #     writer.writerows(values)

def page_source_url(url):

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                     ' Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3722.400 QQBrowser/10.5.3751.400'
    }

    text = requests.get(url,headers=headers).text
    title = re.findall(r'<div\sclass="cont">.*?<b>(.*?)</b>',text,re.DOTALL)
    dynasty = re.findall(r'<p\sclass="source">.*?<a.*?>(.*?)</a>',text,re.DOTALL)
    author = re.findall(r'<p\sclass="source">.*?<a.*?>.*?</a>.*?<a.*?>(.*?)</a>',text,re.DOTALL)
    all_contonts = re.findall(r'<div class="contson".*?>(.*?)</div>',text,re.DOTALL)
    contonts = []

    for all_contont in all_contonts:
        contont = re.sub(r'<.*?>','',all_contont)
        contonts.append(contont.strip())

    for value in zip(title,dynasty,author,contonts):
        title,dynasty,author,contont = value
        poem = {
            '标题':title,
            '朝代':dynasty,
            '作者':author,
            '内容':contont
        }
        # print(poem)
        POMES.append(poem)





def main():
    urls = 'https://www.gushiwen.org/default_{}.aspx'

    for num in range(1,11):
        url = urls.format(num)

        # url = 'https://www.gushiwen.org/default_%s.aspx' % num

        page_source_url(url)
        time.sleep(0.5)


    wrte_csv(POMES)
    # insert_pymysql()
    # print(POMES)

def insert_pymysql():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        database='pymysql',
        port=3306
    )

    cursor = conn.cursor()
    for poem in POMES:
        sql = '''insert into poems (id ,title,dynasty,author,contont) VALUES (DEFAULT ,%s,%s,%s,%s)'''
        title = poem['标题']
        dynasty = poem['朝代']
        author = poem['作者']
        contont = poem['内容']
        cursor.execute(sql, (title, dynasty, author, contont))
        conn.commit()

    cursor.close()

if __name__ == '__main__':
    main()