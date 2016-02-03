#!/usr/bin/python3

from urllib.request import urlopen
from urllib import error
import http
from bs4 import BeautifulSoup
import re

#
def fetchHtml(url):
  print('Fetching '+ url)
  try:
    response = urlopen(url)

  except error.HTTPError as e:
    print('HTTPError = ' + str(e.code))
    return None

  except error.URLError as e:
    print('URLError = ' + str(e.reason))
    return None

  except http.client.HTTPException as e:
    print('HTTPException')
    return None

  except Exception as e:
    import traceback
    print('generic exception: ' + traceback.format_exc())
    return None

  return response.read()

#
def hasNoResults(soup):
  noresults = len(soup.find_all('div', class_="noresults"))
  if(noresults > 0):
    return True
  return False

#
def addQuery(string, query, category):
  if(category == None):
    category = 'sss'
  return string + 'search/{0!s}?query={1!s}'.format(category, query)

#
def getDataFromHtml(html):
  if(html == None):
    return None
  soup = BeautifulSoup(html, 'html.parser')
  if (hasNoResults(soup)):
    return None
  data = list()
  return data

#
def storeData(data):
  print('store results')
  if (data == None):
    return
  if(len(data) <= 0 ):
    return None

#
def getList(query, category):
  sites = 'http://www.craigslist.org/about/sites'
  html = fetchHtml(sites)
  htmlParsed = BeautifulSoup(html, 'html.parser')
  h1 = htmlParsed.find('a', attrs={'name':'US'}).parent
  div = h1.next_sibling.next_sibling
  links = list()
  for link in div.find_all('a', href = re.compile('org')):
    links.append(addQuery('http:' + link.get('href'), query, category))
  return links
