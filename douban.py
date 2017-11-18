#!usr/bin/even python
# -*- coding:utf-8 -*-

import urllib
import bs4
import requests
import random
import time
import xlwt
import sys
import fake_useragent

reload(sys)
sys.setdefaultencoding('utf8')

book_tag = u'推理'
#need_pages = 10

def get_book_list():
    book_list = []
    try_times = 0
    page_num = 0

    while True:
        time.sleep(random.random()*5)
        url = 'https://book.douban.com/tag/'+urllib.quote(book_tag.encode('utf-8'))+'?start='+str(page_num*20)+'&type=T'
        fa = fake_useragent.UserAgent()
        headers = {'User-Agent': fa.random,
                  'Referer': 'https://book.douban.com'}

        try:
            response = requests.get(url, headers=headers)
        except:
            exit(1)

        soup = bs4.BeautifulSoup(response.content, 'lxml')
        all_books = soup.find('ul', attrs={'class': 'subject-list'}).find_all('li')
        try_times += 1
        if len(all_books) < 1 and try_times < 100:
            continue
        elif len(all_books) < 1 and try_times >= 100:
            break

        for i in xrange(len(all_books)):
            try:
                book_name = all_books[i].find('a', attrs={'title': True}).get('title').strip().encode('utf-8')
            except:
                book_name = '书名读取失败'

            try:
                book_url = all_books[i].find('a', attrs={'title': True}).get('href').strip().encode('utf-8')
            except:
                book_url = 'URL读取失败'

            try:
                book_wdp = all_books[i].find('div', attrs={'class': 'pub'}).get_text().strip().encode('utf-8').split('/')
            except:
                book_wdp = ['读取失败', '读取失败', '读取失败']

            try:
                book_writer = book_wdp[0].strip()
            except:
                book_writer = '读取失败'

            try:
                book_date = book_wdp[-2].strip()
            except:
                book_date = '读取失败'

            try:
                book_price = book_wdp[-1].strip()
            except:
                book_price = 0

            try:
                book_rating = float(all_books[i].find('div', attrs={'class': 'star clearfix'}).find('span', attrs={'class': 'rating_nums'}).get_text().strip().encode('utf-8'))
            except:
                book_rating = 0.0

            try:
                book_p_num = int(all_books[i].find('div', attrs={'class': 'star clearfix'}).find('span', attrs={'class': 'pl'}).get_text().strip().encode('utf-8')[1: -10])
            except:
                book_p_num = 0
            book_list.append([book_name, book_url, book_writer, book_date, book_price, book_rating, book_p_num])
        page_num += 1
        try_times = 0
        print '第'+str(page_num)+'页'
#        if page_num >= need_pages:
#            break

    return book_list


def write():
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet(book_tag)
    books = get_book_list()
    i = 1
    worksheet.write(0, 0, '序号')
    worksheet.write(0, 1, '书名')
    worksheet.write(0, 2, 'url')
    worksheet.write(0, 3, '作者')
    worksheet.write(0, 4, '日期')
    worksheet.write(0, 5, '价格')
    worksheet.write(0, 6, '评分')
    worksheet.write(0, 7, '评论人数')
    for book in books:
        worksheet.write(i, 0, i)
        worksheet.write(i, 1, book[0].decode('utf-8'))
        worksheet.write(i, 2, book[1].decode('utf-8'))
        worksheet.write(i, 3, book[2].decode('utf-8'))
        worksheet.write(i, 4, book[3].decode('utf-8'))
        worksheet.write(i, 5, book[4].decode('utf-8'))
        worksheet.write(i, 6, book[5])
        worksheet.write(i, 7, book[6])
        i += 1

    workbook.save(book_tag+'.xls')


if __name__ == '__main__':
    write()
