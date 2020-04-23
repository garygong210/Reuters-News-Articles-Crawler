# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 00:41:15 2019

@author: Jianxiang Gong
"""
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def get_news_urls(links_site):
    '''convert html to BeautifulSoup object'''
    resp = requests.get(links_site)
    if not resp:
        return None
    html = resp.content
    soup = BeautifulSoup(html , 'lxml')
    '''get list of all links on webpage'''
    links = soup.find_all('div', attrs={"class": "search-stock-ticker"})
    urls = [link.find('a')['href'] for link in links]
    urls = 'https:' + urls[0] + '/news' 
    
    html_ = load_all(urls)
    soup_ = BeautifulSoup(html_ , 'lxml')
    links_ = soup_.find_all('div', attrs={"class": "FeedScroll-feed-container-106s7"})
    sub_links = [l.find_all('div', attrs={"class": "item"}) for l in links_][0]
    urls_ = [link.find('a')['href'] for link in sub_links]
    return urls_

def scrap_news_of(articles_url):
    '''Get HTML of the webpage associated with articles_url'''
    articles_html = requests.get(articles_url).content
    
    '''Convert articles_url to a BeautifulSoup object'''
    articles_soup = BeautifulSoup(articles_html , 'lxml')
    
    '''Use news_soup to get the text from all pargraphs on page'''
    dateAll = [ele.text for ele in articles_soup.find_all('div', 'ArticleHeader_date')][0].split('/')
    date = dateAll[0].strip() + ' ' + dateAll[1].strip()
    article_date = datetime.datetime.strptime(date, '%B %d, %Y %H:%M %p')
    header = [ele.text for ele in articles_soup.find_all('h1', "ArticleHeader_headline")][0]
    body_content = [par for par in articles_soup.find_all('div', 'StandardArticleBody_body')][0]
    body_content = [par.text for par in body_content.find_all('p', None)]
    
    '''Lastly, join all text in the list above into a single string'''
    articles_text = header + '\n'.join(body_content)
    return article_date, articles_text

def scrap_all_of(ticker):
    site = 'https://www.reuters.com/search/news?blob=' + ticker
    articles_urls = get_news_urls(site)
    col_names = ['Date', 'Ticker', 'Article']
    articles_df = pd.DataFrame(columns = col_names)
    print('Getting news articles for {0}'.format(ticker))
    for articles_url in articles_urls:
        try:
            article_date, articles_text = scrap_news_of(articles_url)
            article_dic = {'Date':article_date, 'Ticker':ticker, 'Article':articles_text}
            articles_df.loc[len(articles_df)] = article_dic
        except:
            continue
        try:
            articles_df.drop_duplicates(subset=['Article'], keep='first', inplace=True)
        except:
            continue
        articles_df = articles_df[~articles_df.Article.str.contains("US STOCKS-")]
        articles_df = articles_df[~articles_df.Article.str.contains("US STOCKS SNAPSHOT-")]
        articles_df = articles_df[~articles_df.Article.str.contains("click on the link below")]
    return articles_df.reset_index(drop = True)

def load_all(url):
    options = Options()
    options.add_argument("--disable-notifications")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options = chrome_options)
    driver.get(url)
  
    SCROLL_PAUSE_TIME = 1

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
    
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    html = driver.page_source.encode('utf-8')
    return html

#test = scrap_all_of('MMM')
