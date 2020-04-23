# Reuters-News-Articles-Crawler
This Python script, *scrap_reuters.py* contains functions to scrap stock news articles from www.reuters.com using beautifulsoup package

## Table of Cotent
[Modules Required](#Module)
[Feature](#Feature)  

## Feature
```python
def scrap_all_of(ticker)
```
This function can scrap all news articles regarding to the given a stock ticker from www.reuters.com
The function returns a pandas dateframe with columns 'Date', 'Ticker', 'Article'

Example:
Scrap articles with ticker 'MMM' (3M Company)
```python
test_mmm = scrap_all_of('MMM')
```
